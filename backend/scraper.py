import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict
import re

class WebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.timeout = 10
        self.max_content_length = 15000  # Increased from 8000
        self.playwright_available = False
        try:
            from playwright.async_api import async_playwright
            self.async_playwright = async_playwright
            self.playwright_available = True
        except ImportError:
            print("Playwright not available, using httpx only")
    
    async def scrape_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """Scrape multiple URLs in parallel"""
        tasks = [self._scrape_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        cleaned_results = []
        for result in results:
            if isinstance(result, dict) and result.get("content") and len(result.get("content", "")) > 100:
                cleaned_results.append(result)
        
        return cleaned_results
    
    async def _scrape_single(self, url: str) -> Dict[str, str]:
        """Scrape a single URL with fallback to Playwright"""
        try:
            # Try httpx first (faster)
            content = await self._scrape_with_httpx(url)
            if content and len(content) > 100:
                return {
                    "url": url,
                    "title": self._extract_title_from_url(url),
                    "content": content[:self.max_content_length]
                }
            
            # Fallback to Playwright for JS-heavy sites
            if self.playwright_available:
                content = await self._scrape_with_playwright(url)
                if content and len(content) > 100:
                    return {
                        "url": url,
                        "title": self._extract_title_from_url(url),
                        "content": content[:self.max_content_length]
                    }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        return {"url": url, "content": ""}
    
    async def _scrape_with_httpx(self, url: str) -> str:
        """Scrape using httpx"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                return self._extract_content(soup)
        except Exception as e:
            print(f"httpx error for {url}: {e}")
            return ""
    
    async def _scrape_with_playwright(self, url: str) -> str:
        """Scrape using Playwright for JS-heavy sites"""
        try:
            async with self.async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=15000)
                
                # Wait for content to load
                await page.wait_for_timeout(2000)
                
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                await browser.close()
                return self._extract_content(soup)
        except Exception as e:
            print(f"Playwright error for {url}: {e}")
            return ""
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract meaningful text from soup"""
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header", "noscript", "meta", "link"]):
            element.decompose()
        
        content_parts = []
        
        # Try to find main content area
        main_content = soup.find(["main", "article", "div.content", "div.post", "div.entry"])
        if main_content:
            soup = main_content
        
        # Extract headings and paragraphs with better filtering
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "span"]):
            text = tag.get_text(strip=True)
            
            # Filter out short or irrelevant text
            if text and len(text) > 30 and not self._is_navigation_text(text):
                content_parts.append(text)
        
        # Join with proper spacing
        content = " ".join(content_parts)
        
        # Clean up multiple spaces
        content = re.sub(r"\s+", " ", content)
        
        # Keep alphanumeric, spaces, and common punctuation
        # Don't remove special characters that might be part of words
        content = re.sub(r"[^\w\s\.\,\!\?\-\:\;\'\"\(\)&]", " ", content)
        
        # Clean up multiple spaces again after removing special chars
        content = re.sub(r"\s+", " ", content)
        
        return content.strip()
    
    def _is_navigation_text(self, text: str) -> bool:
        """Check if text is navigation/UI element"""
        nav_keywords = ["menu", "home", "about", "contact", "login", "sign up", "subscribe", 
                       "follow", "share", "like", "comment", "read more", "click here", "advertisement"]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in nav_keywords)
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract title from URL"""
        try:
            # Get domain name
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            return domain
        except:
            return "Source"

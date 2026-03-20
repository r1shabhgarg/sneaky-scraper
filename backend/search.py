import httpx
import os
from typing import List

class SearchAPI:
    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"
    
    async def search(self, query: str, count: int = 12) -> List[dict]:
        """Search using Tavily Search API"""
        if not self.tavily_api_key:
            return self._mock_search(query, count)
        
        payload = {
            "api_key": self.tavily_api_key,
            "query": query,
            "max_results": count,
            "include_answer": True
        }
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                results = []
                for item in data.get("results", []):
                    results.append({
                        "url": item.get("url"),
                        "title": item.get("title"),
                        "description": item.get("content", "")
                    })
                return results
        except Exception as e:
            print(f"Search API error: {e}")
            return self._mock_search(query, count)
    
    def _mock_search(self, query: str, count: int) -> List[dict]:
        """Fallback mock search for testing"""
        return [
            {
                "url": f"https://example{i}.com/article",
                "title": f"Article about {query} - Part {i}",
                "description": f"Information about {query}"
            }
            for i in range(1, count + 1)
        ]

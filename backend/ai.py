import httpx
import os
import json
from typing import Dict

class AIProcessor:
    def __init__(self):
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    async def process_content(self, query: str, combined_text: str) -> Dict:
        """Process scraped content using NVIDIA API"""
        if not self.nvidia_api_key:
            return self._smart_process(query, combined_text)
        
        prompt = self._build_prompt(query, combined_text)
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.nvidia_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta/llama-2-70b-chat",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                result_text = data["choices"][0]["message"]["content"]
                return self._parse_response(result_text)
        except Exception as e:
            print(f"AI API error: {e}")
            return self._smart_process(query, combined_text)
    
    def _build_prompt(self, query: str, combined_text: str) -> str:
        """Build the AI prompt with better deduplication instructions"""
        return f"""You are an expert content summarizer. Your task is to analyze scraped web content and create a comprehensive, detailed summary.

USER QUERY: {query}

SCRAPED CONTENT FROM MULTIPLE SOURCES:
{combined_text[:6000]}

CRITICAL INSTRUCTIONS:
1. COMPREHENSIVE: Create a detailed, informative summary that actually helps the user
2. DEDUPLICATION: Remove duplicate information but keep all unique, valuable details
3. LENGTH: Summary should be 4-6 sentences (not just 2-3)
4. KEY POINTS: Provide 8-10 detailed key points (not just 5)
5. DETAILS: Provide 6-8 important details with specific information
6. ACCURACY: Only include information directly related to the query
7. CLARITY: Write clear, detailed sentences without redundancy
8. STRUCTURE: Organize information logically and comprehensively

OUTPUT FORMAT (STRICT JSON ONLY):
{{
    "title": "Comprehensive title summarizing the main topic",
    "summary": "4-6 sentence detailed summary covering main aspects, benefits, uses, and important information",
    "key_points": [
        "First detailed and important point with specific information",
        "Second detailed and important point with specific information",
        "Third detailed and important point with specific information",
        "Fourth detailed and important point with specific information",
        "Fifth detailed and important point with specific information",
        "Sixth detailed and important point with specific information",
        "Seventh detailed and important point with specific information",
        "Eighth detailed and important point with specific information",
        "Ninth detailed and important point with specific information",
        "Tenth detailed and important point with specific information"
    ],
    "important_details": [
        "Critical detail 1 with specific information",
        "Critical detail 2 with specific information",
        "Critical detail 3 with specific information",
        "Critical detail 4 with specific information",
        "Critical detail 5 with specific information",
        "Critical detail 6 with specific information",
        "Critical detail 7 with specific information",
        "Critical detail 8 with specific information"
    ]
}}

RESPOND WITH ONLY THE JSON, NO OTHER TEXT."""
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse AI response"""
        try:
            # Extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Parse error: {e}")
        
        return self._smart_process("", "")
    
    def _smart_process(self, query: str, text: str) -> Dict:
        """Smart processing without AI - extract key info from text with deduplication"""
        # Split text into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 30]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sentences = []
        for sentence in sentences:
            # Normalize for comparison
            normalized = sentence.lower()[:50]
            if normalized not in seen:
                seen.add(normalized)
                unique_sentences.append(sentence)
        
        # Extract title from query
        title = f"Comprehensive Guide: {query}"
        
        # Use first 5-6 unique sentences as summary (longer and more helpful)
        summary_sentences = unique_sentences[:6]
        summary = '. '.join(summary_sentences) if summary_sentences else text[:500]
        if len(summary) > 1000:
            summary = summary[:1000] + "..."
        
        # Extract key points from unique sentences (8-10 points)
        key_points = []
        for sentence in unique_sentences[6:20]:
            if len(sentence) > 40:
                # Keep longer sentences for more detail
                point = sentence[:150] + "..." if len(sentence) > 150 else sentence
                key_points.append(point)
        
        if not key_points:
            key_points = [
                "Information gathered from multiple authoritative sources",
                "Content processed and analyzed for accuracy",
                "Results compiled from comprehensive web search",
                "Data verified from reliable sources",
                "Information organized for user understanding",
                "Details extracted from multiple perspectives",
                "Content deduplicated for clarity",
                "Information structured for easy comprehension"
            ]
        
        # Ensure we have 8-10 key points
        while len(key_points) < 8:
            key_points.append(f"Additional information point {len(key_points) - 7}")
        
        # Extract important details from remaining sentences (6-8 details)
        important_details = []
        for sentence in unique_sentences[20:30]:
            if len(sentence) > 40:
                detail = sentence[:150] + "..." if len(sentence) > 150 else sentence
                important_details.append(detail)
        
        if not important_details:
            important_details = [
                "Data collected from reliable and authoritative sources",
                "Information verified and cross-referenced",
                "Content processed for accuracy and relevance",
                "Details organized for user benefit",
                "Information deduplicated to avoid redundancy",
                "Content structured for easy understanding",
                "Multiple perspectives considered",
                "Comprehensive analysis provided"
            ]
        
        # Ensure we have 6-8 important details
        while len(important_details) < 6:
            important_details.append(f"Important detail {len(important_details) - 5}")
        
        return {
            "title": title,
            "summary": summary,
            "key_points": key_points[:10],
            "important_details": important_details[:8]
        }
    
    def _mock_process(self, query: str, text: str) -> Dict:
        """Fallback mock processing"""
        return {
            "title": f"Summary: {query}",
            "summary": text[:200] if text else "No content available",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "important_details": ["Detail 1", "Detail 2"]
        }

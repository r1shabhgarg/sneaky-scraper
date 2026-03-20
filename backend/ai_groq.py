import httpx
import os
import json
from typing import Dict

class AIProcessor:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    async def process_content(self, query: str, combined_text: str) -> Dict:
        """Process scraped content using Groq API (FREE)"""
        if not self.groq_api_key:
            return self._smart_process(query, combined_text)
        
        prompt = self._build_prompt(query, combined_text)
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "mixtral-8x7b-32768",  # Fast and good quality
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                result_text = data["choices"][0]["message"]["content"]
                return self._parse_response(result_text)
        except Exception as e:
            print(f"Groq API error: {e}")
            return self._smart_process(query, combined_text)
    
    def _build_prompt(self, query: str, combined_text: str) -> str:
        """Build the AI prompt for detailed, practical responses"""
        return f"""You are an expert content curator and guide writer. Your task is to create a comprehensive, practical, and actionable guide based on scraped web content.

USER QUERY: {query}

SCRAPED CONTENT FROM MULTIPLE SOURCES:
{combined_text[:8000]}

CRITICAL INSTRUCTIONS:
1. PRACTICAL & ACTIONABLE: Provide real, usable information that helps the user immediately
2. DETAILED EXPLANATIONS: Explain what things are, how they work, why they matter
3. STEP-BY-STEP GUIDES: Include recipes, instructions, or how-to steps when relevant
4. SPECIFIC DETAILS: Include measurements, temperatures, times, ingredients, quantities
5. REAL EXAMPLES: Use concrete examples and specific information from the content
6. WELL-ORGANIZED: Use clear sections, bullet points, and formatting for readability
7. COMPREHENSIVE: Cover all important aspects - what it is, how to make it, how to use it, tips
8. ENGAGING: Make it interesting and easy to read with emojis and formatting where appropriate

OUTPUT FORMAT (STRICT JSON ONLY):
{{
    "title": "Comprehensive guide title",
    "summary": "Detailed 4-6 sentence introduction explaining what it is, why it matters, and key overview",
    "key_points": [
        "Detailed point 1 with specific information, measurements, or steps",
        "Detailed point 2 with specific information, measurements, or steps",
        "Detailed point 3 with specific information, measurements, or steps",
        "Detailed point 4 with specific information, measurements, or steps",
        "Detailed point 5 with specific information, measurements, or steps",
        "Detailed point 6 with specific information, measurements, or steps",
        "Detailed point 7 with specific information, measurements, or steps",
        "Detailed point 8 with specific information, measurements, or steps",
        "Detailed point 9 with specific information, measurements, or steps",
        "Detailed point 10 with specific information, measurements, or steps"
    ],
    "important_details": [
        "Specific detail 1 with measurements, ingredients, or actionable steps",
        "Specific detail 2 with measurements, ingredients, or actionable steps",
        "Specific detail 3 with measurements, ingredients, or actionable steps",
        "Specific detail 4 with measurements, ingredients, or actionable steps",
        "Specific detail 5 with measurements, ingredients, or actionable steps",
        "Specific detail 6 with measurements, ingredients, or actionable steps",
        "Specific detail 7 with measurements, ingredients, or actionable steps",
        "Specific detail 8 with measurements, ingredients, or actionable steps"
    ]
}}

IMPORTANT GUIDELINES:
- If it's a recipe: Include ingredients with quantities and step-by-step instructions
- If it's a how-to: Include specific steps, measurements, and tips
- If it's a product/concept: Explain what it is, benefits, uses, and how to get/use it
- Include specific numbers, measurements, temperatures, times
- Use formatting with emojis and symbols for readability
- Make it practical and immediately useful
- Include tips, tricks, and pro advice when relevant

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
        """Smart processing - extract detailed, practical info from text"""
        # Split text into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 30]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sentences = []
        for sentence in sentences:
            normalized = sentence.lower()[:50]
            if normalized not in seen:
                seen.add(normalized)
                unique_sentences.append(sentence)
        
        # Extract title
        title = f"Complete Guide to {query}"
        
        # Create detailed summary (4-6 sentences)
        summary_sentences = unique_sentences[:6]
        summary = '. '.join(summary_sentences) if summary_sentences else text[:500]
        if len(summary) > 1200:
            summary = summary[:1200] + "..."
        
        # Extract detailed key points (8-10 with specific info)
        key_points = []
        for sentence in unique_sentences[6:25]:
            if len(sentence) > 40:
                # Keep full sentences for detail
                point = sentence[:180] + "..." if len(sentence) > 180 else sentence
                key_points.append(point)
        
        if not key_points:
            key_points = [
                f"Overview: {query} is a popular and widely used topic",
                "Benefits and advantages of using or learning about this",
                "Common uses and applications in daily life",
                "Key ingredients or components if applicable",
                "Step-by-step process or method for preparation",
                "Important tips and tricks for best results",
                "Variations and alternatives available",
                "Nutritional or practical value and benefits",
                "Where to find or how to access this",
                "Expert recommendations and best practices"
            ]
        
        # Ensure 8-10 key points
        while len(key_points) < 8:
            key_points.append(f"Additional important information about {query}")
        
        # Extract important details (6-8 with specific info)
        important_details = []
        for sentence in unique_sentences[25:40]:
            if len(sentence) > 40:
                detail = sentence[:180] + "..." if len(sentence) > 180 else sentence
                important_details.append(detail)
        
        if not important_details:
            important_details = [
                f"Detailed information about ingredients or components needed",
                f"Specific measurements, quantities, or proportions",
                f"Step-by-step instructions or process details",
                f"Cooking time, temperature, or duration if applicable",
                f"Pro tips and tricks for best results",
                f"Common mistakes to avoid",
                f"Storage or preservation methods",
                f"Serving suggestions or usage recommendations"
            ]
        
        # Ensure 6-8 important details
        while len(important_details) < 6:
            important_details.append(f"Important detail about {query}")
        
        return {
            "title": title,
            "summary": summary,
            "key_points": key_points[:10],
            "important_details": important_details[:8]
        }

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import asyncio

from search import SearchAPI
from scraper import WebScraper
from ai_groq import AIProcessor

load_dotenv()

app = FastAPI(title="Web Scraper & Summarizer API")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
search_api = SearchAPI()
scraper = WebScraper()
ai_processor = AIProcessor()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    title: str
    summary: str
    key_points: list
    important_details: list

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Main search endpoint"""
    try:
        if not request.query or len(request.query.strip()) < 2:
            raise HTTPException(status_code=400, detail="Query too short")
        
        # Step 1: Search for URLs
        search_results = await search_api.search(request.query, count=12)
        urls = [result["url"] for result in search_results if result.get("url")]
        
        if not urls:
            raise HTTPException(status_code=404, detail="No search results found")
        
        # Step 2: Scrape URLs in parallel
        scraped_data = await scraper.scrape_urls(urls)
        
        if not scraped_data:
            raise HTTPException(status_code=404, detail="Could not scrape any content")
        
        # Step 3: Combine content (skip first source in summary)
        combined_text = "\n\n".join([
            f"{item['content']}"
            for item in scraped_data[1:]  # Skip first source
        ])
        
        # Step 4: Process with AI
        ai_result = await ai_processor.process_content(request.query, combined_text)
        
        return SearchResponse(
            title=ai_result.get("title", ""),
            summary=ai_result.get("summary", ""),
            key_points=ai_result.get("key_points", []),
            important_details=ai_result.get("important_details", [])
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

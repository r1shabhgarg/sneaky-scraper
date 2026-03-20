# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SearchBar → ResultCard → LoadingSpinner             │   │
│  │  (Tailwind CSS, Responsive Design)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ (HTTP/REST)
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POST /search                                        │   │
│  │  ├─ Search Layer (search.py)                         │   │
│  │  ├─ Scraping Layer (scraper.py)                      │   │
│  │  ├─ AI Processing (ai.py)                            │   │
│  │  └─ Response Formatting                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─────────┐         ┌──────────┐
    │  Brave  │          │ Website │         │ NVIDIA   │
    │ Search  │          │  URLs   │         │   API    │
    │   API   │          │ (Scrape)│         │  (AI)    │
    └─────────┘          └─────────┘         └──────────┘
```

## Data Flow

### 1. User Input
```
User enters query → Frontend sends POST /search → Backend receives
```

### 2. Search Phase
```
Backend → Brave Search API → Returns 8 URLs
```

### 3. Scraping Phase
```
Backend → Parallel scrape all URLs (asyncio)
  ├─ URL 1 → Extract content
  ├─ URL 2 → Extract content
  ├─ URL 3 → Extract content
  └─ ... (up to 8 URLs)
→ Combine all content
```

### 4. AI Processing Phase
```
Combined content → NVIDIA API → Structured JSON
  {
    "title": "...",
    "summary": "...",
    "key_points": [...],
    "important_details": [...]
  }
```

### 5. Response
```
Backend → Frontend → Display results with sources
```

## Component Details

### Backend Components

#### main.py
- FastAPI application entry point
- Defines `/search` endpoint
- Orchestrates the pipeline
- Error handling and response formatting

#### search.py (SearchAPI)
- Integrates with Brave Search API
- Fetches top 8 URLs for query
- Fallback to mock data if API unavailable
- Validates URLs

#### scraper.py (WebScraper)
- Parallel URL scraping using asyncio
- BeautifulSoup for HTML parsing
- Removes scripts, styles, navigation
- Extracts meaningful content
- 8-second timeout per URL
- 5000 character limit per site

#### ai.py (AIProcessor)
- Sends combined content to NVIDIA API
- Builds structured prompt
- Parses JSON response
- Fallback to mock processing

### Frontend Components

#### pages/index.js
- Main page component
- State management (result, loading, error)
- Orchestrates search flow

#### components/SearchBar.js
- Input field for query
- Search button
- Disabled state during loading

#### components/ResultCard.js
- Displays title, summary, key points
- Shows important details
- Lists source URLs
- Responsive layout

#### components/LoadingSpinner.js
- Animated loading indicator
- Status messages

## API Specification

### POST /search

**Request:**
```json
{
  "query": "string (required, min 2 chars)"
}
```

**Response (200 OK):**
```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "important_details": ["string"],
  "sources": ["string (URLs)"]
}
```

**Error Responses:**
- 400: Invalid query
- 404: No results found
- 500: Server error

### GET /health

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

## Performance Characteristics

### Timing
- Search API: ~1-2 seconds
- Parallel scraping: ~8-10 seconds (8 URLs concurrently)
- AI processing: ~5-10 seconds
- **Total: ~15-30 seconds**

### Resource Usage
- Memory: ~100-200 MB
- CPU: Moderate (async I/O bound)
- Network: ~2-5 MB per search

### Scalability
- Horizontal: Can run multiple backend instances
- Vertical: Increase timeout for larger content
- Caching: Add Redis for repeated queries

## Error Handling Strategy

### Search Failures
- Fallback to mock search results
- Log error and continue

### Scraping Failures
- Skip failed URLs
- Continue with successful ones
- Timeout after 8 seconds per URL

### AI Processing Failures
- Fallback to mock processing
- Return basic structure
- Log error for debugging

### Network Issues
- Retry logic for transient failures
- Graceful degradation
- User-friendly error messages

## Security Measures

1. **Input Validation**
   - Query length validation
   - URL validation
   - Content sanitization

2. **API Security**
   - CORS configuration
   - Environment variables for secrets
   - No sensitive data in logs

3. **Scraping Safety**
   - User-Agent headers
   - Timeout limits
   - Content length limits
   - Robots.txt respect (optional)

4. **Frontend Security**
   - XSS prevention (React escaping)
   - CSRF protection (if needed)
   - Secure headers

## Deployment Architecture

### Development
```
Local Machine
├─ Backend (localhost:8000)
└─ Frontend (localhost:3000)
```

### Docker
```
Docker Compose
├─ Backend Container (port 8000)
└─ Frontend Container (port 3000)
```

### Production
```
Cloud Provider (Heroku/Railway/AWS)
├─ Backend Service
│  ├─ Multiple instances (load balanced)
│  └─ Environment variables
├─ Frontend Service (Vercel/Netlify)
│  └─ CDN distribution
└─ Optional: Redis cache, Database
```

## Extension Points

### 1. Add Caching
```python
# In main.py
from redis import Redis
cache = Redis()

# Cache search results
@app.post("/search")
async def search(request: SearchRequest):
    cache_key = f"search:{request.query}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    # ... existing logic
    cache.setex(cache_key, 3600, json.dumps(result))
```

### 2. Add Database
```python
# Store search history
from sqlalchemy import create_engine
engine = create_engine("postgresql://...")

# Log searches
db.add(SearchLog(query=query, timestamp=now()))
```

### 3. Add Authentication
```python
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/search")
async def search(request: SearchRequest, credentials = Depends(security)):
    # Verify user
```

### 4. Add Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/search")
@limiter.limit("10/minute")
async def search(request: SearchRequest):
    # ...
```

### 5. Add More AI Models
```python
# Support multiple AI providers
class AIProcessor:
    async def process_content(self, query, text, model="nvidia"):
        if model == "nvidia":
            return await self._nvidia_process(query, text)
        elif model == "openai":
            return await self._openai_process(query, text)
```

## Monitoring & Logging

### Backend Logging
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Search query: {query}")
logger.error(f"Scraping failed: {url}")
```

### Frontend Logging
```javascript
console.log("Search initiated:", query)
console.error("API error:", error)
```

### Metrics to Track
- Search latency
- Scraping success rate
- AI processing time
- Error rates
- API usage

## Testing Strategy

### Backend Tests
```python
# test_search.py
def test_search_endpoint():
    response = client.post("/search", json={"query": "test"})
    assert response.status_code == 200

# test_scraper.py
async def test_scrape_urls():
    scraper = WebScraper()
    results = await scraper.scrape_urls(["https://example.com"])
    assert len(results) > 0
```

### Frontend Tests
```javascript
// __tests__/SearchBar.test.js
test("renders search input", () => {
  render(<SearchBar />)
  expect(screen.getByPlaceholderText(/search/i)).toBeInTheDocument()
})
```

## Future Enhancements

1. **Advanced Features**
   - Multi-language support
   - Custom scraping rules per site
   - Advanced filtering options
   - Search history and bookmarks

2. **Performance**
   - Redis caching layer
   - Database for history
   - CDN for static assets
   - Image optimization

3. **AI Improvements**
   - Multiple AI model support
   - Custom summarization styles
   - Entity extraction
   - Sentiment analysis

4. **User Experience**
   - User accounts and preferences
   - Saved searches
   - Export results (PDF, JSON)
   - Advanced search syntax

5. **Infrastructure**
   - Kubernetes deployment
   - Microservices architecture
   - Message queue (RabbitMQ)
   - Real-time updates (WebSocket)

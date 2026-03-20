# API Examples & Usage Guide

## Quick Start

### Using cURL

```bash
# Basic search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Dhurandhar 2"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={"query": "Dhurandhar 2"}
)

result = response.json()
print(result["title"])
print(result["summary"])
```

### Using JavaScript/Fetch

```javascript
const response = await fetch("http://localhost:8000/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "Dhurandhar 2" })
})

const result = await response.json()
console.log(result.title)
console.log(result.summary)
```

### Using Axios

```javascript
import axios from "axios"

const result = await axios.post("http://localhost:8000/search", {
  query: "Dhurandhar 2"
})

console.log(result.data.title)
console.log(result.data.summary)
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Purpose:** Check if the API is running

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok"
}
```

### 2. Search & Summarize

**Endpoint:** `POST /search`

**Purpose:** Search web, scrape content, and generate AI summary

**Request Body:**
```json
{
  "query": "string (required, minimum 2 characters)"
}
```

**Response (200 OK):**
```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string", "string", "string"],
  "important_details": ["string", "string"],
  "sources": ["https://example1.com", "https://example2.com"]
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "Query too short"
}
```

404 Not Found:
```json
{
  "detail": "No search results found"
}
```

500 Server Error:
```json
{
  "detail": "Error message"
}
```

## Example Requests & Responses

### Example 1: Movie Search

**Request:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Dhurandhar 2 movie"}'
```

**Response:**
```json
{
  "title": "Dhurandhar 2 - Indian Film",
  "summary": "Dhurandhar 2 is an Indian action thriller film that continues the story of the original Dhurandhar. The film features intense action sequences and explores themes of justice and revenge. It has received mixed reviews from critics but has a dedicated fan following.",
  "key_points": [
    "Sequel to the original Dhurandhar film",
    "Features high-octane action sequences",
    "Explores themes of justice and revenge",
    "Released in Indian cinema",
    "Mixed critical reception"
  ],
  "important_details": [
    "Directed by [Director Name]",
    "Stars [Actor Names]",
    "Runtime approximately 2 hours",
    "Available on streaming platforms",
    "Box office performance exceeded expectations"
  ],
  "sources": [
    "https://en.wikipedia.org/wiki/Dhurandhar_2",
    "https://www.imdb.com/title/tt...",
    "https://www.rottentomatoes.com/...",
    "https://www.youtube.com/...",
    "https://www.filmfare.com/..."
  ]
}
```

### Example 2: Technology Search

**Request:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence trends 2024"}'
```

**Response:**
```json
{
  "title": "AI Trends in 2024",
  "summary": "2024 marks a significant year for artificial intelligence with major advancements in large language models, multimodal AI, and enterprise adoption. Key trends include improved efficiency, reduced costs, and increased focus on AI safety and ethics. Organizations are moving beyond experimentation to production deployments.",
  "key_points": [
    "Large language models becoming more efficient",
    "Multimodal AI gaining mainstream adoption",
    "Enterprise AI implementations increasing",
    "Focus on AI safety and ethical considerations",
    "Cost reduction in AI infrastructure"
  ],
  "important_details": [
    "GPT-4 and similar models showing improved performance",
    "Open-source models gaining traction",
    "Regulatory frameworks being developed",
    "AI talent shortage remains a challenge",
    "Investment in AI continues to grow"
  ],
  "sources": [
    "https://www.techcrunch.com/...",
    "https://www.forbes.com/...",
    "https://www.gartner.com/...",
    "https://www.mckinsey.com/...",
    "https://www.wired.com/..."
  ]
}
```

### Example 3: Health/Medical Search

**Request:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "benefits of regular exercise"}'
```

**Response:**
```json
{
  "title": "Health Benefits of Regular Exercise",
  "summary": "Regular exercise provides numerous health benefits including improved cardiovascular health, weight management, mental health improvement, and increased longevity. Exercise strengthens muscles and bones, reduces risk of chronic diseases, and enhances overall quality of life.",
  "key_points": [
    "Improves cardiovascular health and reduces heart disease risk",
    "Aids in weight management and metabolism",
    "Enhances mental health and reduces depression/anxiety",
    "Strengthens muscles and bones",
    "Increases energy levels and improves sleep quality"
  ],
  "important_details": [
    "Recommended 150 minutes of moderate exercise per week",
    "Reduces risk of type 2 diabetes by 50%",
    "Improves cognitive function and memory",
    "Boosts immune system function",
    "Can add years to life expectancy"
  ],
  "sources": [
    "https://www.healthline.com/...",
    "https://www.mayoclinic.org/...",
    "https://www.cdc.gov/...",
    "https://www.who.int/...",
    "https://www.ncbi.nlm.nih.gov/..."
  ]
}
```

## Integration Examples

### React Component

```javascript
import { useState } from 'react'
import axios from 'axios'

export default function SearchComponent() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(
        'http://localhost:8000/search',
        { query }
      )
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search query"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h1>{result.title}</h1>
          <p>{result.summary}</p>
          <h3>Key Points:</h3>
          <ul>
            {result.key_points.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
```

### Python Script

```python
import requests
import json
from typing import Dict

class WebScraperClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def search(self, query: str) -> Dict:
        """Search and get summarized results"""
        response = requests.post(
            f"{self.base_url}/search",
            json={"query": query},
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def health_check(self) -> bool:
        """Check if API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

# Usage
client = WebScraperClient()

# Check health
if client.health_check():
    print("API is running!")

# Search
result = client.search("Dhurandhar 2")
print(json.dumps(result, indent=2))
```

### Node.js Script

```javascript
const axios = require('axios')

class WebScraperClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl
    this.client = axios.create({ baseURL: baseUrl })
  }

  async search(query) {
    const response = await this.client.post('/search', { query })
    return response.data
  }

  async healthCheck() {
    try {
      const response = await this.client.get('/health')
      return response.status === 200
    } catch {
      return false
    }
  }
}

// Usage
const client = new WebScraperClient()

;(async () => {
  const isHealthy = await client.healthCheck()
  console.log('API healthy:', isHealthy)

  const result = await client.search('Dhurandhar 2')
  console.log(JSON.stringify(result, null, 2))
})()
```

## Error Handling

### Handling Different Error Types

```python
import requests
from requests.exceptions import Timeout, ConnectionError

try:
    response = requests.post(
        "http://localhost:8000/search",
        json={"query": "test"},
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
except Timeout:
    print("Request timed out")
except ConnectionError:
    print("Could not connect to API")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid query")
    elif e.response.status_code == 404:
        print("No results found")
    elif e.response.status_code == 500:
        print("Server error")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Rate Limiting & Best Practices

1. **Implement Caching**
   ```python
   cache = {}
   
   def search_with_cache(query):
       if query in cache:
           return cache[query]
       result = client.search(query)
       cache[query] = result
       return result
   ```

2. **Add Retry Logic**
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential
   
   @retry(stop=stop_after_attempt(3), wait=wait_exponential())
   def search_with_retry(query):
       return client.search(query)
   ```

3. **Batch Processing**
   ```python
   queries = ["query1", "query2", "query3"]
   results = [client.search(q) for q in queries]
   ```

## Testing the API

### Using Postman

1. Create new POST request
2. URL: `http://localhost:8000/search`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "query": "your search query"
   }
   ```
5. Click Send

### Using Thunder Client (VS Code)

1. Install Thunder Client extension
2. Create new request
3. Method: POST
4. URL: `http://localhost:8000/search`
5. Body: `{"query": "your search query"}`
6. Send

## Performance Tips

- Keep queries between 2-100 characters
- Implement client-side caching
- Use connection pooling for multiple requests
- Set appropriate timeouts (30-60 seconds)
- Monitor API response times

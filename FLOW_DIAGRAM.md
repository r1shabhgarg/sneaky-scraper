# System Flow Diagrams

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Frontend (Next.js + React + Tailwind)                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  SearchBar Component                                │  │  │
│  │  │  - Input field                                      │  │  │
│  │  │  - Search button                                    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  LoadingSpinner Component                           │  │  │
│  │  │  - Shows while processing                           │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  ResultCard Component                               │  │  │
│  │  │  - Title                                            │  │  │
│  │  │  - Summary                                          │  │  │
│  │  │  - Key Points                                       │  │  │
│  │  │  - Important Details                                │  │  │
│  │  │  - Sources                                          │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ↕ (HTTP/REST)
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER (FastAPI)                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  POST /search Endpoint                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  1. Search Layer (search.py)                        │  │  │
│  │  │     - Brave Search API                              │  │  │
│  │  │     - Returns 8 URLs                                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  2. Scraping Layer (scraper.py)                     │  │  │
│  │  │     - Parallel scraping (asyncio)                   │  │  │
│  │  │     - BeautifulSoup parsing                         │  │  │
│  │  │     - Content extraction                            │  │  │
│  │  │     - 8 concurrent requests                         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  3. Data Processing                                 │  │  │
│  │  │     - Combine content                               │  │  │
│  │  │     - Remove duplicates                             │  │  │
│  │  │     - Clean text                                    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  4. AI Processing (ai.py)                           │  │  │
│  │  │     - NVIDIA API                                    │  │  │
│  │  │     - Summarization                                 │  │  │
│  │  │     - Structuring                                   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                        ↓                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  5. Response Formatting                             │  │  │
│  │  │     - JSON structure                                │  │  │
│  │  │     - Add sources                                   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─────────┐         ┌──────────┐
    │  Brave  │          │ Website │         │ NVIDIA   │
    │ Search  │          │  URLs   │         │   API    │
    │   API   │          │ (Scrape)│         │  (AI)    │
    └─────────┘          └─────────┘         └──────────┘
```

## 2. Request/Response Flow

```
USER INTERACTION
    ↓
┌─────────────────────────────────────────┐
│ User enters query: "Dhurandhar 2"       │
│ Clicks "Search" button                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Frontend sends POST /search              │
│ {                                        │
│   "query": "Dhurandhar 2"               │
│ }                                        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Backend receives request                 │
│ Validates query (min 2 chars)           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ SEARCH PHASE (~1-2 seconds)             │
│ Brave Search API                        │
│ Returns: [URL1, URL2, ..., URL8]       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ SCRAPING PHASE (~8-10 seconds)          │
│ Parallel scrape all URLs                │
│ Extract content from each               │
│ Combine into single text                │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ AI PROCESSING PHASE (~5-10 seconds)     │
│ Send combined text to NVIDIA API        │
│ Receive structured JSON                 │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Backend sends response                   │
│ {                                        │
│   "title": "...",                       │
│   "summary": "...",                     │
│   "key_points": [...],                  │
│   "important_details": [...],           │
│   "sources": [...]                      │
│ }                                        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Frontend receives response               │
│ Displays results                        │
│ Shows loading spinner during process    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ USER SEES RESULTS                       │
│ - Title                                 │
│ - Summary                               │
│ - Key Points (bullets)                  │
│ - Important Details (checkmarks)        │
│ - Source Links                          │
└─────────────────────────────────────────┘
```

## 3. Scraping Process (Parallel)

```
SCRAPING LAYER - PARALLEL EXECUTION

Start: 8 URLs to scrape
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Async Task Pool (asyncio)                                   │
│                                                              │
│  URL1 ──→ Fetch ──→ Parse ──→ Extract ──→ Content1         │
│  URL2 ──→ Fetch ──→ Parse ──→ Extract ──→ Content2         │
│  URL3 ──→ Fetch ──→ Parse ──→ Extract ──→ Content3         │
│  URL4 ──→ Fetch ──→ Parse ──→ Extract ──→ Content4         │
│  URL5 ──→ Fetch ──→ Parse ──→ Extract ──→ Content5         │
│  URL6 ──→ Fetch ──→ Parse ──→ Extract ──→ Content6         │
│  URL7 ──→ Fetch ──→ Parse ──→ Extract ──→ Content7         │
│  URL8 ──→ Fetch ──→ Parse ──→ Extract ──→ Content8         │
│                                                              │
│  (All running concurrently, 8-second timeout each)         │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Combine Results                                              │
│ Content1 + Content2 + ... + Content8 = Combined Text       │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Clean & Process                                              │
│ - Remove duplicates                                         │
│ - Remove scripts/styles                                     │
│ - Limit to 5000 chars per site                             │
│ - Prepare for AI                                            │
└─────────────────────────────────────────────────────────────┘
```

## 4. AI Processing Pipeline

```
AI PROCESSING LAYER

Input: Combined scraped text
    ↓
┌─────────────────────────────────────────┐
│ Build Prompt                             │
│ - User query                             │
│ - Scraped data                           │
│ - Instructions                           │
│ - Output format (JSON)                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Send to NVIDIA API                       │
│ - Model: llama-2-70b-chat               │
│ - Temperature: 0.7                       │
│ - Max tokens: 1024                       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Receive Response                         │
│ {                                        │
│   "title": "...",                       │
│   "summary": "...",                     │
│   "key_points": [...],                  │
│   "important_details": [...]            │
│ }                                        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Parse & Validate                         │
│ - Extract JSON                           │
│ - Validate structure                     │
│ - Handle errors                          │
└─────────────────────────────────────────┘
    ↓
Output: Structured JSON response
```

## 5. Error Handling Flow

```
ERROR HANDLING STRATEGY

┌─────────────────────────────────────────┐
│ Search API Error                         │
│ ↓                                        │
│ Fallback to mock search results         │
│ Continue with mock URLs                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Scraping Error (per URL)                 │
│ ↓                                        │
│ Skip failed URL                          │
│ Continue with other URLs                │
│ (Timeout after 8 seconds)               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ AI Processing Error                      │
│ ↓                                        │
│ Fallback to mock processing             │
│ Return basic structure                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Network Error                            │
│ ↓                                        │
│ Retry with exponential backoff          │
│ Or return error to user                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Invalid Input                            │
│ ↓                                        │
│ Return 400 Bad Request                  │
│ With error message                      │
└─────────────────────────────────────────┘
```

## 6. Frontend Component Hierarchy

```
App (pages/index.js)
├── Header
│   └── Title & Description
├── Main Content
│   ├── SearchBar Component
│   │   ├── Input Field
│   │   └── Search Button
│   ├── LoadingSpinner Component (conditional)
│   │   ├── Spinner Animation
│   │   └── Status Messages
│   ├── Error Display (conditional)
│   │   └── Error Message
│   ├── ResultCard Component (conditional)
│   │   ├── Title
│   │   ├── Summary
│   │   ├── Key Points List
│   │   ├── Important Details List
│   │   └── Sources List
│   └── Empty State (conditional)
│       └── Welcome Message
└── Footer
    └── Copyright
```

## 7. Data Structure Flow

```
SEARCH QUERY
    ↓
    "Dhurandhar 2"
    ↓
SEARCH RESULTS
    ↓
    [
      { url: "...", title: "...", description: "..." },
      { url: "...", title: "...", description: "..." },
      ...
    ]
    ↓
SCRAPED CONTENT
    ↓
    [
      { url: "...", title: "...", content: "..." },
      { url: "...", title: "...", content: "..." },
      ...
    ]
    ↓
COMBINED TEXT
    ↓
    "Source: URL1\nTitle: ...\nContent: ...\n\nSource: URL2\n..."
    ↓
AI PROCESSED RESULT
    ↓
    {
      "title": "...",
      "summary": "...",
      "key_points": ["...", "...", "..."],
      "important_details": ["...", "..."]
    }
    ↓
FINAL RESPONSE
    ↓
    {
      "title": "...",
      "summary": "...",
      "key_points": [...],
      "important_details": [...],
      "sources": ["url1", "url2", ...]
    }
```

## 8. Deployment Architecture

```
DEVELOPMENT
    ↓
┌─────────────────────────────────────────┐
│ Local Machine                            │
│ ├─ Backend (localhost:8000)             │
│ └─ Frontend (localhost:3000)            │
└─────────────────────────────────────────┘

DOCKER
    ↓
┌─────────────────────────────────────────┐
│ Docker Compose                           │
│ ├─ Backend Container (port 8000)        │
│ └─ Frontend Container (port 3000)       │
└─────────────────────────────────────────┘

PRODUCTION
    ↓
┌─────────────────────────────────────────┐
│ Cloud Infrastructure                     │
│ ├─ Backend Service (Heroku/Railway)     │
│ │  ├─ Multiple instances                │
│ │  └─ Load balancer                     │
│ ├─ Frontend Service (Vercel/Netlify)    │
│ │  └─ CDN distribution                  │
│ └─ Optional Services                    │
│    ├─ Redis cache                       │
│    └─ Database                          │
└─────────────────────────────────────────┘
```

## 9. Performance Timeline

```
USER INITIATES SEARCH
    ↓ (0ms)
┌─────────────────────────────────────────┐
│ Frontend sends request                   │
│ Time: 0-100ms                            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Backend receives & validates             │
│ Time: 100-200ms                          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Search API call                          │
│ Time: 200-2500ms (1-2 seconds)          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Parallel scraping (8 URLs)               │
│ Time: 2500-12500ms (8-10 seconds)       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ AI processing                            │
│ Time: 12500-22500ms (5-10 seconds)      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Response sent to frontend                │
│ Time: 22500-22600ms                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Frontend displays results                │
│ Time: 22600-22700ms                      │
└─────────────────────────────────────────┘
    ↓
TOTAL TIME: ~15-30 seconds
```

---

These diagrams show the complete flow of the system from user input to final output.

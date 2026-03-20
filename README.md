# Web Scraper & Summarizer - Full Stack AI Tool

A production-ready full-stack application that searches the web, scrapes multiple websites, and uses AI to generate structured summaries.

## 🎯 Features

- **Web Search**: Integrates with Tavily Search API to find relevant URLs
- **Parallel Scraping**: Efficiently scrapes 5-10 websites concurrently
- **AI Summarization**: Uses NVIDIA API to generate structured summaries
- **Deduplication**: Removes duplicate and redundant information
- **Modern UI**: Clean, responsive Next.js frontend with Tailwind CSS
- **Error Handling**: Graceful fallbacks and error management
- **Production Ready**: Modular, scalable architecture

## 🏗️ Architecture

```
web-scraper-summarizer/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── search.py         # Search API integration
│   ├── scraper.py        # Web scraping logic
│   ├── ai.py             # AI processing
│   ├── requirements.txt   # Python dependencies
│   └── .env.example      # Environment variables template
└── frontend/
    ├── pages/
    │   ├── index.js      # Main page
    │   └── _app.js       # App wrapper
    ├── components/
    │   ├── SearchBar.js  # Search input component
    │   ├── ResultCard.js # Results display
    │   └── LoadingSpinner.js
    ├── styles/
    │   └── globals.css   # Tailwind styles
    ├── package.json
    ├── next.config.js
    ├── tailwind.config.js
    └── .env.local.example
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- API Keys:
  - NVIDIA API Key (for summarization)
  - Tavily API Key (for web search)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your API keys to `.env`:
```
NVIDIA_API_KEY=your_key_here
BRAVE_SEARCH_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:3000
```

6. Run the server:
```bash
python main.py
```

Server runs on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
cp .env.local.example .env.local
```

4. Run development server:
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

## 📝 API Documentation

### POST /search

Search, scrape, and summarize web content.

**Request:**
```json
{
  "query": "Dhurandhar 2"
}
```

**Response:**
```json
{
  "title": "Summary Title",
  "summary": "Comprehensive summary of findings...",
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "important_details": [
    "Detail 1",
    "Detail 2"
  ],
  "sources": [
    "https://example1.com",
    "https://example2.com"
  ]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
- `NVIDIA_API_KEY`: Your NVIDIA API key for AI processing
- `BRAVE_SEARCH_API_KEY`: Your Brave Search API key
- `CORS_ORIGINS`: Comma-separated list of allowed origins

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## 🎨 Features Explained

### 1. Search Layer
- Uses Brave Search API to find relevant URLs
- Fallback to mock data if API unavailable
- Extracts 8 URLs per query

### 2. Scraping Layer
- Parallel scraping using asyncio
- Removes scripts, styles, and navigation elements
- Extracts meaningful content (headings, paragraphs)
- 8-second timeout per URL
- 5000 character limit per site

### 3. AI Processing
- Sends combined content to NVIDIA API
- Removes duplicates and merges information
- Generates structured JSON output
- Fallback to mock processing if API unavailable

### 4. Frontend
- Responsive design with Tailwind CSS
- Real-time loading indicators
- Error handling and display
- Source attribution
- Mobile-friendly interface

## 🔐 Security Considerations

- User-Agent headers to avoid blocking
- Timeout handling for slow sites
- Content length limits to prevent overload
- CORS configuration for frontend
- Environment variables for sensitive data
- Input validation on all endpoints

## 📊 Performance

- **Parallel Scraping**: 8 concurrent requests
- **Timeout**: 8 seconds per URL
- **Content Limit**: 5000 characters per site
- **API Timeout**: 30 seconds for AI processing
- **Total Time**: ~15-30 seconds for full pipeline

## 🐛 Error Handling

- Graceful fallbacks for API failures
- Mock data for testing without API keys
- Detailed error messages
- Timeout handling
- Invalid URL filtering

## 🚀 Deployment

### Backend (Heroku/Railway)

```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
git push heroku main
```

### Frontend (Vercel)

```bash
# Deploy with Vercel CLI
vercel

# Or connect GitHub repo to Vercel dashboard
```

## 📦 Dependencies

**Backend:**
- FastAPI: Web framework
- Uvicorn: ASGI server
- Requests: HTTP client
- BeautifulSoup4: HTML parsing
- HTTPX: Async HTTP client
- Python-dotenv: Environment management

**Frontend:**
- Next.js: React framework
- Tailwind CSS: Styling
- Axios: HTTP client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project

## 🆘 Troubleshooting

**Backend won't start:**
- Check Python version (3.8+)
- Verify all dependencies installed
- Check port 8000 is available

**Frontend won't connect:**
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

**API errors:**
- Verify API keys are correct
- Check API rate limits
- Review error logs

**Scraping issues:**
- Some sites may block requests
- Check timeout settings
- Verify User-Agent headers

## 📞 Support

For issues or questions, please open an issue on GitHub.

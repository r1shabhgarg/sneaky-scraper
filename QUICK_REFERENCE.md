# Quick Reference Guide

## 🚀 Start in 3 Steps

### Step 1: Get API Keys
```
NVIDIA: https://build.nvidia.com/explore/discover
Brave Search: https://api.search.brave.com/
```

### Step 2: Setup
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Step 3: Run
```bash
# Option A: Automatic
./start.sh          # macOS/Linux
start.bat           # Windows

# Option B: Manual
# Terminal 1
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py

# Terminal 2
cd frontend && npm install && npm run dev
```

Then open: **http://localhost:3000**

---

## 📁 File Structure

```
backend/
  ├── main.py           # FastAPI app
  ├── search.py         # Search API
  ├── scraper.py        # Web scraping
  ├── ai.py             # AI processing
  ├── requirements.txt
  └── .env.example

frontend/
  ├── pages/index.js    # Main page
  ├── components/       # React components
  ├── styles/           # CSS
  ├── package.json
  └── .env.local.example

docs/
  ├── README.md         # Overview
  ├── SETUP.md          # Setup guide
  ├── ARCHITECTURE.md   # Design
  ├── API_EXAMPLES.md   # Examples
  └── FLOW_DIAGRAM.md   # Diagrams
```

---

## 🔌 API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Search
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your query"}'
```

### Response Format
```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "important_details": ["string"],
  "sources": ["url"]
}
```

---

## 🛠️ Common Commands

### Backend
```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python main.py

# Run on different port
python main.py --port 8001
```

### Frontend
```bash
# Setup
cd frontend
npm install

# Run
npm run dev

# Build
npm run build

# Start production
npm start
```

### Docker
```bash
# Start all services
docker-compose up

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build
```

---

## 🔑 Environment Variables

### Backend (.env)
```
NVIDIA_API_KEY=your_key
BRAVE_SEARCH_API_KEY=your_key
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `lsof -i :8000` then kill process |
| Port 3000 in use | `npm run dev -- -p 3001` |
| Module not found | `pip install -r requirements.txt` |
| API key error | Check .env file, verify keys are correct |
| CORS error | Check CORS_ORIGINS in .env |
| Can't connect | Verify backend running on 8000 |
| Slow scraping | Normal, takes 15-30 seconds |

---

## 📊 Performance

| Phase | Time |
|-------|------|
| Search | 1-2s |
| Scraping | 8-10s |
| AI Processing | 5-10s |
| **Total** | **15-30s** |

---

## 🔐 Security Checklist

- [ ] API keys in .env (not in code)
- [ ] CORS configured correctly
- [ ] Input validation enabled
- [ ] Timeouts set (8s per URL)
- [ ] Content limits enforced (5000 chars)
- [ ] Error messages don't leak info

---

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| README.md | Project overview |
| SETUP.md | Installation guide |
| ARCHITECTURE.md | System design |
| API_EXAMPLES.md | Code examples |
| FLOW_DIAGRAM.md | Visual flows |
| CHECKLIST.md | Requirements |
| QUICK_REFERENCE.md | This file |

---

## 🚢 Deployment

### Heroku (Backend)
```bash
heroku create your-app
git push heroku main
```

### Vercel (Frontend)
```bash
vercel
```

### Docker
```bash
docker-compose up -d
```

---

## 💡 Tips & Tricks

1. **Test without API keys**: Uses mock data
2. **Parallel scraping**: 8 concurrent requests
3. **Timeout handling**: 8 seconds per URL
4. **Error recovery**: Skips failed URLs
5. **Caching**: Add Redis for repeated queries
6. **Rate limiting**: Implement if needed
7. **Logging**: Check console for errors

---

## 🎯 Common Use Cases

### Search for Information
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning trends"}'
```

### Research Topic
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "climate change solutions"}'
```

### Find News
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "latest technology news"}'
```

---

## 🔄 Development Workflow

1. **Make changes** to code
2. **Backend auto-reloads** (if using uvicorn --reload)
3. **Frontend auto-reloads** (Next.js dev mode)
4. **Test in browser** at http://localhost:3000
5. **Check console** for errors
6. **Commit changes** to git

---

## 📦 Dependencies

### Backend
- FastAPI (web framework)
- Uvicorn (ASGI server)
- BeautifulSoup4 (HTML parsing)
- HTTPX (async HTTP)
- Requests (HTTP client)

### Frontend
- Next.js (React framework)
- Tailwind CSS (styling)
- Axios (HTTP client)

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [NVIDIA API](https://build.nvidia.com/)

---

## 🆘 Getting Help

1. Check **SETUP.md** for installation issues
2. Check **API_EXAMPLES.md** for usage questions
3. Check **ARCHITECTURE.md** for design questions
4. Check **FLOW_DIAGRAM.md** for flow questions
5. Review error logs in console

---

## ✨ Next Steps

- [ ] Get API keys
- [ ] Setup environment
- [ ] Run application
- [ ] Test search
- [ ] Customize UI
- [ ] Deploy to production
- [ ] Add features
- [ ] Monitor performance

---

## 🎉 You're Ready!

Everything is set up and documented. Start with Step 1 above and you'll be running in minutes.

**Happy scraping! 🚀**

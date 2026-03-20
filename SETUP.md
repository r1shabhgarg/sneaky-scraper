# Setup Guide

## Getting API Keys

### 1. NVIDIA API Key

1. Go to [NVIDIA API Catalog](https://build.nvidia.com/explore/discover)
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy and save it

### 2. Tavily Search API Key

1. Go to [Tavily Search API](https://tavily.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy and save it

## Local Development Setup

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd web-scraper-summarizer
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
# NVIDIA_API_KEY=your_key
# TAVILY_API_KEY=your_key

# Run backend
python main.py
```

Backend will be available at: `http://localhost:8000`

### Step 3: Frontend Setup (in new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.local.example .env.local

# Run frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Run with Docker

```bash
# Create .env file with your API keys
cp .env.example .env
# Edit .env and add your keys

# Start services
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Testing the Application

1. Open `http://localhost:3000` in your browser
2. Enter a search query (e.g., "Dhurandhar 2")
3. Click "Search"
4. Wait for results (15-30 seconds)
5. View the summarized results with sources

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
python main.py --port 8001
```

**Module not found errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**API key errors:**
- Verify keys are correct in `.env`
- Check API key permissions
- Ensure API keys are not expired

### Frontend Issues

**Port 3000 already in use:**
```bash
npm run dev -- -p 3001
```

**Cannot connect to backend:**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

**Dependencies issues:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment

### Backend (Heroku)

```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| NVIDIA_API_KEY | NVIDIA API key for AI | nvapi-xxx |
| BRAVE_SEARCH_API_KEY | Brave Search API key | brav-xxx |
| CORS_ORIGINS | Allowed CORS origins | http://localhost:3000 |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | http://localhost:8000 |

## Performance Tips

1. **Caching**: Consider adding Redis for caching search results
2. **Rate Limiting**: Implement rate limiting on backend
3. **Database**: Add PostgreSQL for storing search history
4. **CDN**: Use CDN for frontend assets in production
5. **Monitoring**: Add error tracking (Sentry)

## Next Steps

- Add user authentication
- Implement search history
- Add advanced filtering options
- Create admin dashboard
- Add more AI models
- Implement caching layer

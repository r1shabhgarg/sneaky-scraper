import { useState } from 'react'
import axios from 'axios'
import SearchBar from '../components/SearchBar'
import ResultCard from '../components/ResultCard'
import LoadingSpinner from '../components/LoadingSpinner'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastQuery, setLastQuery] = useState('')

  const handleSearch = async (query) => {
    setIsLoading(true)
    setError(null)
    setLastQuery(query)

    try {
      const response = await axios.post(`${API_BASE_URL}/search`, {
        query: query
      }, {
        timeout: 60000
      })

      setResult(response.data)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred'
      setError(errorMessage)
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Web Scraper & Summarizer</h1>
          <p className="text-gray-600 mt-1">Search, scrape, and summarize web content with AI</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Loading State */}
        {isLoading && <LoadingSpinner />}

        {/* Error State */}
        {error && !isLoading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <p className="text-red-800 font-medium">Error</p>
            <p className="text-red-700 text-sm mt-1">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && !isLoading && (
          <div className="space-y-4">
            <div className="text-sm text-gray-600">
              Results for: <span className="font-semibold text-gray-900">"{lastQuery}"</span>
            </div>
            <ResultCard result={result} />
          </div>
        )}

        {/* Empty State */}
        {!result && !isLoading && !error && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Start Searching</h2>
            <p className="text-gray-600">Enter a query above to search and summarize web content</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-6xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>Web Scraper & Summarizer • Powered by AI</p>
        </div>
      </footer>
    </div>
  )
}

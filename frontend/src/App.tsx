import { useState } from 'react'
import { VideoCameraIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface GeneratedVideo {
  prompt: string
  url: string
  timestamp: number
}

function App() {
  const [prompt, setPrompt] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [generatedVideos, setGeneratedVideos] = useState<GeneratedVideo[]>([])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setIsLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_URL}/api/generate-video`, {
        prompt: prompt.trim()
      })

      if (response.data.videoUrl) {
        setGeneratedVideos(prev => [{
          prompt: prompt.trim(),
          url: response.data.videoUrl,
          timestamp: Date.now()
        }, ...prev])
        setPrompt('')
      } else {
        throw new Error('No video URL in response')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate video')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center">
          <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto">
            <VideoCameraIcon className="h-8 w-8 text-white" />
          </div>
          <h1 className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            AI Video Generator
          </h1>
          <p className="mt-2 text-lg text-gray-400">
            Transform your ideas into stunning videos using AI
          </p>
        </div>

        {/* Form */}
        <div className="mt-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="bg-gray-800 rounded-lg p-4 shadow-lg">
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-300 mb-2">
                Describe your video
              </label>
              <textarea
                id="prompt"
                rows={3}
                className="w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="A cinematic shot of a futuristic city at sunset..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !prompt.trim()}
              className="w-full flex justify-center items-center py-3 px-4 rounded-md bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Generating...
                </>
              ) : (
                'Generate Video'
              )}
            </button>
          </form>

          {/* Error Message */}
          {error && (
            <div className="mt-4 bg-red-900/50 border border-red-500 rounded-md p-4">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          {/* Generated Videos */}
          {generatedVideos.length > 0 && (
            <div className="mt-12 space-y-8">
              <h2 className="text-xl font-semibold text-gray-200">Generated Videos</h2>
              {generatedVideos.map((video) => (
                <div key={video.timestamp} className="bg-gray-800 rounded-lg overflow-hidden shadow-lg">
                  <div className="p-4">
                    <p className="text-sm text-gray-400">
                      Generated {new Date(video.timestamp).toLocaleString()}
                    </p>
                    <p className="mt-1 text-sm text-gray-300">
                      Prompt: "{video.prompt}"
                    </p>
                  </div>
                  <div className="aspect-video bg-gray-900">
                    <video
                      className="w-full h-full object-contain"
                      controls
                      src={video.url}
                      poster="/video-placeholder.png"
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
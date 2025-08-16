# AI Video Generator

Transform your ideas into stunning videos using AI. This web application allows users to generate videos from text descriptions using advanced AI models.

## Live Demo

- Frontend: [https://ai-video-generator-six-delta.vercel.app](https://ai-video-generator-six-delta.vercel.app)
- Backend API: [https://ai-video-generator-vtqv.vercel.app](https://ai-video-generator-vtqv.vercel.app)

## Features

- Text-to-video generation using AI
- Real-time video generation status
- Modern, responsive UI with dark mode
- Video history display
- Error handling and loading states
- Prompt enhancement using AI

## Tech Stack

### Frontend
- React with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Axios for API communication
- Heroicons for icons

### Backend
- FastAPI (Python)
- OpenRouter API (Qwen 2.5) for prompt enhancement
- Replicate API (Zeroscope v2 XL) for video generation
- Custom error handling and logging
- Environment variable configuration

## Video Generation

The application uses two AI models in sequence:
1. **Qwen 2.5** (via OpenRouter) enhances user prompts by adding cinematic details
2. **Zeroscope v2 XL** (via Replicate) generates the video with parameters:
   - Resolution: 576x320
   - Frame rate: 12 FPS
   - Duration: 24 frames (~2 seconds)
   - Quality: 50 inference steps
   - Guidance scale: 12.5 for better prompt adherence

## Local Development

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- API keys:
  - OpenRouter API key for prompt enhancement
  - Replicate API token for video generation

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Environment Variables

Frontend (.env):
```
VITE_API_URL=http://localhost:8000
```

Backend (.env):
```
OPENROUTER_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_token_here
CORS_ORIGINS=http://localhost:5173
```

## Deployment

The application is deployed on Vercel:

1. Frontend:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables: Set `VITE_API_URL` to backend URL

2. Backend:
   - Framework: Python
   - Build Command: None (uses vercel.json)
   - Environment Variables: Set API keys and CORS origins

## API Endpoints

- `GET /`: Health check endpoint
- `POST /api/generate-video`: Generate video from text prompt
  - Request body: `{ "prompt": "string" }`
  - Response: `{ "videoUrl": "string", "generationDetails": "string" }`

## Security Considerations

- API keys are stored securely in environment variables
- CORS is configured to allow only specific origins
- Input validation on both frontend and backend
- Error handling for failed API calls
- Detailed error logging for troubleshooting

## Usage Tips

1. **Effective Prompts**:
   - Be specific about visual elements
   - Include details about lighting and atmosphere
   - Mention camera angles or movements
   - Example: "A cinematic beach sunset with golden light reflecting off gentle waves"

2. **Generation Time**:
   - Video generation typically takes 30-60 seconds
   - The AI enhances your prompt first
   - Progress is shown in the UI

3. **Video Quality**:
   - Videos are optimized for web viewing
   - Square aspect ratio for compatibility
   - Short duration for quick generation
   - High-quality settings for best results
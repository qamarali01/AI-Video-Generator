# AI Video Generator

Transform your ideas into stunning videos using AI. This web application allows users to generate videos from text descriptions using advanced AI models.

## Live Demo

- Frontend: [https://ai-video-generator-six-delta.vercel.app](https://ai-video-generator-six-delta.vercel.app)
- Backend API: [https://ai-video-generator-vtqv.vercel.app](https://ai-video-generator-vtqv.vercel.app)

## Features

- Text-to-video generation using AI
- Real-time video generation status
- Modern, responsive UI
- Video history display
- Error handling and loading states

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
- Replicate API (Deforum Stable Diffusion) for video generation
- Custom CORS middleware
- Environment variable configuration

## Local Development

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- API keys for OpenRouter and Replicate

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

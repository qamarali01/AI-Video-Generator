# AI Video Generation Web App

This web application generates short videos based on text prompts using AI technology. It provides a simple interface for users to input their creative ideas and receive AI-generated videos in response.

## Features

- Text-to-video generation using AI
- Modern, responsive web interface
- Real-time generation status updates
- Secure API key handling
- Cloud deployment

## Tech Stack

- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI (Python)
- AI Provider: Pika Labs
- Deployment: Vercel

## Project Structure

```
peppo/
├── frontend/           # React frontend application
├── backend/           # FastAPI backend server
├── .env.example       # Example environment variables
├── README.md         # Project documentation
└── .gitignore       # Git ignore rules
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- pnpm (recommended) or npm

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd peppo
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. Frontend setup:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

4. Backend setup:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Backend
PIKA_API_KEY=your_pika_api_key
CORS_ORIGINS=http://localhost:5173

# Frontend
VITE_API_URL=http://localhost:8000
```

## API Documentation

The backend API provides the following endpoints:

- `POST /api/generate-video`
  - Generates a video from a text prompt
  - Request body: `{ "prompt": "string" }`
  - Returns: Video URL or generation status

## Deployment

This application is deployed using Vercel. Follow these steps for deployment:

1. Frontend deployment:
   - Connect your GitHub repository to Vercel
   - Configure build settings and environment variables
   - Deploy

2. Backend deployment:
   - Use Vercel's Python runtime
   - Configure environment variables
   - Deploy

## Security

- API keys are stored securely using environment variables
- CORS is configured to allow only specific origins
- Rate limiting is implemented to prevent abuse

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

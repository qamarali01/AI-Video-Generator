from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Video Generation API")

# Configure CORS
# CORS headers are handled directly in the routes

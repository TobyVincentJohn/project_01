from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, posts
from app.core.config import settings

app = FastAPI(title="My App", version="0.115.12")

# Allow requests from frontend origin (e.g. http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_router
#from app.core.config import settings

app = FastAPI(
    title="My App",
    version="0.115.12",
    description="API for managing agents and other resources"
)

# Allow requests from frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")



@app.get("/")
async def root():
    return {
        "message": "Welcome to the API",
        "docs_url": "/docs",
        "version": "0.115.12"
    }
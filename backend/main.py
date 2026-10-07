from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import database.models
from database.db import Base, engine

from auth.gmail_oauth import router as auth_router
from mail.fetcher import router as email_router
from briefing.generator import router as briefing_router

# Load environment variables
load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MailBrief API",
    description="Backend API for MailBrief: Your personal email intelligence system.",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(email_router)
app.include_router(briefing_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Serve the frontend statically
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

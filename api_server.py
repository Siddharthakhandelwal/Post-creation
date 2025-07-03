from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from main import generate_doctor_post

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Doctor Post Agent API",
    description="AI-Powered Social Media Content Generator for Healthcare Professionals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Doctor Post Agent API"

@app.post("/post")
def generate_post():
    try:
        post = generate_doctor_post()
        return {"post": post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

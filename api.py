from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Import the main application logic
from main import (
    fetch_latest_news,
    generate_caption,
    generate_image,
    CATEGORIES,
    MONSTER_API_KEY,
    GROQ_API_KEY,
    NEWS_API_KEY
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Doctor Post Agent API",
    description="AI-Powered Social Media Content Generator for Healthcare Professionals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class PostGenerationRequest(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="News category to fetch. If not provided, a random category will be selected.",
        example="health"
    )
    custom_prompt: Optional[str] = Field(
        default=None,
        description="Custom prompt for content generation",
        example="Focus on preventive care aspects"
    )

class ArticleData(BaseModel):
    title: str
    description: str
    url: str
    source: Optional[str] = None
    published_at: Optional[str] = None

class GeneratedContent(BaseModel):
    caption: str
    word_count: int
    hashtags: List[str]
    image_url: Optional[str] = None

class PostResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any]

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

# Global variables for tracking generation status
generation_status = {}

# Helper functions
def validate_api_keys():
    """Validate that all required API keys are present"""
    missing_keys = []
    if not MONSTER_API_KEY:
        missing_keys.append("MONSTER_API_KEY")
    if not GROQ_API_KEY:
        missing_keys.append("GROQ_API_KEY")
    if not NEWS_API_KEY:
        missing_keys.append("NEWS_API_KEY")
    
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )

def extract_hashtags(caption: str) -> List[str]:
    """Extract hashtags from generated caption"""
    import re
    hashtags = re.findall(r'#\w+', caption)
    return hashtags

async def generate_post_async(category: Optional[str] = None, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
    """Async wrapper for post generation"""
    try:
        # Validate API keys
        validate_api_keys()
        
        # Select category
        import random
        selected_category = category if category and category in CATEGORIES else random.choice(CATEGORIES)
        
        logger.info(f"Generating post for category: {selected_category}")
        
        # Fetch news
        news_article = fetch_latest_news(selected_category)
        if not news_article:
            raise HTTPException(status_code=404, detail="No news articles found for the selected category")
        
        # Prepare article data
        article_data = ArticleData(
            title=news_article.get('title', ''),
            description=news_article.get('description', ''),
            url=news_article.get('url', ''),
            source=news_article.get('source', {}).get('name', ''),
            published_at=news_article.get('publishedAt', '')
        )
        
        # Generate caption
        caption_prompt = f"""
        You are a creative Instagram content writer for a doctor. Write an engaging, 
        informative, and emotional Instagram Post for the following news. Use emojis, 
        2-3 relevant hashtags, and keep it under 200 words.
        
        {custom_prompt if custom_prompt else ""}

        Title: {article_data.title}
        Description: {article_data.description}
        Link: {article_data.url}
        """
        
        context = "You are an expert social media content creator for a doctor."
        generated_caption = generate_caption(caption_prompt, context)
        
        if not generated_caption or generated_caption == "Unable to generate caption.":
            raise HTTPException(status_code=500, detail="Failed to generate caption")
        
        # Extract hashtags and count words
        hashtags = extract_hashtags(generated_caption)
        word_count = len(generated_caption.split())
        
        # Generate image
        image_prompt_request = f"Create an Instagram-style image based on the article: {article_data.title} - {article_data.description}"
        image_url = generate_image(image_prompt_request)
        
        # Prepare response data
        content = GeneratedContent(
            caption=generated_caption,
            word_count=word_count,
            hashtags=hashtags,
            image_url=image_url
        )
        
        return {
            "article": article_data.dict(),
            "content": content.dict(),
            "generation_info": {
                "category": selected_category,
                "timestamp": datetime.now().isoformat(),
                "custom_prompt_used": bool(custom_prompt)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# API Routes

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "Doctor Post Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        validate_api_keys()
        services_status = "healthy"
    except HTTPException:
        services_status = "unhealthy - missing API keys"
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services={
            "api_keys": services_status,
            "news_api": "configured" if NEWS_API_KEY else "missing",
            "groq_api": "configured" if GROQ_API_KEY else "missing",
            "monster_api": "configured" if MONSTER_API_KEY else "missing"
        }
    )

@app.get("/categories", response_model=List[str])
async def get_categories():
    """Get available news categories"""
    return CATEGORIES

@app.post("/generate", response_model=PostResponse)
async def generate_post(request: PostGenerationRequest):
    """Generate a complete social media post"""
    try:
        # Generate unique task ID
        import uuid
        task_id = str(uuid.uuid4())
        
        # Update generation status
        generation_status[task_id] = {
            "status": "processing",
            "started_at": datetime.now().isoformat()
        }
        
        # Generate post
        result = await generate_post_async(request.category, request.custom_prompt)
        
        # Update status
        generation_status[task_id] = {
            "status": "completed",
            "started_at": generation_status[task_id]["started_at"],
            "completed_at": datetime.now().isoformat()
        }
        
        return PostResponse(
            success=True,
            data=result,
            metadata={
                "task_id": task_id,
                "processing_time": "calculated_in_production",
                "api_version": "1.0.0"
            }
        )
        
    except HTTPException as e:
        return PostResponse(
            success=False,
            error=e.detail,
            metadata={
                "error_code": e.status_code,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return PostResponse(
            success=False,
            error="Internal server error",
            metadata={
                "error_code": 500,
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-async", response_model=Dict[str, str])
async def generate_post_async_endpoint(request: PostGenerationRequest, background_tasks: BackgroundTasks):
    """Start asynchronous post generation"""
    import uuid
    task_id = str(uuid.uuid4())
    
    # Initialize status
    generation_status[task_id] = {
        "status": "queued",
        "started_at": datetime.now().isoformat()
    }
    
    # Add background task
    background_tasks.add_task(
        process_generation_task,
        task_id,
        request.category,
        request.custom_prompt
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "check_status_url": f"/status/{task_id}"
    }

@app.get("/status/{task_id}", response_model=Dict[str, Any])
async def get_generation_status(task_id: str):
    """Get the status of an asynchronous generation task"""
    if task_id not in generation_status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return generation_status[task_id]

async def process_generation_task(task_id: str, category: Optional[str], custom_prompt: Optional[str]):
    """Background task for processing post generation"""
    try:
        generation_status[task_id]["status"] = "processing"
        
        result = await generate_post_async(category, custom_prompt)
        
        generation_status[task_id].update({
            "status": "completed",
            "result": result,
            "completed_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        generation_status[task_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })

@app.get("/news/{category}", response_model=Dict[str, Any])
async def get_news_by_category(category: str):
    """Get latest news for a specific category"""
    if category not in CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Available categories: {', '.join(CATEGORIES)}"
        )
    
    try:
        validate_api_keys()
        news_article = fetch_latest_news(category)
        
        if not news_article:
            raise HTTPException(status_code=404, detail="No news articles found")
        
        return {
            "category": category,
            "article": {
                "title": news_article.get('title', ''),
                "description": news_article.get('description', ''),
                "url": news_article.get('url', ''),
                "source": news_article.get('source', {}).get('name', ''),
                "published_at": news_article.get('publishedAt', '')
            },
            "fetched_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")

@app.post("/caption", response_model=Dict[str, Any])
async def generate_caption_only(
    title: str = Field(..., description="Article title"),
    description: str = Field(..., description="Article description"),
    url: str = Field(..., description="Article URL"),
    custom_prompt: Optional[str] = Field(None, description="Custom prompt")
):
    """Generate only the caption for given article data"""
    try:
        validate_api_keys()
        
        caption_prompt = f"""
        You are a creative Instagram content writer for a doctor. Write an engaging, 
        informative, and emotional Instagram Post for the following news. Use emojis, 
        2-3 relevant hashtags, and keep it under 200 words.
        
        {custom_prompt if custom_prompt else ""}

        Title: {title}
        Description: {description}
        Link: {url}
        """
        
        context = "You are an expert social media content creator for a doctor."
        generated_caption = generate_caption(caption_prompt, context)
        
        if not generated_caption or generated_caption == "Unable to generate caption.":
            raise HTTPException(status_code=500, detail="Failed to generate caption")
        
        hashtags = extract_hashtags(generated_caption)
        word_count = len(generated_caption.split())
        
        return {
            "caption": generated_caption,
            "word_count": word_count,
            "hashtags": hashtags,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate caption")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "metadata": {
                "path": str(request.url.path),
                "timestamp": datetime.now().isoformat()
            }
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "metadata": {
                "timestamp": datetime.now().isoformat()
            }
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Doctor Post Agent API starting up...")
    try:
        validate_api_keys()
        logger.info("API keys validated successfully")
    except HTTPException as e:
        logger.warning(f"API key validation failed: {e.detail}")
    logger.info("Doctor Post Agent API ready to serve requests")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Doctor Post Agent API shutting down...")

if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Run the application
    uvicorn.run(
        "api:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )

# Doctor Post Agent API Overview

## Purpose
This project is a social media content generator designed for healthcare professionals. It automatically creates engaging Instagram posts by combining news articles from specific categories (health, medical, environment) with AI-generated captions and images.

## How It Works
1. **News Fetching**: The app pulls recent news articles from the NewsAPI using predefined categories.
2. **Caption Generation**: A Groq API-powered AI writes captions that are:
   - Engaging and emotional
   - Include emojis
   - Have 2-3 relevant hashtags
   - Stay under 200 words
3. **Image Generation**: The MonsterAPI creates visual prompts based on the caption and generates images.
4. **API Endpoints**: FastAPI provides:
   - A root endpoint with basic info
   - Health checks for API keys
   - Category listing
   - Synchronous/asynchronous post generation
   - News article retrieval by category

## Data Flow
- User requests a post via API endpoints
- The system fetches news data from NewsAPI
- AI processes news data to create captions (via Groq API)
- Caption is used to generate image prompts (via MonsterAPI)
- Final output includes both text and image URLs

## Architecture
- **Frontend**: Not implemented (focus is on backend API)
- **Backend**: FastAPI framework handles requests
- **AI Services**:
  - Groq API for text generation
  - MonsterAPI for image generation
- **Data Sources**:
  - NewsAPI for article content
  - Environment variables for API keys

## Key Features
- Asynchronous processing for background tasks
- Error handling with proper status codes
- Logging for debugging and monitoring
- API key validation to ensure service availability

## Technologies Used
- Python 3.10+
- FastAPI (ASGI framework)
- Groq API (LLM service)
- MonsterAPI (image generation)
- NewsAPI (news data)
- dotenv for environment variables
- Uvicorn as ASGI server

## Configuration
All API keys are stored in a `.env` file:
```
MONSTER_API_KEY=your_monster_api_key_here
GROQ_API_KEY=your_groq_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

## Running the Application
```bash
uvicorn api:app --reload
```

## Example Usage
1. Fetch categories:
   `GET /categories`
2. Generate post:
   `POST /generate` with JSON body:
   ```json
   {
     "category": "health",
     "custom_prompt": "Focus on preventive care aspects"
   }
   ```
3. Check generation status:
   `GET /status/{task_id}`

## Error Handling
- 404: For invalid endpoints or missing news
- 500: For internal server errors (missing API keys, etc.)

## Future Improvements
- Add frontend interface
- Implement user authentication
- Add more content types (e.g., Twitter, Facebook)
- Include analytics tracking
- Add caching for news articles

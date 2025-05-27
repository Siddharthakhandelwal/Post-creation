# Doctor Post Agent - AI-Powered Social Media Content Generator

An intelligent social media content generation system that creates engaging Instagram posts for healthcare professionals by combining real-time news data with AI-powered content generation and image creation.

## 🎯 Project Overview

This application automatically generates Instagram-ready content for doctors by:
- Fetching latest health, medical, and environmental news
- Creating engaging captions using AI language models
- Generating relevant images using AI image generation
- Providing a complete social media post package

## 🏗️ Project Architecture

```
Doctor Post Agent
├── Data Layer (News APIs)
├── Processing Layer (AI Models)
├── Generation Layer (Content & Images)
└── Output Layer (Social Media Ready Content)
```

## 📋 Features

- **Real-time News Fetching**: Retrieves latest news from NewsAPI
- **AI-Powered Caption Generation**: Uses Groq's Llama 3.3 model for creative writing
- **AI Image Generation**: Creates relevant images using Monster API
- **Multi-category Support**: Covers health, medical, and environmental topics
- **Instagram Optimization**: Generates content optimized for Instagram format
- **Automated Workflow**: Complete end-to-end content generation

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7+
- API Keys for:
  - Monster API (Image Generation)
  - Groq API (Text Generation)
  - NewsAPI (News Fetching)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Post
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with your API keys:
   ```env
   MONSTER_API_KEY=your_monster_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   NEWS_API_KEY=your_news_api_key_here
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 📊 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | Latest | HTTP requests for API calls |
| `beautifulsoup4` | Latest | Web scraping (if needed) |
| `groq` | Latest | Groq API client |
| `python-dotenv` | Latest | Environment variable management |
| `monsterapi` | Latest | Monster API client for image generation |

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONSTER_API_KEY` | API key for Monster API image generation | Yes |
| `GROQ_API_KEY` | API key for Groq language model | Yes |
| `NEWS_API_KEY` | API key for NewsAPI news fetching | Yes |

## 🎛️ Configuration Variables

### Core Settings
- `CATEGORIES`: List of news categories to fetch
  - Default: `["health", "medical", "environment"]`
- `today`: Current date for news filtering
- Model configurations for image generation

### API Endpoints
- **NewsAPI**: `https://newsapi.org/v2/everything`
- **Groq API**: `https://api.groq.com/openai/v1/chat/completions`
- **Monster API**: Via client library

## 🔄 Workflow Process

1. **Category Selection**: Randomly selects from predefined categories
2. **News Fetching**: Retrieves latest news articles from NewsAPI
3. **Article Selection**: Randomly picks one article from results
4. **Caption Generation**: Creates Instagram caption using Groq AI
5. **Image Prompt Creation**: Generates visual prompt for image AI
6. **Image Generation**: Creates relevant image using Monster API
7. **Output Delivery**: Provides complete social media post package

## 📈 Data Flow

```
[NewsAPI] → [Article Selection] → [Groq AI] → [Caption]
                                      ↓
[Monster API] ← [Visual Prompt] ← [Caption Analysis]
      ↓
[Generated Image] → [Complete Post Package]
```

## 🏛️ System Architecture

### Layer 1: Data Acquisition
- **NewsAPI Integration**: Fetches real-time news data
- **Category Filtering**: Focuses on health/medical/environmental topics
- **Date Filtering**: Ensures recent and relevant content

### Layer 2: Content Processing
- **Groq AI Integration**: Processes news into engaging captions
- **Prompt Engineering**: Optimizes AI prompts for Instagram format
- **Content Optimization**: Ensures medical professional tone

### Layer 3: Visual Generation
- **Monster API Integration**: Generates relevant images
- **Visual Prompt Creation**: Converts text to visual concepts
- **Image Optimization**: Ensures Instagram-ready format

### Layer 4: Output Management
- **Content Packaging**: Combines text and image
- **Format Optimization**: Ensures social media readiness
- **Error Handling**: Manages API failures gracefully

## 🚀 Usage Examples

### Basic Usage
```python
python main.py
```

### Expected Output
```
🔍 Fetching latest 'health' news for 2025-05-27...

📰 Title: [News Article Title]

📝 Instagram Caption:
[AI-generated caption with emojis and hashtags]

🖼️ Generated Image URL:
[URL to generated image]
```

## 🔧 API Integration Details

### NewsAPI Configuration
- **Endpoint**: `/v2/everything`
- **Parameters**: 
  - `q`: Category query
  - `from`: Date filter
  - `sortBy`: Popularity sorting
  - `apiKey`: Authentication

### Groq API Configuration
- **Model**: `llama-3.3-70b-versatile`
- **System Role**: Expert social media content creator
- **User Role**: Content generation requests

### Monster API Configuration
- **Model**: `sdxl-base`
- **Parameters**:
  - `samples`: 2
  - `steps`: 50
  - `aspect_ratio`: square
  - `guidance_scale`: 7.5

## 🛠️ Error Handling

The application includes comprehensive error handling for:
- API connection failures
- Invalid API responses
- Missing environment variables
- Network connectivity issues
- Rate limiting scenarios

## 📝 Logging & Monitoring

- Console output for process tracking
- Error messages with descriptive context
- Success confirmations for each step
- URL output for generated content

## 🔒 Security Considerations

- API keys stored in environment variables
- No hardcoded credentials in source code
- Secure API communication over HTTPS
- Input validation for API responses

## 🚀 Deployment Options

### Local Development
```bash
python main.py
```

### FastAPI Web Service
Use the included `api.py` for web deployment:
```bash
uvicorn api:app --reload
```

### Docker Deployment
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the error messages in console output
2. Verify API key configuration
3. Ensure all dependencies are installed
4. Check network connectivity

## 🔮 Future Enhancements

- Multiple social media platform support
- Scheduled posting capabilities
- Content analytics and tracking
- Custom prompt templates
- Batch processing capabilities
- Web interface for easier usage

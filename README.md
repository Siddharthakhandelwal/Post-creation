# Doctor Post Agent

**AI-Powered Social Media Content Generator for Healthcare Professionals**

This project is an AI-powered application that automatically generates engaging social media posts for doctors. It scrapes the latest news from reputable sources, selects a relevant article, and then uses a generative AI model to create a concise and informative post suitable for a medical audience.

## Architecture

The application consists of two main components:

1.  **Core Logic (`main.py`):** This module is responsible for the primary functionality of the application. It uses the Firecrawl API to scrape news articles from specified URLs and then leverages the Gemini API to generate social media posts based on the scraped content.

2.  **API Server (`api_server.py`):** This module exposes the functionality of the core logic through a RESTful API built with FastAPI. It provides an endpoint to trigger the post-generation process and returns the generated post in the response.

## Data Flow

1.  **News Source Selection:** The application randomly selects a news category from a predefined list (e.g., Health, Science, Environment).

2.  **Web Scraping:** The Firecrawl API is used to scrape the content of the selected news article.

3.  **Content Generation:** The scraped content is passed to the Gemini API with a prompt to generate a short, engaging social media post for a doctor's audience.

4.  **API Endpoint:** The generated post is made available through a `/post` endpoint in the FastAPI server.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/doctor-post-agent.git
    cd doctor-post-agent
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```
    GEMINI_API_KEY="your-gemini-api-key"
    FIRECRAWL_API_KEY="your-firecrawl-api-key"
    ```

## Usage

1.  **Run the API server:**
    ```bash
    uvicorn api_server:app --reload
    ```

2.  **Generate a post:**
    Send a POST request to the `/post` endpoint using a tool like `curl` or Postman:
    ```bash
    curl -X POST http://127.0.0.1:8000/post
    ```

    The API will respond with a JSON object containing the generated post:
    ```json
    {
      "post": "Generated post content..."
    }
    ```

## Workflow

A GitHub Actions workflow can be set up to automate the deployment of this application. The workflow would typically involve the following steps:

1.  **Checkout:** Checks out the repository code.
2.  **Set up Python:** Sets up the specified version of Python.
3.  **Install dependencies:** Installs the required packages from `requirements.txt`.
4.  **Run tests:** Executes any available tests to ensure code quality.
5.  **Deploy:** Deploys the application to a cloud platform like Heroku, AWS, or Google Cloud.
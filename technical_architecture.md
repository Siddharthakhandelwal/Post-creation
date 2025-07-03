# Technical Architecture and Data Flow

## System Architecture

The application is built on a simple, decoupled architecture consisting of a core logic module and an API server.

*   **`main.py` (Core Logic):** This module contains the business logic of the application. It is responsible for:
    *   **Web Scraping:** Utilizes the `firecrawl-py` library to scrape news articles from a predefined list of URLs. The `app.scrape_url()` function is called to fetch the content of a randomly selected URL in Markdown format.
    *   **Content Generation:** Interacts with the Google Gemini API via the `google-generativeai` library. The scraped content is passed to the `gemini-1.5-flash` model with a specific prompt to generate a social media post.
    *   **API Keys:** Manages API keys for Firecrawl and Gemini services, loaded from a `.env` file using `python-dotenv`.

*   **`api_server.py` (API Server):** This module provides a RESTful API to expose the core functionality.
    *   **Framework:** Built using `FastAPI`, a modern, high-performance web framework for Python.
    *   **Endpoints:**
        *   `GET /`: A root endpoint for health checks, returning a simple status message.
        *   `POST /post`: The main endpoint that triggers the post generation process. It calls the `generate_doctor_post()` function from `main.py` and returns the generated post as a JSON response.
    *   **CORS:** Implements Cross-Origin Resource Sharing (CORS) middleware to allow requests from any origin. This should be configured to a specific domain in a production environment.
    *   **Error Handling:** Includes basic error handling to catch exceptions during the post generation process and returns a `500 Internal Server Error` with the error details.

## Data Flow Diagram

```
+-----------------+      +------------------+      +-----------------+
|   API Client    |----->|   FastAPI Server   |----->|   Core Logic    |
| (e.g., curl)    |      |  (api_server.py) |      |    (main.py)    |
+-----------------+      +------------------+      +-----------------+
      ^                      |                      |
      |                      |                      |
      |                      v                      v
      |      +------------------+      +-----------------+
      |      |   Generate Post  |      |  Scrape Article |
      |      |    (POST /post)  |      |  (Firecrawl API)|
      |      +------------------+      +-----------------+
      |                      |                      |
      |                      |                      v
      |                      |      +-----------------+
      |                      |      |  Generate Text  |
      |                      |      |   (Gemini API)  |
      |                      |      +-----------------+
      |                      |                      |
      |                      +----------------------+
      |                                             |
      +---------------------------------------------+
                         (JSON Response)
```

## Detailed Data Flow

1.  **Request Initiation:** An API client sends a `POST` request to the `/post` endpoint of the FastAPI server.
2.  **Endpoint Handling:** The `generate_post()` function in `api_server.py` receives the request.
3.  **Core Logic Invocation:** The `generate_post()` function calls the `generate_doctor_post()` function from the `main.py` module.
4.  **URL Selection:** `generate_doctor_post()` randomly selects a URL from the `links` list.
5.  **Web Scraping:** The selected URL is passed to the `crawl_url()` function, which uses the Firecrawl API to scrape the content of the page. The result is returned in Markdown format.
6.  **Content Generation:** The scraped content is then passed to the Google Gemini API. A prompt is constructed to instruct the model to generate a short, engaging post for a doctor's audience.
7.  **Response Generation:** The Gemini API returns the generated text.
8.  **API Response:** The `generate_doctor_post()` function returns the generated text to the `api_server.py` module, which then sends it back to the API client as a JSON response with a `200 OK` status.
9.  **Error Handling:** If any exception occurs during this process, the FastAPI server catches it and returns a `500 Internal Server Error` with the exception details.
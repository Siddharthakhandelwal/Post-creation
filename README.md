# Doctor Post Agent

This project generates creative, trending social media posts for doctors or the general public, based on real-time web data and AI.

## Features

- Scrapes trending hashtags, health news, and environment issues from the web
- Uses Google's Gemini model to generate engaging posts or articles
- 100% free and open source (except for Gemini API usage)

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Gemini API key:**

   - Create a `.env` file in the project root (if not already present)
   - Add your API key:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

3. **Run the agent:**
   ```bash
   python agent.py
   ```
   The script will scrape trending topics and print a creative, relevant post to your console.

## How it works

- Scrapes trending hashtags from best-hashtags.com
- Scrapes trending health and environment news from Google News
- Sends all trending data (including a list of hashtags and news) to Google Gemini with a prompt to filter and generate a creative post
- The model is instructed to use the provided hashtags and keywords in the generated post
- Prints the result in a social-media-ready format

## Notes

- You need a valid Gemini API key (see https://aistudio.google.com/app/apikey)
- All scraping uses public/free sources
- Only `agent.py`, `data_sources.py`, `requirements.txt`, `.env`, and this `README.md` are required for the CLI tool.
- There may be legacy files (e.g., old Streamlit code). **Ask before deleting any files.**

## Free and Open Source

- Uses only free APIs and open-source models (except Gemini API)

from data_sources import (
    scrape_trending_hashtags,
    scrape_trending_news,
    scrape_environment_issues
)

import groq
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API")

def call_groq_for_post(trending_data):
    # Compose the prompt
    prompt = (
        "These are the trending topics, headlines, and hashtags: "
        f"{trending_data}\n"
        "Filter out the headings or hashtags related to doctors or normal people, "
        "and then write a creative, engaging social media post or article on it."
    )
    # Call Groq API using the key from .env
    try:
        client = groq.Client(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error generating post: {e}]"

if __name__ == "__main__":
    print("Scraping trending hashtags...")
    hashtags = scrape_trending_hashtags()
    print("Scraping trending news...")
    news = scrape_trending_news()
    print("Scraping environment issues...")
    env_issues = scrape_environment_issues()
    trending_data = {
        "hashtags": hashtags,
        "news": news,
        "environment_issues": env_issues
    }
    print("\nGenerating post using Groq...")
    post = call_groq_for_post(trending_data)
    print("\n--- Generated Post ---\n")
    print(post)

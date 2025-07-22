from data_sources import (
    scrape_trending_hashtags,
    scrape_trending_news,
    scrape_environment_issues
)

import requests
import os
from dotenv import load_dotenv
from google import genai
# Load environment variables from .env
load_dotenv()

def call_Gemini_for_post(word_limit, hashtags, keyword_count, keyword, news):
    """
    Generate a post using Gemini API.
    Args:
        word_limit (int): Maximum word count for the post.
        hashtags (list): List of hashtags to use in the post.
        keyword_count (int): Minimum number of times hashtags should appear.
        keyword (str): Keyword(s) to include in the post.
        news (list): List of news headlines to use as context.
    Returns:
        str: Generated post or error message.
    """

    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
        "Authorization": "Bearer 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",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
        hashtags_str = ', '.join(hashtags)
        news_str = '\n'.join(news)
        prompt = (
            f""
            f"Create an interactive and interesting post for a Doctor's audience based on the following scraped news from the internet:\n{news_str}\n"
            f"Choose any one of the news items in which the following hashtags can be used: {hashtags_str}. "
            f"Create a post for a Doctor's audience. Use emojis and hashtags if needed. Only return the post, no other text. "
            f"Keep the word limit to {word_limit} max. Try to use the keyword {keyword} in this post at least {keyword_count} times. "
        )
        payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True  # Enable streaming for real-time responses
    }
        response = requests.post(url, headers=headers, json=payload, stream=True)
        return response.text
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
    print("\nGenerating post using Gemini...")
    post = call_Gemini_for_post(100, hashtags, 2, "covid", news)
    print("\n--- Generated Post ---\n")
    print(post)
    print(hashtags)

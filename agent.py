from data_sources import (
    scrape_trending_hashtags,
    scrape_trending_news,
    scrape_environment_issues
)


import os
from dotenv import load_dotenv
from google import genai
# Load environment variables from .env
load_dotenv()

def call_Gemini_for_post(word_limit, hashtags, hashtag_count, keyword, news):
    """
    Generate a post using Gemini API.
    Args:
        word_limit (int): Maximum word count for the post.
        hashtags (list): List of hashtags to use in the post.
        hashtag_count (int): Minimum number of times hashtags should appear.
        keyword (str): Keyword(s) to include in the post.
        news (list): List of news headlines to use as context.
    Returns:
        str: Generated post or error message.
    """
    try:
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        hashtags_str = ', '.join(hashtags)
        news_str = '\n'.join(news)
        prompt = (
            f"Create an interactive and interesting post for a Doctor's audience based on the following scraped news from the internet:\n{news_str}\n"
            f"Choose any one of the news items in which the following hashtags can be used: {hashtags_str}. "
            f"Create a post for a Doctor's audience. Use emojis and hashtags if needed. Only return the post, no other text. "
            f"Keep the word limit to {word_limit} max. Try to use the hashtags in this post at least {hashtag_count} times. "
            f"Also include these keywords: {keyword}."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
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
    post = call_Gemini_for_post(100, hashtags, 2, "health, pollution", news)
    print("\n--- Generated Post ---\n")
    print(post)
    print(hashtags)

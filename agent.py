from data_sources import (
    scrape_trending_hashtags,
    scrape_trending_news,
    scrape_environment_issues
)

import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def post_gemini(prompt):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print(e)
        return f"[Error generating post: {e}]"
    
def post_perplexity(prompt):

    try:
        api_key=os.getenv("Perplexity")
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
        "Authorization": f"Bearer {api_key}",  # Replace with your actual API key
        "Content-Type": "application/json"
        }
        payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Disable streaming for easier response handling
    }
        response = requests.post(url, headers=headers, json=payload)
        
        # Parse the JSON response and extract only the content
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        print(content)
        
        # Return only the content
        return content
    except Exception as e:
        return f"[Error generating post: {e}]"
    
def post_groq(prompt):

    try:
        api_key=os.getenv("GROQ_API")
        url="https://api.groq.com/openai/v1/chat/completions"
        headers = {
        "Authorization": f"Bearer {api_key}",  # Replace with your actual API key
        "Content-Type": "application/json"
        }
        payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=payload)
        
        # Parse the JSON response and extract only the content
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        print(content)
        # Return only the content
        return content

    except Exception as e:
        return f"[Error generating post: {e}]"



if __name__ == "__main__":
    print("Scraping trending hashtags...")
    hashtags = scrape_trending_hashtags()
    print("Scraping trending news...")
    news = scrape_trending_news()
    # print("Scraping environment issues...")
    # env_issues = scrape_environment_issues()
    trending_data = {
        "hashtags": hashtags,
        "news": news,
    }

    hashtags_str = ', '.join(hashtags)
    news_str = '\n'.join(news)

    model_input=input("Enter model name ( Gemini , perplexity , Groq ):")
    prompt_input=input("Which prompt ( Old or New ): ")

    word_limit=int(input("Enter the word limit: "))
    keyword=input("Enter the Key word you want: ")
    keyword_count=int(input("Keyword count in the whole post: "))
    keyword_count_line=int(input("Keyword count per Line: "))

    prompt_old=f'''
        Create an interactive and interesting post for a Doctor's audience based on the following scraped news from the internet:\n{news_str}\n
        Choose any one of the news items in which the following hashtags can be used: {hashtags_str}. 
        Create a post for a Doctor's audience. Use emojis and hashtags if needed. Only return the post, no other text. 
        Keep the word limit to {word_limit} max. Try to use the keyword {keyword} in this post at least {keyword_count} times. 
    '''

    prompt_new=f'''You're creating a social media post on behalf of a doctor, intended to educate, engage, and inform patients or a general public audience.The content must be based on the scraped news articles provided in the following string:{news_str}
    📌 Instructions:
        Carefully read through the news and select only one news item that is most relevant or engaging for a doctor's audience (e.g. patients, health-conscious individuals).
        Create a short, catchy, and informative post that communicates the key message clearly.
        The tone should be friendly, trustworthy, and easy to understand — like how a doctor would explain something to their patients.
        Use emojis where appropriate to increase readability and engagement.

    Try to include the following hashtags naturally (you can choose the most relevant ones):{hashtags_str}
    Integrate the keyword below into the post at least {keyword_count} times:{keyword} and also try to use this keyword {keyword_count_line} times in a line. 
    📏 Keep the total word count within {word_limit} words.
    ❗Output only the final social media post — do not include any explanations or formatting outside the post itself.

    '''

    if "Ge" in model_input:
        print("\nGenerating post using Gemini...")
        if "d" in prompt_input:
            post_gemini(prompt_old)
        elif "w" in prompt_input:
            post_gemini(prompt_new)

    elif "p" in model_input:
        print("\nGenerating post using perplexity...")
        if "d" in prompt_input:
            post_perplexity(prompt_old)
        elif "w" in prompt_input:
            post_perplexity(prompt_new)

    elif "Gr" in model_input :
        print("\nGenerating post using Groq...")
        if "d" in prompt_input:
            post_groq(prompt_old)
        elif "w" in prompt_input:
            post_groq(prompt_new)
        
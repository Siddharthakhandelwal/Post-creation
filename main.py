import requests
import random
from datetime import datetime
import os
from dotenv import load_dotenv
from monsterapi import client

# Load environment variables from .env file
load_dotenv()

# === API KEYS (stored in .env) ===
MONSTER_API_KEY = os.getenv("MONSTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize Monster API client
monster_client = client(MONSTER_API_KEY)

# Topics of interest
CATEGORIES = ["health", "medical", "environment"]

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# === Fetch News from NewsAPI ===
def fetch_latest_news(category):
    url = (
        f'https://newsapi.org/v2/everything?'
        f'q={category}&'
        f'from={today}&'
        f'sortBy=popularity&'
        f'apiKey={NEWS_API_KEY}'
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return None
        return random.choice(articles)
    except Exception as e:
        print("❌ Error fetching news:", e)
        return None

# === Generate Caption using Groq API ===
def generate_caption(prompt, context):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print("❌ Error generating caption:", e)
        return "Unable to generate caption."

# === Generate Image using Monster API ===
def generate_image(prompt):
    # model = 'txt2img'
    # input_data = {
    #     'prompt': prompt,
    #     'negprompt': 'blurry, cartoon, unrealistic, fantasy',
    #     'samples': 1,
    #     'steps': 40,
    #     'aspect_ratio': 'square',
    #     'guidance_scale': 8,
    #     'seed': random.randint(1000, 9999),
    # }
    model = 'sdxl-base' 
# Replace with the desired model name
    input_data = {
    'prompt': prompt,
    'negprompt':'blurry, cartoon, unrealistic, fantasy',
    'samples': 2,
    'enhance': True,
    'optimize': True,
    'safe_filter': True,
    'steps': 50,
    'aspect_ratio': 'square',
    'guidance_scale': 7.5,
    'seed': 2414,
    }

    try:
        result = monster_client.generate(model, input_data)
        return result['output'][0]  # Return image URL
    except Exception as e:
        print("❌ Error generating image:", e)
        return None

# === Main Execution Flow ===
def main():
    category = random.choice(CATEGORIES)
    print(f"🔍 Fetching latest '{category}' news for {today}...\n")

    news = fetch_latest_news(category)
    if not news:
        print("⚠️ No news found.")
        return

    print(f"📰 Title: {news['title']}\n")

    caption_prompt = f"""
    You are a creative Instagram content writer for a doctor. Write an engaging, informative, and emotional Instagram Post for the following news. Use emojis, 2-3 relevant hashtags, and keep it under 200 words.

    Title: {news.get('title', '')}
    Description: {news.get('description', '')}
    Link: {news.get('url', '')}
    """
    context = "You are an expert social media content creator for a doctor."

    caption = generate_caption(caption_prompt, context)

    print("📝 Instagram Caption:\n")
    print(caption)

    image_prompt_request = f"Create a visual prompt for an AI model to generate an Instagram-style image based on this caption:\n\n{caption}"
    visual_prompt = generate_caption(image_prompt_request, context)

    image_url = generate_image(visual_prompt)

    if image_url:
        print("\n🖼️ Generated Image URL:\n", image_url)
    else:
        print("\n⚠️ No image generated.")

# Run the program
if __name__ == "__main__":
    main()

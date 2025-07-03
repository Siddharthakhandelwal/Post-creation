from firecrawl import FirecrawlApp
import os
import numpy as np
from google import genai
from dotenv import load_dotenv


load_dotenv()

app = FirecrawlApp(api_key=os.environ.get("firecrawl"))

links = [
    {"health": "https://www.thehindu.com/sci-tech/health/"},
    {"India": "https://www.thehindu.com/news/national/"},
    {"Enviroment": "https://www.thehindu.com/sci-tech/energy-and-environment/"},
    {"Science": "https://www.thehindu.com/sci-tech/science/"}
]

def crawl_url(link):
    
    scrape_result = app.scrape_url(link, formats=['markdown'])
    return scrape_result

def generate_doctor_post():
    link_dict = links[np.random.randint(0, len(links))]
    link_to_crawl = list(link_dict.values())[0]
    news = crawl_url(link_to_crawl)
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Create a interactive and intresting post for Doctor's audience based on the following scrapped news from the internet:\n{news}\n , choose any one of the news and create a post for Doctor's audience. Keep the post short (max 50-70 words). Use emojis and hashtags if needed.only return the post no other text"
    )
    return response.text


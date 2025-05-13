import requests
from bs4 import BeautifulSoup # type: ignore

# Free APIs (no key required) or static lists as fallback

def scrape_trending_hashtags():
    # Example: Scrape trending hashtags from a public site (like best-hashtags.com)
    try:
        url = 'https://best-hashtags.com/hashtag/health/'
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        hashtags = []
        tag_block = soup.find('div', {'class': 'tag-box tag-box-v3 margin-bottom-40'})
        if tag_block:
            hashtags = [tag.strip() for tag in tag_block.text.split() if tag.startswith('#')]
        return hashtags[:10]
    except Exception:
        return ['#health', '#wellness', '#doctor', '#fitness', '#mentalhealth']

def scrape_trending_news():
    # Example: Scrape health news headlines from Google News
    try:
        url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ4Y0dNU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US:en'
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        headlines = [a.text for a in soup.find_all('a', {'class': 'DY5T1d'})]
        return headlines[:10]
    except Exception:
        return ["Global health update: Stay safe!", "New research on heart health released."]

def scrape_environment_issues():
    # Example: Scrape environment news from Google News
    try:
        url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ4Y0dNU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US:en'
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        headlines = [a.text for a in soup.find_all('a', {'class': 'DY5T1d'}) if 'environment' in a.text.lower()]
        return headlines[:10]
    except Exception:
        return ["Climate change impacts health worldwide."]

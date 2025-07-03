# Project Explanation: AI Social Media Assistant for Doctors

## What is this project?

Imagine a helpful assistant who reads the latest news every day and then writes interesting social media posts for your doctor. This project is exactly that—an automated social media assistant designed specifically for healthcare professionals. It helps doctors stay active on social media by providing them with fresh, relevant content to share with their audience.

## How does it work? (Data Flow)

The process is simple and can be broken down into a few key steps:

1.  **Picks a Topic:** The assistant starts by choosing a news category from a list of topics like "Health," "Science," or "Environment."

2.  **Reads the News:** Once a topic is selected, the assistant visits a reputable news website and reads the latest articles in that category.

3.  **Writes a Post:** After reading an article, the assistant uses artificial intelligence (the same technology behind chatbots like ChatGPT) to write a short and engaging social media post. The post is designed to be interesting for a medical audience and often includes emojis and hashtags to make it more appealing.

4.  **Delivers the Post:** The final post is then delivered and ready to be shared on the doctor's social media accounts.

## The "Architecture" (How it's built)

Think of the project as having two main parts that work together:

1.  **The "Brain" (`main.py`):** This is the core of the operation. It's responsible for all the smart work, like picking the news, reading the articles (using a service called Firecrawl), and writing the posts (using Google's Gemini AI).

2.  **The "Messenger" (`api_server.py`):** This part of the project acts like a messenger. It takes the post created by the "Brain" and makes it available through a simple web link (an API). This allows other applications or services to easily grab the post and share it.

In short, this project is a time-saving tool that helps doctors maintain an active and informative social media presence with minimal effort.
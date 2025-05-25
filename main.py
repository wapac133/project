# AutoNiche GhostMachine - Fully Automated Digital Product Factory
# Built for Replit / Railway Deployment

import os
import requests
import openai
import datetime
from bs4 import BeautifulSoup
from fpdf import FPDF

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- STEP 1: GET TRENDS FROM REDDIT --- #
def get_trending_topics(subreddit="entrepreneur"):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    response = requests.get(url, headers=headers)
    data = response.json()
    topics = [post['data']['title'] for post in data['data']['children']]
    return topics

# --- STEP 2: GENERATE PRODUCT CONTENT --- #
def generate_ebook(topic):
    prompt = f"""
    Create a 10-page actionable mini-ebook for the topic: "{topic}".
    Include a title, table of contents, and 10 short chapters with tips, examples, and clear headings.
    End with a call to action.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- STEP 3: EXPORT TO PDF --- #
def save_to_pdf(title, content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    filename = title.replace(" ", "_")[:50] + ".pdf"
    pdf.output(f"/mnt/data/{filename}")
    return filename

# --- STEP 4: UPLOAD TO GUMROAD (semi-automated) --- #
def print_gumroad_upload_instructions(title, filename):
    print("\n\n=== UPLOAD MANUALLY ONCE ===")
    print(f"Title: {title}")
    print(f"File: {filename}")
    print("Go to: https://gumroad.com/products/new")
    print("Set price: $9")
    print("Paste generated content as product description.")

# --- STEP 5: GENERATE SOCIAL POSTS --- #
def generate_social_post(topic):
    prompt = f"Write a viral tweet promoting a digital ebook titled '{topic}' that solves a common problem."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === MAIN EXECUTION === #
def run_daily_automation():
    topics = get_trending_topics()
    for topic in topics[:1]:  # Limit to 1 product per day
        print(f"\nGenerating product for: {topic}")
        content = generate_ebook(topic)
        filename = save_to_pdf(topic, content)
        print_gumroad_upload_instructions(topic, filename)
        tweet = generate_social_post(topic)
        print("\nSuggested Tweet:")
        print(tweet)

if __name__ == "__main__":
    run_daily_automation()

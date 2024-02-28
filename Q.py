import requests
from bs4 import BeautifulSoup
import sqlite3
import pyshorteners

def extract_previews(url):
    # Fetch the HTML content of the URL
    response = requests.get(url)
    html_content = response.text

    # Parse HTML using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract social media previews
    title = soup.find('meta', property='og:title')
    description = soup.find('meta', property='og:description')
    image = soup.find('meta', property='og:image')

    # Get the content of the meta tags
    title_content = title['content'] if title else ''
    description_content = description['content'] if description else ''
    image_content = image['content'] if image else ''

    return title_content, description_content, image_content

def generate_short_link(url):
    # Initialize shortener
    shortener = pyshorteners.Shortener()

    # Generate short link
    short_link = shortener.tinyurl.short(url)

    return short_link

def store_data(url, title, description, image, short_link):
    # Connect to SQLite database
    conn = sqlite3.connect('social_media_previews.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS previews
                 (url TEXT, title TEXT, description TEXT, image TEXT, short_link TEXT)''')

    # Insert data into the table
    c.execute("INSERT INTO previews VALUES (?, ?, ?, ?, ?)", (url, title, description, image, short_link))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Sample URL
    url = "https://ilmkey.xyz"

    # Extract social media previews
    title, description, image = extract_previews(url)

    # Generate short link
    short_link = generate_short_link(url)

    # Store data in the database
    store_data(url, title, description, image, short_link)

    print("Social media previews extracted and stored successfully!")

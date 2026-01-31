"""
Test script to debug Anthropic scraping
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.anthropic.com/news"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Save the HTML for inspection
    with open('anthropic_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print("✓ Page fetched successfully")
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)} bytes")
    print("\nTesting selectors:")
    
    # Test different selectors
    articles = soup.select("article")
    print(f"\n1. 'article' selector: {len(articles)} found")
    
    divs_with_news = soup.find_all('div', class_=lambda x: x and 'news' in x.lower() if x else False)
    print(f"2. divs with 'news' class: {len(divs_with_news)} found")
    
    links_with_news = soup.find_all('a', href=lambda x: x and '/news/' in x if x else False)
    print(f"3. links with '/news/' in href: {len(links_with_news)} found")
    
    # Look for common structures
    all_links = soup.find_all('a', href=True)
    news_links = [a for a in all_links if a.get('href', '').startswith('/news/')]
    print(f"4. Links starting with '/news/': {len(news_links)} found")
    
    if news_links:
        print("\nFirst few news links found:")
        for i, link in enumerate(news_links[:5], 1):
            print(f"  {i}. {link.get('href')}")
            title_elem = link.find(['h2', 'h3', 'h4', 'h5'])
            if title_elem:
                print(f"     Title: {title_elem.get_text(strip=True)}")
    
    # Check for specific patterns in the page
    print("\nLooking for common patterns:")
    print(f"  - Total <a> tags: {len(all_links)}")
    print(f"  - <article> tags: {len(soup.find_all('article'))}")
    print(f"  - <div> tags: {len(soup.find_all('div'))}")
    
    # Find all unique class names used
    all_classes = set()
    for tag in soup.find_all(class_=True):
        classes = tag.get('class', [])
        if isinstance(classes, list):
            all_classes.update(classes)
    
    # Filter for likely news-related classes
    news_classes = [c for c in all_classes if any(keyword in c.lower() for keyword in ['news', 'post', 'article', 'item', 'card', 'entry'])]
    print(f"\n  - Likely news-related classes: {', '.join(sorted(news_classes)[:10])}")
    
except Exception as e:
    print(f"Error: {e}")

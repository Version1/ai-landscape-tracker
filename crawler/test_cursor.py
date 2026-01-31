"""
Test script to debug Cursor scraping
"""

import requests
from bs4 import BeautifulSoup

url = "https://www.cursor.com/changelog"

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
    with open('cursor_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print("[OK] Page fetched successfully")
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)} bytes")
    print("\nTesting selectors from config:")
    
    # Test configured selector
    articles = soup.select(".changelog-entry")
    print(f"1. '.changelog-entry' selector: {len(articles)} found")
    
    # Try alternative selectors
    test_selectors = [
        "article",
        ".entry",
        "[class*='changelog']",
        "[class*='entry']",
        "[class*='change']",
    ]
    
    for selector in test_selectors:
        results = soup.select(selector)
        print(f"2. '{selector}' selector: {len(results)} found")
    
    # Look for common patterns
    print("\nLooking for common patterns:")
    print(f"  - Total <article> tags: {len(soup.find_all('article'))}")
    print(f"  - Total <div> tags: {len(soup.find_all('div'))}")
    print(f"  - Total <section> tags: {len(soup.find_all('section'))}")
    
    # Find all unique class names used
    all_classes = set()
    for tag in soup.find_all(class_=True):
        classes = tag.get('class', [])
        if isinstance(classes, list):
            all_classes.update(classes)
    
    # Filter for likely changelog-related classes
    changelog_classes = [c for c in all_classes if any(keyword in c.lower() for keyword in ['change', 'log', 'entry', 'item', 'post', 'update', 'version', 'release'])]
    print(f"\n  - Likely changelog-related classes: {', '.join(sorted(changelog_classes)[:15])}")
    
    # Check for date patterns
    dates = soup.find_all(['time', 'span', 'div'], class_=lambda x: x and any(d in str(x).lower() for d in ['date', 'time']) if x else False)
    print(f"\n  - Elements with date/time in class: {len(dates)} found")
    if dates:
        print(f"    First few: {[d.get('class') for d in dates[:3]]}")
    
    # Look for headings that might be titles
    h_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"\n  - Total heading tags: {len(h_tags)} found")
    if h_tags:
        print(f"    First few headings:")
        for i, h in enumerate(h_tags[:5], 1):
            print(f"      {i}. <{h.name}>: {h.get_text(strip=True)[:60]}")
    
    # Check if content looks dynamic
    scripts = soup.find_all('script')
    react_indicators = ['__NEXT_DATA__', 'React', 'react', 'next', '__next']
    has_react = any(indicator in str(script) for script in scripts for indicator in react_indicators)
    print(f"\n  - Possible React/Next.js app: {has_react}")
    
    if len(response.text) < 50000:
        print(f"  - Small HTML size ({len(response.text)} bytes) - might be JavaScript-rendered")
    
except Exception as e:
    print(f"Error: {e}")

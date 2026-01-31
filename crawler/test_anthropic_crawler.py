"""
Test Anthropic crawling specifically with debug output
"""

import sys
sys.path.insert(0, 'src')

from crawler import Crawler

# Create crawler instance
crawler = Crawler(config_path='config.yaml')

# Find Anthropic source
anthropic_source = None
for source in crawler.config.get('sources', []):
    if source['name'] == 'Anthropic':
        anthropic_source = source
        break

if not anthropic_source:
    print("ERROR: Anthropic source not found in config")
    sys.exit(1)

print(f"Testing Anthropic source:")
print(f"  URL: {anthropic_source['url']}")
print(f"  Selectors: {anthropic_source['selectors']}")
print()

# Crawl just Anthropic
print("Fetching page...")
soup = crawler._fetch_page(anthropic_source['url'])

if not soup:
    print("ERROR: Failed to fetch page")
    sys.exit(1)

print("[OK] Page fetched successfully\n")

# Test selectors
selectors = anthropic_source.get('selectors', {})
article_selector = selectors.get('article_list', 'article')
print(f"Looking for articles with selector: '{article_selector}'")

articles = soup.select(article_selector)
print(f"Found {len(articles)} articles\n")

if len(articles) == 0:
    print("ERROR: No articles found. Testing alternative selectors...")
    
    # Test alternatives
    test_selectors = [
        "a[href^='/news/']",
        'a[href*="/news/"]',
        'a[href*="news"]'
    ]
    
    for test_sel in test_selectors:
        test_articles = soup.select(test_sel)
        print(f"  {test_sel}: {len(test_articles)} found")
    
    # Try finding with find_all
    print("\nTrying with find_all:")
    all_links = soup.find_all('a', href=True)
    print(f"  Total <a> tags with href: {len(all_links)}")
    
    news_links = [a for a in all_links if a.get('href', '').startswith('/news/')]
    print(f"  Links with href starting with '/news/': {len(news_links)} found")
    
    # Check what hrefs we DO have
    print("\nSample of hrefs found (first 20):")
    for i, link in enumerate(all_links[:20], 1):
        href = link.get('href', '')
        print(f"    {i}. {href}")
    
    # Save the HTML to compare
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("[OK] Saved HTML to debug_page.html for inspection")
    
    if news_links:
        print("\nFirst 3 news links found with find_all:")
        for i, link in enumerate(news_links[:3], 1):
            print(f"    {i}. href={link.get('href')}")
            print(f"       classes={link.get('class')}")
    
    sys.exit(1)

# Process first few articles
print("Processing first 5 articles:\n")
for i, article in enumerate(articles[:5], 1):
    print(f"Article {i}:")
    
    # Get title
    title_elem = article.select_one(selectors.get('title', 'h2'))
    title = title_elem.get_text(strip=True) if title_elem else "NO TITLE"
    print(f"  Title: {title}")
    
    # Get date
    date_elem = article.select_one(selectors.get('date', 'time'))
    if date_elem:
        date_str = date_elem.get('datetime', date_elem.get_text(strip=True))
        parsed_date = crawler._parse_date(date_str)
        within_range = crawler._is_within_backfill_range(parsed_date)
        print(f"  Date: {date_str} -> {parsed_date}")
        print(f"  Within backfill range? {within_range}")
    else:
        print(f"  Date: NO DATE FOUND")
    
    # Get URL
    link_selector = selectors.get('link', 'a')
    if link_selector is None:
        link_elem = article if article.name == 'a' else None
    else:
        link_elem = article.select_one(link_selector)
    
    if link_elem:
        href = link_elem.get('href', '')
        print(f"  Raw href: {href}")
        
        # Test URL construction logic
        if href and not href.startswith('http'):
            base_url = anthropic_source['url'].rstrip('/')
            constructed_url = f"{base_url}/{href.lstrip('/')}"
            print(f"  Constructed URL: {constructed_url}")
        else:
            print(f"  Final URL: {href}")
    else:
        print(f"  Link: NO LINK FOUND")
    
    print()

print("\nBackfill config:")
print(f"  Enabled: {crawler.config.get('backfill', {}).get('enabled', False)}")
print(f"  Start date: {crawler.config.get('backfill', {}).get('start_date', 'N/A')}")

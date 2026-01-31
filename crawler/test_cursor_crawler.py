"""
Test Cursor crawling specifically with updated selectors
"""

import sys
sys.path.insert(0, 'src')

from crawler import Crawler

# Create crawler instance
crawler = Crawler(config_path='config.yaml')

# Find Cursor source
cursor_source = None
for source in crawler.config.get('sources', []):
    if source['name'] == 'Cursor':
        cursor_source = source
        break

if not cursor_source:
    print("ERROR: Cursor source not found in config")
    sys.exit(1)

print(f"Testing Cursor source:")
print(f"  URL: {cursor_source['url']}")
print(f"  Selectors: {cursor_source['selectors']}")
print()

# Crawl Cursor
entries = crawler.crawl_source(cursor_source)

print(f"\nResult: {len(entries)} entries found")

if entries:
    print("\nFirst 3 entries:")
    for i, entry in enumerate(entries[:3], 1):
        print(f"\n{i}. {entry['title']}")
        print(f"   Date: {entry['date']}")
        print(f"   URL: {entry['url']}")
        print(f"   Content preview: {entry['content'][:100]}...")
else:
    print("\nNo entries found - debugging...")
    
    soup = crawler._fetch_page(cursor_source['url'])
    if soup:
        selectors = cursor_source['selectors']
        articles = soup.select(selectors['article_list'])
        print(f"\nFound {len(articles)} articles")
        
        if articles:
            print("\nFirst article analysis:")
            article = articles[0]
            
            title_elem = article.select_one(selectors.get('title', 'h2'))
            print(f"  Title element: {title_elem}")
            if title_elem:
                print(f"    Text: {title_elem.get_text(strip=True)}")
            
            date_elem = article.select_one(selectors.get('date', 'time'))
            print(f"  Date element: {date_elem}")
            if date_elem:
                print(f"    datetime: {date_elem.get('datetime')}")
                print(f"    Text: {date_elem.get_text(strip=True)}")
            
            link_elem = article.select_one(selectors.get('link', 'a'))
            print(f"  Link element: {link_elem}")
            if link_elem:
                print(f"    href: {link_elem.get('href')}")

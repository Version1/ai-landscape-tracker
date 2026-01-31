import sys
sys.path.insert(0, 'src')
from crawler import Crawler

c = Crawler('config.yaml')
soup = c._fetch_page('https://www.cursor.com/changelog')

with open('cursor_fetch_test.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print(f"HTML length: {len(soup.prettify())}")
print(f"Articles found: {len(soup.find_all('article'))}")
print("Saved to cursor_fetch_test.html")

# Also compare with direct request
import requests
r = requests.get('https://www.cursor.com/changelog')
print(f"\nDirect request:")
print(f"  HTML length: {len(r.text)}")
print(f"  Has <article: {'<article' in r.text}")

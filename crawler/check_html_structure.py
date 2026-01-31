#!/usr/bin/env python3
"""Check HTML structure of recent Anthropic entries."""

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.anthropic.com/news')
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.select("a[href^='/news/']")

print("=== Entry with title (older, Nov 2025) ===")
print(links[0].prettify())
print("\n\n")

print("=== Entry without title (recent, Jan 2026) ===")
print(links[4].prettify())

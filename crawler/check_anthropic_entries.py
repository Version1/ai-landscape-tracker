#!/usr/bin/env python3
"""Check why we're not seeing all Anthropic news entries."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# Fetch page
r = requests.get('https://www.anthropic.com/news')
soup = BeautifulSoup(r.text, 'html.parser')

# Find all news links
links = soup.select("a[href^='/news/']")
print(f'Total news links found: {len(links)}\n')

# Process each link
entries = []
for i, link in enumerate(links, 1):
    title_elem = link.select_one("h4, h3")
    title = title_elem.get_text(strip=True) if title_elem else "NO TITLE"
    
    date_elem = link.select_one("time")
    date_str = date_elem.get('datetime', date_elem.get_text(strip=True)) if date_elem else "NO DATE"
    
    href = link.get('href', '')
    
    # Parse date
    parsed_date = None
    if date_str and date_str != "NO DATE":
        try:
            # Try parsing as ISO format first
            parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                # Try common date formats
                for fmt in ['%b %d, %Y', '%B %d, %Y', '%Y-%m-%d']:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
                        break
                    except:
                        continue
            except:
                pass
    
    # Check if within backfill range (2024-01-01 onwards)
    within_range = False
    if parsed_date:
        backfill_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        within_range = parsed_date >= backfill_start
    
    entries.append({
        'title': title,
        'date_str': date_str,
        'parsed_date': parsed_date,
        'within_range': within_range,
        'href': href
    })
    
    print(f"{i}. {title}")
    print(f"   Date: {date_str} -> {parsed_date.strftime('%Y-%m-%d') if parsed_date else 'PARSE FAILED'}")
    print(f"   Within range: {within_range}")
    print(f"   URL: {href}")
    print()

# Summary
print(f"\n=== SUMMARY ===")
print(f"Total links: {len(links)}")
print(f"Entries within backfill range: {sum(1 for e in entries if e['within_range'])}")
print(f"Entries with parse errors: {sum(1 for e in entries if e['parsed_date'] is None and e['date_str'] != 'NO DATE')}")
print(f"Entries with no date: {sum(1 for e in entries if e['date_str'] == 'NO DATE')}")

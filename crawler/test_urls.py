#!/usr/bin/env python3
"""Quick test of URL construction for Anthropic and Cursor."""

import yaml
from src.crawler import Crawler

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

crawler = Crawler('config.yaml')

# Test Anthropic
print("Testing Anthropic...")
anthropic_source = config['sources'][0]
entries = crawler.crawl_source(anthropic_source)
print(f"Found {len(entries)} entries")
if entries:
    print("\nFirst 3 entries:")
    for i, entry in enumerate(entries[:3], 1):
        print(f"{i}. {entry['title']}")
        print(f"   URL: {entry['url']}")
        print()

# Test Cursor
print("\nTesting Cursor...")
cursor_source = [s for s in config['sources'] if s['name'] == 'Cursor'][0]
entries = crawler.crawl_source(cursor_source)
print(f"Found {len(entries)} entries")
if entries:
    print("\nFirst 3 entries:")
    for i, entry in enumerate(entries[:3], 1):
        print(f"{i}. {entry['title']}")
        print(f"   URL: {entry['url']}")
        print()

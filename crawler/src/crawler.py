"""
Agentic AI Landscape Tracker - Web Crawler
Fetches and processes content from AI news sources.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
import feedparser
import yaml
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from summarizer import Summarizer


class Crawler:
    """Main crawler class for fetching AI news from configured sources."""
    
    def __init__(self, config_path: str = "../config.yaml"):
        self.config = self._load_config(config_path)
        self.summarizer = Summarizer()
        self.entries = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load crawler configuration from YAML file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _generate_id(self, url: str, title: str) -> str:
        """Generate unique ID for an entry."""
        content = f"{url}{title}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _fetch_rss(self, rss_url: str) -> list:
        """Fetch and parse RSS feed."""
        try:
            feed = feedparser.parse(rss_url)
            entries = []
            for entry in feed.entries:
                entries.append({
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'date': entry.get('published', entry.get('updated', '')),
                    'content': entry.get('summary', entry.get('description', ''))
                })
            return entries
        except Exception as e:
            print(f"Error fetching RSS {rss_url}: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse date string to ISO format."""
        if not date_str:
            return None
        try:
            parsed = date_parser.parse(date_str)
            return parsed.strftime('%Y-%m-%d')
        except Exception:
            return None
    
    def _is_within_backfill_range(self, date_str: Optional[str]) -> bool:
        """Check if date is within backfill range."""
        if not date_str:
            return True  # Include if no date
        if not self.config.get('backfill', {}).get('enabled', False):
            return True
            
        start_date = self.config['backfill'].get('start_date', '2024-01-01')
        try:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d')
            backfill_start = datetime.strptime(start_date, '%Y-%m-%d')
            return entry_date >= backfill_start
        except Exception:
            return True
    
    def crawl_source(self, source: dict) -> list:
        """Crawl a single source for articles."""
        print(f"Crawling {source['name']}...")
        entries = []
        
        # Try RSS first if available
        if source.get('rss_url'):
            rss_entries = self._fetch_rss(source['rss_url'])
            for entry in rss_entries:
                date = self._parse_date(entry['date'])
                if not self._is_within_backfill_range(date):
                    continue
                    
                entries.append({
                    'id': self._generate_id(entry['url'], entry['title']),
                    'title': entry['title'],
                    'source': source['name'],
                    'url': entry['url'],
                    'date': date,
                    'content': entry['content'],
                    'summary': None,
                    'category': 'Other',
                    'tags': []
                })
        else:
            # Fall back to HTML scraping
            soup = self._fetch_page(source['url'])
            if soup:
                selectors = source.get('selectors', {})
                articles = soup.select(selectors.get('article_list', 'article'))
                
                for article in articles[:20]:  # Limit to 20 per source
                    title_elem = article.select_one(selectors.get('title', 'h2'))
                    date_elem = article.select_one(selectors.get('date', 'time'))
                    link_elem = article.select_one(selectors.get('link', 'a'))
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    # Handle relative URLs
                    if url and not url.startswith('http'):
                        base_url = source['url'].rstrip('/')
                        url = f"{base_url}/{url.lstrip('/')}"
                    
                    date_str = date_elem.get('datetime', date_elem.get_text(strip=True)) if date_elem else None
                    date = self._parse_date(date_str)
                    
                    if not self._is_within_backfill_range(date):
                        continue
                    
                    entries.append({
                        'id': self._generate_id(url, title),
                        'title': title,
                        'source': source['name'],
                        'url': url,
                        'date': date,
                        'content': article.get_text(strip=True)[:500],
                        'summary': None,
                        'category': 'Other',
                        'tags': []
                    })
        
        print(f"  Found {len(entries)} entries from {source['name']}")
        return entries
    
    def crawl_all(self) -> list:
        """Crawl all configured sources."""
        all_entries = []
        
        for source in self.config.get('sources', []):
            entries = self.crawl_source(source)
            all_entries.extend(entries)
        
        # Remove duplicates by ID
        seen_ids = set()
        unique_entries = []
        for entry in all_entries:
            if entry['id'] not in seen_ids:
                seen_ids.add(entry['id'])
                unique_entries.append(entry)
        
        # Sort by date (newest first)
        unique_entries.sort(key=lambda x: x['date'] or '1900-01-01', reverse=True)
        
        return unique_entries
    
    def generate_summaries(self, entries: list) -> list:
        """Generate summaries for entries using Copilot SDK."""
        print("Generating summaries...")
        for entry in entries:
            if not entry.get('summary') and entry.get('content'):
                entry['summary'] = self.summarizer.summarize(
                    title=entry['title'],
                    content=entry['content'],
                    source=entry['source']
                )
        return entries
    
    def save_entries(self, entries: list):
        """Save entries to JSON file."""
        output_path = Path(self.config['output']['path'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'last_updated': datetime.utcnow().isoformat() + 'Z',
            'entries': entries
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(entries)} entries to {output_path}")
    
    def run(self):
        """Run the full crawl pipeline."""
        print("Starting crawler...")
        
        # Crawl all sources
        entries = self.crawl_all()
        
        # Generate summaries
        entries = self.generate_summaries(entries)
        
        # Save to file
        self.save_entries(entries)
        
        print("Crawl complete!")
        return entries


if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()

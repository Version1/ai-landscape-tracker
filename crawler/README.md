# Agentic AI Landscape Tracker - Crawler

Python-based web crawler that fetches and summarizes AI news from major players.

## Setup

```bash
cd crawler
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to:
- Add/remove sources
- Adjust backfill date range
- Modify output path
- Configure crawler behavior (delays, retries, timeout)

### Crawler Settings

```yaml
crawler:
  delay_between_requests: 1  # Seconds between requests (be respectful)
  max_retries: 3  # Retry attempts for failed requests
  timeout: 30  # Request timeout in seconds
```

## Usage

```bash
cd crawler/src
python crawler.py
```

## Troubleshooting

### 403 Forbidden Errors

Some websites block automated scrapers. The crawler implements:

**Built-in Mitigations:**
- Enhanced browser headers to mimic real browsers
- Automatic retry with exponential backoff
- Configurable delays between requests
- Session management with connection pooling

**If 403 errors persist:**

1. **Use RSS feeds instead** - Check if the site offers RSS/Atom feeds:
   ```yaml
   rss_url: "https://example.com/blog/rss.xml"
   ```

2. **Increase delays** - Be more respectful with request timing:
   ```yaml
   crawler:
     delay_between_requests: 3  # Increase from 1 to 3+ seconds
   ```

3. **Check robots.txt** - Verify the site allows crawling:
   ```
   https://example.com/robots.txt
   ```

4. **Consider alternatives:**
   - Official APIs (e.g., OpenAI's API)
   - Newsletter subscriptions
   - Manual updates for protected sources

### Current Known Issues

**FIXED Issues:**
- ~~**Anthropic**: Uses JavaScript-rendered content~~ - **RESOLVED**: Site works with proper Accept-Encoding handling
- ~~**Cursor**: Returning 0 entries~~ - **RESOLVED**: Fixed Accept-Encoding header and URL construction
- ~~**OpenAI**: 403 Forbidden errors~~ - **RESOLVED**: Using RSS feed instead

**Working Sources:**
- ✅ Anthropic - Scraping news page (4+ entries)
- ✅ Cursor - Scraping changelog (10+ entries)
- ✅ GitHub Copilot - RSS feed with HTML cleaning (10+ entries)
- ✅ OpenAI - RSS feed (534+ entries)
- ✅ Google DeepMind - Scraping blog (20+ entries)

### Key Fixes Applied

1. **Accept-Encoding Header Issue**: Removed explicit `Accept-Encoding: gzip, deflate, br` header
   - When explicitly set, requests library doesn't auto-decompress
   - Now lets requests handle compression automatically
   - Affected: Anthropic, Cursor (both now working)

2. **URL Construction for Absolute Paths**: Fixed `/news/` type paths
   - Paths starting with `/` are now resolved from domain root
   - Paths without leading `/` are resolved relative to source URL
   - Fixed double-path issue (e.g., `/news/news/` → `/news/`)

3. **RSS Feed Fallback**: Using RSS feeds where available (OpenAI, GitHub Copilot)
   - More reliable than scraping for bot-protected sites
   - Includes HTML tag stripping for clean content

### JavaScript-Rendered Sites

Previously, sites like Anthropic and Cursor were thought to require browser automation due to JavaScript rendering. However, the actual issue was with HTTP request handling:

**Root Cause**: Explicitly setting `Accept-Encoding: gzip, deflate, br` prevents automatic decompression in the requests library.

**Solution**: Remove the explicit Accept-Encoding header and let requests handle compression automatically.

**When Browser Automation IS Actually Needed:**
- Sites that genuinely require JavaScript execution to render content
- Dynamic content loaded after page load via AJAX/fetch
- Sites with complex authentication or anti-bot measures

**Current Status**: All configured sources work with simple HTTP requests after fixing header issues.

## Sources

Currently configured sources:
- Anthropic (blog)
- Cursor (changelog)
- GitHub Copilot (blog + RSS)
- OpenAI (blog + RSS fallback)
- Google DeepMind (blog)

## LLM Integration

Uses GitHub Copilot SDK for generating summaries. Requires:
- GitHub Copilot subscription
- Copilot CLI installed

Falls back to basic text extraction if SDK unavailable.

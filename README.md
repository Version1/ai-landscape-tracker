# AI Landscape Tracker

A curated, automatically updated portal tracking AI developments from major players including Anthropic, Cursor, GitHub Copilot, OpenAI, and Google DeepMind.

## Features

- **Automated Content Crawling**: Monitors RSS/Atom feeds and blogs for latest AI news
- **AI-Powered Categorization**: Automatically categorizes entries as "Agentic AI" or "Other"
  - **Agentic AI**: AI agents, autonomous systems, tool use, workflows, multi-agent systems
  - **Other**: General models, partnerships, policy, infrastructure, research
- **Confidence Scoring**: Each categorization includes a confidence level (0-100)
- **Content Summaries**: Concise summaries for each entry
- **Timeline View**: Chronological feed with filtering and search capabilities
- **Version 1 Branding**: Professional design following brand guidelines

## Current Statistics

- **Total Entries**: 581
- **Agentic AI**: 96 entries (16.5%)
- **Other**: 485 entries (83.5%)
- **Last Updated**: January 31, 2026

## Architecture

```
├── crawler/          # Python crawler application
│   ├── src/          # Source code (crawler.py, summarizer.py)
│   ├── data/         # Crawled data
│   │   └── entries.json
│   ├── config.yaml   # Source configuration
│   ├── requirements.txt
│   └── tests/        # Unit tests
│
├── site/             # Static website (GitHub Pages)
│   ├── index.html
│   ├── css/styles.css
│   ├── js/app.js
│   └── data/
│       ├── entries.json      # Processed entries with categories
│       └── entries raw.json  # Original crawled data
│
├── tests/            # End-to-end tests
│   ├── e2e/
│   └── playwright.config.ts
│
├── Councils of Agents/  # Agent persona definitions
│
└── .github/workflows/   # Automation
    └── crawl-and-deploy.yml
```

## Data Structure

Each entry in `entries.json` contains:

```json
{
  "id": "unique-id",
  "title": "Entry title",
  "source": "OpenAI",
  "url": "https://...",
  "date": "2026-01-31",
  "content": "Full content text",
  "summary": "Concise summary",
  "category": "Agentic AI",
  "categoryConfidence": 85,
  "tags": []
}
```

## Local Development

### Crawler
```bash
cd crawler
pip install -r requirements.txt
python test_urls.py  # Test source URLs
cd src
python crawler.py    # Run crawler
```

### Processing & Categorization
```bash
# Process entries with categorization
python process_entries_basic.py

# Or use AI-powered processing (requires GitHub Copilot SDK)
python summarize_entries.py
```

### Website
Open `site/index.html` in a browser, or use a local server:
```bash
cd site
python -m http.server 8000
# Visit http://localhost:8000
```

### Testing
```bash
# Run crawler tests
cd crawler
pytest tests/

# Run E2E tests
cd tests
npm install
npx playwright test
```

## Deployment

1. Push to GitHub
2. Enable GitHub Pages (Settings → Pages → Source: GitHub Actions)
3. The workflow will automatically:
   - Run crawler every 12 hours
   - Commit updated data
   - Deploy to GitHub Pages

## Adding Sources

Edit `crawler/config.yaml` to add new sources:

```yaml
sources:
  - name: "New Source"
    type: "blog"
    url: "https://example.com/blog"
    selectors:
      article_list: "article"
      title: "h2"
      date: "time"
      link: "a"
```

## Categorization

The system categorizes entries into two categories:

### Agentic AI
Entries related to AI systems that can:
- Take autonomous actions
- Use tools and function calling
- Plan and execute workflows
- Operate in multi-agent systems
- Orchestrate complex tasks

Examples: AI agents, Codex, workflow automation, tool-using AI

### Other
All other AI developments including:
- General AI models and capabilities
- Enterprise adoption and partnerships
- Policy, governance, and infrastructure
- Research without agentic components
- Educational initiatives

## Project Structure

- **`crawler/`**: Python-based web crawler for collecting AI news
- **`site/`**: Frontend application for displaying the tracker
- **`tests/`**: End-to-end testing with Playwright
- **`Councils of Agents/`**: AI agent persona definitions for different use cases
- **`Documentation/`**: Project documentation and SDLC artifacts

## Scripts

- **`process_entries_basic.py`**: Keyword-based categorization
- **`summarize_entries.py`**: AI-powered summarization (requires API key)
- **`processing_summary.md`**: Latest processing statistics

## License

Internal use - Version 1

# Agentic AI Landscape Tracker

A curated, automatically updated portal tracking developments in the Agentic AI space from major players including Anthropic, Cursor, GitHub Copilot, OpenAI, and Google DeepMind.

## Features

- **AI Summaries**: Brief 2-3 sentence summaries generated using GitHub Copilot SDK
- **Timeline View**: Chronological feed with filtering and search
- **Version 1 Branding**: Professional design following brand guidelines

## Architecture

```
├── crawler/          # Python crawler application
│   ├── src/          # Source code
│   ├── config.yaml   # Source configuration
│   └── requirements.txt
│
├── site/             # Static website (GitHub Pages)
│   ├── index.html
│   ├── css/
│   └── js/
│
├── data/             # Crawled content (JSON)
│   └── entries.json
│
└── .github/workflows/  # Automation
    └── crawl-and-deploy.yml
```

## Local Development

### Crawler
```bash
cd crawler
pip install -r requirements.txt
cd src
python crawler.py
```

### Website
Open `site/index.html` in a browser, or use a local server:
```bash
cd site
python -m http.server 8000
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

## License

Internal use - Version 1

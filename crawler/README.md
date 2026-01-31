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

## Usage

```bash
cd crawler/src
python crawler.py
```

## Sources

Currently configured sources:
- Anthropic (blog)
- Cursor (changelog)
- GitHub Copilot (blog + RSS)
- OpenAI (blog)
- Google DeepMind (blog)

## LLM Integration

Uses GitHub Copilot SDK for generating summaries. Requires:
- GitHub Copilot subscription
- Copilot CLI installed

Falls back to basic text extraction if SDK unavailable.

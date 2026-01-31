# Test Suite

Comprehensive test coverage for the Agentic AI Landscape Tracker.

## Test Structure

```
tests/
├── e2e/                    # Playwright E2E tests
│   └── site.spec.ts       # Site functionality tests
├── playwright.config.ts    # Playwright configuration
└── package.json           # Node dependencies

crawler/tests/
├── test_crawler.py        # Unit tests for crawler
├── test_summarizer.py     # Unit tests for summarizer
└── test_integration.py    # Integration tests
```

## Running Tests

### Python Unit Tests

```bash
cd crawler
pip install -r requirements.txt
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Playwright E2E Tests

```bash
cd tests
npm install
npx playwright install
npm test
```

Interactive mode:
```bash
npm run test:ui
```

Debug mode:
```bash
npm run test:debug
```

Specific browser:
```bash
npm run test:chromium
npm run test:firefox
npm run test:webkit
```

Mobile tests:
```bash
npm run test:mobile
```

## Test Coverage

### Unit Tests (Python)
- Crawler ID generation and uniqueness
- Date parsing (ISO, human-readable, invalid)
- Backfill range validation
- Configuration loading
- Summarizer initialization
- Fallback summarization logic

### Integration Tests (Python)
- Full crawler workflow
- Entry deduplication
- Date-based sorting
- Summary generation
- JSON output validation

### E2E Tests (Playwright)
- Page loads correctly
- Header and branding display
- Filter controls present
- Entries load and display
- Source filtering
- Category filtering
- Search functionality
- Combined filters
- Filter reset
- Empty state handling
- External links (target="_blank")
- Mobile responsiveness
- Hover effects

## CI/CD Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests
- Manual workflow dispatch

See `.github/workflows/test.yml` for CI configuration.

## Test Reports

- **Unit test coverage**: `crawler/htmlcov/index.html`
- **Playwright report**: `tests/playwright-report/index.html`

Generate reports locally:
```bash
# Python coverage
cd crawler && pytest tests/ --cov=src --cov-report=html

# Playwright report
cd tests && npm run report
```

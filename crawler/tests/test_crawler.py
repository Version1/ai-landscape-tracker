"""
Unit tests for crawler functionality
"""

import pytest
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from crawler import Crawler


class TestCrawler:
    """Test Crawler class"""
    
    @pytest.fixture
    def crawler(self, tmp_path):
        """Create crawler instance with test config"""
        config_path = tmp_path / "test_config.yaml"
        config_path.write_text("""
output:
  path: "test_output.json"
  
backfill:
  enabled: true
  start_date: "2024-01-01"

sources:
  - name: "Test Source"
    type: "blog"
    url: "https://example.com"
    selectors:
      article_list: "article"
      title: "h2"
      date: "time"
      link: "a"

categories:
  - "Release"
  - "Feature"
""")
        return Crawler(str(config_path))
    
    def test_generate_id(self, crawler):
        """Test ID generation is consistent"""
        id1 = crawler._generate_id("https://example.com", "Test Title")
        id2 = crawler._generate_id("https://example.com", "Test Title")
        assert id1 == id2
        assert len(id1) == 12
    
    def test_generate_id_unique(self, crawler):
        """Test different inputs generate different IDs"""
        id1 = crawler._generate_id("https://example.com", "Title 1")
        id2 = crawler._generate_id("https://example.com", "Title 2")
        assert id1 != id2
    
    def test_parse_date_iso(self, crawler):
        """Test parsing ISO date format"""
        result = crawler._parse_date("2024-01-15T10:30:00Z")
        assert result == "2024-01-15"
    
    def test_parse_date_human(self, crawler):
        """Test parsing human-readable date"""
        result = crawler._parse_date("January 15, 2024")
        assert result == "2024-01-15"
    
    def test_parse_date_invalid(self, crawler):
        """Test parsing invalid date returns None"""
        result = crawler._parse_date("invalid date")
        assert result is None
    
    def test_is_within_backfill_range_recent(self, crawler):
        """Test recent date is within backfill range"""
        assert crawler._is_within_backfill_range("2024-06-01") is True
    
    def test_is_within_backfill_range_old(self, crawler):
        """Test old date is outside backfill range"""
        assert crawler._is_within_backfill_range("2023-12-31") is False
    
    def test_is_within_backfill_range_no_date(self, crawler):
        """Test None date is included"""
        assert crawler._is_within_backfill_range(None) is True
    
    def test_config_loading(self, crawler):
        """Test configuration is loaded correctly"""
        assert crawler.config is not None
        assert 'output' in crawler.config
        assert 'sources' in crawler.config
        assert len(crawler.config['sources']) == 1

"""
Integration tests for full crawler workflow
"""

import pytest
import json
from pathlib import Path
import sys
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from crawler import Crawler


class TestCrawlerIntegration:
    """Integration tests for complete crawler workflow"""
    
    @pytest.fixture
    def test_config(self, tmp_path):
        """Create test configuration"""
        config_path = tmp_path / "test_config.yaml"
        output_path = tmp_path / "output.json"
        
        config_path.write_text(f"""
output:
  path: "{output_path}"
  
backfill:
  enabled: false

sources:
  - name: "Test Source"
    type: "blog"
    url: "https://example.com"
    rss_url: null
    selectors:
      article_list: "article"
      title: "h2"
      date: "time"
      link: "a"

categories:
  - "Release"
  - "Feature"
""")
        return str(config_path), str(output_path)
    
    def test_save_entries(self, test_config):
        """Test saving entries to JSON file"""
        config_path, output_path = test_config
        crawler = Crawler(config_path)
        
        test_entries = [
            {
                'id': 'test123',
                'title': 'Test Article',
                'source': 'Test Source',
                'url': 'https://example.com/article',
                'date': '2024-01-15',
                'summary': 'Test summary',
                'category': 'Release',
                'tags': []
            }
        ]
        
        crawler.save_entries(test_entries)
        
        # Verify file exists
        assert Path(output_path).exists()
        
        # Verify content
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert 'last_updated' in data
        assert 'entries' in data
        assert len(data['entries']) == 1
        assert data['entries'][0]['id'] == 'test123'
    
    def test_crawl_all_deduplication(self, test_config):
        """Test that duplicate entries are removed"""
        config_path, _ = test_config
        crawler = Crawler(config_path)
        
        # Mock crawl_source to return duplicates
        duplicate_entries = [
            {
                'id': 'same123',
                'title': 'Same Article',
                'source': 'Test Source',
                'url': 'https://example.com/article',
                'date': '2024-01-15',
                'content': 'Test',
                'summary': None,
                'category': 'Release',
                'tags': []
            },
            {
                'id': 'same123',  # Duplicate ID
                'title': 'Same Article',
                'source': 'Test Source',
                'url': 'https://example.com/article',
                'date': '2024-01-15',
                'content': 'Test',
                'summary': None,
                'category': 'Release',
                'tags': []
            }
        ]
        
        with patch.object(crawler, 'crawl_source', return_value=duplicate_entries):
            result = crawler.crawl_all()
        
        # Should only have 1 entry after deduplication
        assert len(result) == 1
        assert result[0]['id'] == 'same123'
    
    def test_crawl_all_sorting(self, test_config):
        """Test that entries are sorted by date (newest first)"""
        config_path, _ = test_config
        crawler = Crawler(config_path)
        
        unsorted_entries = [
            {
                'id': 'old123',
                'title': 'Old Article',
                'source': 'Test Source',
                'url': 'https://example.com/old',
                'date': '2024-01-01',
                'content': 'Test',
                'summary': None,
                'category': 'Release',
                'tags': []
            },
            {
                'id': 'new123',
                'title': 'New Article',
                'source': 'Test Source',
                'url': 'https://example.com/new',
                'date': '2024-06-01',
                'content': 'Test',
                'summary': None,
                'category': 'Release',
                'tags': []
            }
        ]
        
        with patch.object(crawler, 'crawl_source', return_value=unsorted_entries):
            result = crawler.crawl_all()
        
        # Newest should be first
        assert result[0]['id'] == 'new123'
        assert result[1]['id'] == 'old123'
    
    @patch('crawler.Summarizer')
    def test_generate_summaries(self, mock_summarizer_class, test_config):
        """Test summary generation for entries"""
        config_path, _ = test_config
        crawler = Crawler(config_path)
        
        # Mock summarizer
        mock_summarizer = Mock()
        mock_summarizer.summarize.return_value = "Generated summary"
        crawler.summarizer = mock_summarizer
        
        entries = [
            {
                'id': 'test123',
                'title': 'Test Article',
                'source': 'Test Source',
                'url': 'https://example.com/article',
                'date': '2024-01-15',
                'content': 'Article content here',
                'summary': None,
                'category': 'Release',
                'tags': []
            }
        ]
        
        result = crawler.generate_summaries(entries)
        
        # Verify summarizer was called
        mock_summarizer.summarize.assert_called_once()
        
        # Verify summary was added
        assert result[0]['summary'] == "Generated summary"

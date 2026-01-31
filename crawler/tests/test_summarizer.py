"""
Unit tests for summarizer functionality
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from summarizer import Summarizer


class TestSummarizer:
    """Test Summarizer class"""
    
    @pytest.fixture
    def summarizer(self):
        """Create summarizer instance"""
        return Summarizer()
    
    def test_summarizer_initialization(self, summarizer):
        """Test summarizer initializes"""
        assert summarizer is not None
    
    def test_fallback_summarize_short_content(self, summarizer):
        """Test fallback with short content"""
        result = summarizer._fallback_summarize(
            title="Test Title",
            content="Short content here.",
            source="Test Source"
        )
        assert result == "Short content here."
    
    def test_fallback_summarize_long_content(self, summarizer):
        """Test fallback truncates long content"""
        long_content = "A" * 300
        result = summarizer._fallback_summarize(
            title="Test Title",
            content=long_content,
            source="Test Source"
        )
        assert len(result) <= 203  # 200 + "..."
        assert result.endswith("...")
    
    def test_fallback_summarize_sentences(self, summarizer):
        """Test fallback extracts sentences"""
        content = "First sentence here. Second sentence here. Third sentence."
        result = summarizer._fallback_summarize(
            title="Test Title",
            content=content,
            source="Test Source"
        )
        assert "First sentence" in result
        assert len(result) <= 300
    
    def test_summarize_empty_content(self, summarizer):
        """Test summarize with empty content"""
        result = summarizer.summarize(
            title="Test Title",
            content="",
            source="Test Source"
        )
        assert "Test Source" in result
        assert "Test Title" in result
    
    def test_summarize_with_content(self, summarizer):
        """Test summarize with actual content"""
        result = summarizer.summarize(
            title="New AI Model Released",
            content="Company X has released a new AI model with improved capabilities.",
            source="Company X"
        )
        assert len(result) > 0
        assert isinstance(result, str)

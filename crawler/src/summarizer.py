"""
Agentic AI Landscape Tracker - LLM Summarizer
Uses GitHub Copilot SDK to generate brief summaries.
"""

from typing import Optional


class Summarizer:
    """Generate summaries using GitHub Copilot SDK."""
    
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize the Copilot SDK client."""
        try:
            from github_copilot_sdk import CopilotClient
            self.client = CopilotClient()
        except ImportError:
            print("Warning: github-copilot-sdk not installed. Summaries will use fallback.")
            self.client = None
        except Exception as e:
            print(f"Warning: Could not initialize Copilot SDK: {e}")
            self.client = None
    
    def summarize(self, title: str, content: str, source: str) -> str:
        """
        Generate a 2-3 sentence summary of an AI announcement.
        
        Args:
            title: Article title
            content: Article content/excerpt
            source: Source name (e.g., "Anthropic", "Cursor")
            
        Returns:
            Brief summary string
        """
        if not content:
            return f"New update from {source}: {title}"
        
        # If Copilot SDK available, use it
        if self.client:
            return self._summarize_with_copilot(title, content, source)
        
        # Fallback: extract first meaningful sentences
        return self._fallback_summarize(title, content, source)
    
    def _summarize_with_copilot(self, title: str, content: str, source: str) -> str:
        """Generate summary using GitHub Copilot SDK."""
        prompt = f"""Summarize this AI/tech announcement in 2-3 concise sentences.
Focus on: what was announced, key capabilities, and why it matters.

Source: {source}
Title: {title}
Content: {content[:1000]}

Summary:"""
        
        try:
            response = self.client.complete(
                prompt=prompt,
                max_tokens=150,
                temperature=0.3
            )
            summary = response.strip()
            return summary if summary else self._fallback_summarize(title, content, source)
        except Exception as e:
            print(f"Copilot summarization failed: {e}")
            return self._fallback_summarize(title, content, source)
    
    def _fallback_summarize(self, title: str, content: str, source: str) -> str:
        """Fallback summarization when Copilot SDK unavailable."""
        # Clean and truncate content
        content = content.strip()
        
        # Find first sentence(s)
        sentences = []
        for sep in ['. ', '! ', '? ']:
            if sep in content:
                parts = content.split(sep)
                sentences.extend(parts[:2])
                break
        
        if sentences:
            summary = '. '.join(s.strip() for s in sentences[:2] if s.strip())
            if summary and not summary.endswith('.'):
                summary += '.'
            return summary[:300]
        
        # Last resort: truncate content
        return content[:200] + '...' if len(content) > 200 else content


if __name__ == '__main__':
    # Test summarizer
    summarizer = Summarizer()
    test_summary = summarizer.summarize(
        title="Claude 3.5 Sonnet Released",
        content="Anthropic has released Claude 3.5 Sonnet, their most capable model yet. It features improved reasoning, faster response times, and enhanced coding abilities.",
        source="Anthropic"
    )
    print(f"Test summary: {test_summary}")

"""
Process entries from 'entries raw.json' and add:
- Improved summary
- Category (Agentic AI or Other)
- Confidence level

This script is designed to be run with Claude as the processing engine.
"""

import json
from pathlib import Path

def load_entries():
    """Load entries from the raw JSON file"""
    input_path = Path("c:/Users/VilhenaM/Cursor_VSCode Workspaces/ai-landscape-tracker/site/data/entries raw.json")
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_entries(data):
    """Save processed entries to the output file"""
    output_path = Path("c:/Users/VilhenaM/Cursor_VSCode Workspaces/ai-landscape-tracker/site/data/entries.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {output_path}")

def analyze_entry(entry):
    """
    Analyze entry and return categorization.
    This needs to be filled in with actual AI analysis.
    """
    title = entry.get('title', '').lower()
    content = entry.get('content', '').lower()
    text = title + " " + content
    
    # Keywords that suggest Agentic AI
    agentic_keywords = [
        'agent', 'agentic', 'autonomous', 'tool use', 'function calling',
        'workflow', 'orchestration', 'multi-agent', 'task planning',
        'action', 'execute', 'codex', 'automation'
    ]
    
    # Check for agentic keywords
    agentic_score = sum(1 for keyword in agentic_keywords if keyword in text)
    
    # Basic categorization logic
    if agentic_score >= 2:
        category = "Agentic AI"
        confidence = min(70 + (agentic_score * 5), 95)
    elif agentic_score == 1:
        category = "Agentic AI"
        confidence = 60
    else:
        category = "Other"
        confidence = 75
    
    # Create a better summary from content
    content_str = entry.get('content', '')
    if len(content_str) > 200:
        summary = content_str[:197] + "..."
    else:
        summary = content_str
    
    return {
        'summary': summary,
        'category': category,
        'categoryConfidence': confidence
    }

def main():
    # Load data
    data = load_entries()
    entries = data['entries']
    
    print(f"Processing {len(entries)} entries...")
    print("\nThis is a placeholder script.")
    print("For accurate AI-powered categorization, each entry should be")
    print("analyzed individually with proper AI context.")
    print("\nPlease run this with Claude to process entries properly.")
    
    # Process each entry (basic version)
    for i, entry in enumerate(entries):
        if (i + 1) % 50 == 0:
            print(f"Processed {i+1}/{len(entries)} entries...")
        
        result = analyze_entry(entry)
        entry['summary'] = result['summary']
        entry['category'] = result['category']
        entry['categoryConfidence'] = result['categoryConfidence']
    
    # Save results
    save_entries(data)
    
    # Statistics
    agentic_count = sum(1 for e in entries if e.get('category') == 'Agentic AI')
    other_count = len(entries) - agentic_count
    avg_confidence = sum(e.get('categoryConfidence', 0) for e in entries) / len(entries)
    
    print(f"\nStatistics:")
    print(f"  Total entries: {len(entries)}")
    print(f"  Agentic AI: {agentic_count}")
    print(f"  Other: {other_count}")
    print(f"  Average Confidence: {avg_confidence:.1f}%")

if __name__ == "__main__":
    main()

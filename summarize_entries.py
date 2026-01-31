import json
import anthropic
import os
from pathlib import Path

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def categorize_and_summarize_entry(entry):
    """
    Analyze an entry and return:
    - A concise summary
    - Category (Agentic AI or Other)
    - Confidence level (0-100)
    """
    
    # Prepare the prompt
    prompt = f"""Analyze this AI news entry and provide:
1. A concise 1-2 sentence summary of the content
2. Choose the best category: "Agentic AI" or "Other"
   - "Agentic AI" = AI systems that can take actions, make decisions, use tools, plan, or operate autonomously
   - "Other" = General AI models, applications, partnerships, policy, infrastructure, etc.
3. Your confidence level (0-100) in the category choice

Entry:
Title: {entry.get('title', '')}
Source: {entry.get('source', '')}
Content: {entry.get('content', '')}

Respond in this exact JSON format:
{{
  "summary": "your summary here",
  "category": "Agentic AI" or "Other",
  "confidence": 85
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        response_text = message.content[0].text
        
        # Extract JSON from the response
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            print(f"Warning: Could not parse response for entry {entry.get('id')}")
            return {
                "summary": entry.get('content', '')[:200],
                "category": "Other",
                "confidence": 50
            }
            
    except Exception as e:
        print(f"Error processing entry {entry.get('id')}: {e}")
        return {
            "summary": entry.get('content', '')[:200],
            "category": "Other",
            "confidence": 0
        }

def process_entries():
    """Process all entries in the raw JSON file"""
    
    # Read the input file
    input_path = Path("c:/Users/VilhenaM/Cursor_VSCode Workspaces/ai-landscape-tracker/site/data/entries raw.json")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data['entries'])} entries...")
    
    # Process each entry
    for i, entry in enumerate(data['entries']):
        print(f"Processing entry {i+1}/{len(data['entries'])}: {entry.get('title', 'Untitled')}")
        
        result = categorize_and_summarize_entry(entry)
        
        # Update the entry
        entry['summary'] = result['summary']
        entry['category'] = result['category']
        entry['categoryConfidence'] = result['confidence']
        
        # Progress indicator every 10 entries
        if (i + 1) % 10 == 0:
            print(f"  ... {i+1} entries processed")
    
    # Write back to the file
    output_path = Path("c:/Users/VilhenaM/Cursor_VSCode Workspaces/ai-landscape-tracker/site/data/entries.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete! Processed {len(data['entries'])} entries.")
    print(f"Output saved to: {output_path}")
    
    # Print statistics
    agentic_count = sum(1 for e in data['entries'] if e.get('category') == 'Agentic AI')
    other_count = len(data['entries']) - agentic_count
    avg_confidence = sum(e.get('categoryConfidence', 0) for e in data['entries']) / len(data['entries'])
    
    print(f"\nStatistics:")
    print(f"  Agentic AI: {agentic_count}")
    print(f"  Other: {other_count}")
    print(f"  Average Confidence: {avg_confidence:.1f}")

if __name__ == "__main__":
    process_entries()

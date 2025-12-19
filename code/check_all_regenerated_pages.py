#!/usr/bin/env python3
"""
Check all pages that were supposedly regenerated to identify which have wrong/duplicate content.
"""

from pathlib import Path

# Pages that were regenerated from non-square originals
REGENERATED_PAGES = [
    {"page_num": 26, "original_file": "page26.png", "original_size": "2368x1792", "prompt_file": "page-26.md"},
    {"page_num": 27, "original_file": "page27.png", "original_size": "2368x1792", "prompt_file": "page-27.md"},
    {"page_num": 28, "original_file": "page28.jpg", "original_size": "687x1024", "prompt_file": "page-28.md"},
    {"page_num": 31, "original_file": "page31.png", "original_size": "2816x1536", "prompt_file": "page-31.md"},
    {"page_num": 33, "original_file": "page33.png", "original_size": "2816x1536", "prompt_file": "page-33.md"},
    {"page_num": 34, "original_file": "page34.png", "original_size": "1184x896", "prompt_file": "page-34.md"},
    {"page_num": 40, "original_file": "page40.png", "original_size": "1152x896", "prompt_file": "page-40.md"},
    {"page_num": 41, "original_file": "page41.png", "original_size": "1152x896", "prompt_file": "page-41.md"},
    {"page_num": 42, "original_file": "page42.png", "original_size": "832x1248", "prompt_file": "page-42.md"},
    {"page_num": 43, "original_file": "page43.png", "original_size": "832x1248", "prompt_file": "page-43.md"},
    {"page_num": 44, "original_file": "page44.png", "original_size": "1472x704", "prompt_file": "page-44.md"},
    {"page_num": 45, "original_file": "page45.png", "original_size": "832x1248", "prompt_file": "page-45.md"},
    {"page_num": 46, "original_file": "page46.png", "original_size": "1152x896", "prompt_file": "page-46.md"},
    {"page_num": 47, "original_file": "page-47-back-cover-montage.png", "original_size": "1876x1900", "prompt_file": "page-47-back-cover.md"},
]

# Map current page numbers to original illustration numbers for text lookup
PAGE_MAPPING = {
    26: 24, 27: 25, 28: 26, 29: 27, 30: 28, 31: 29, 32: 30, 33: 31, 34: 32, 35: 33,
    36: 34, 37: 35, 38: 36, 39: 37, 40: 38, 41: 39, 42: 40, 43: 41, 44: 42, 45: 43, 
    46: 44, 47: 45
}

def get_page_text(page_num):
    """Get the page text to understand what the page should show."""
    prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    if not prompt_file.exists():
        return "File not found"
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Extract PAGE TEXT section
    lines = content.split('\n')
    page_text = ""
    in_page_text = False
    
    for line in lines:
        if line.strip().startswith("## PAGE TEXT"):
            in_page_text = True
            continue
        elif line.strip().startswith("## ") and in_page_text:
            break
        elif in_page_text and line.strip():
            page_text += line.strip() + " "
    
    return page_text.strip()

def get_image_prompt_snippet(page_num):
    """Get a snippet of the image prompt to see what it should show."""
    prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    if not prompt_file.exists():
        return "File not found"
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Extract first part of IMAGE PROMPT section
    lines = content.split('\n')
    in_image_prompt = False
    prompt_snippet = ""
    
    for line in lines:
        if line.strip().startswith("## IMAGE PROMPT"):
            in_image_prompt = True
            continue
        elif line.strip().startswith("Create a modern 2D cartoon") and in_image_prompt:
            # Get the main description line
            prompt_snippet = line.strip()
            break
        elif in_image_prompt and line.strip() and not line.startswith("**"):
            prompt_snippet = line.strip()
            break
    
    return prompt_snippet

def check_for_phone_reviews_prompt(page_num):
    """Check if a page has the wrong phone/reviews prompt."""
    prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    if not prompt_file.exists():
        return False
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Look for telltale signs of the phone/reviews prompt
    indicators = [
        "holding up his smartphone",
        "3D holographic **THUMBS UP**",
        "holographic phone effects",
        "reading glowing reviews",
        "during the peak success period"
    ]
    
    content_lower = content.lower()
    matches = sum(1 for indicator in indicators if indicator.lower() in content_lower)
    
    return matches >= 2  # If 2+ indicators, likely wrong prompt

def main():
    """Check all regenerated pages for issues."""
    print("🔍 Checking all regenerated pages for content accuracy...\n")
    
    issues = []
    
    for page_info in REGENERATED_PAGES:
        page_num = page_info["page_num"]
        
        print(f"📄 Page {page_num} (originally {page_info['original_size']}):")
        
        # Get what the page should show
        page_text = get_page_text(page_num)
        prompt_snippet = get_image_prompt_snippet(page_num)
        has_wrong_prompt = check_for_phone_reviews_prompt(page_num)
        
        print(f"   Text: {page_text[:100]}{'...' if len(page_text) > 100 else ''}")
        print(f"   Prompt: {prompt_snippet[:80]}{'...' if len(prompt_snippet) > 80 else ''}")
        
        # Check for issues
        if has_wrong_prompt:
            issues.append({
                "page": page_num,
                "issue": "Wrong prompt (phone/reviews instead of career fantasy)",
                "text": page_text[:50] + "..."
            })
            print("   🚨 ISSUE: Has wrong phone/reviews prompt!")
        elif "phone" in page_text.lower() or "review" in page_text.lower():
            print("   ✅ Phone/reviews content (correct)")
        else:
            # Check if image matches text content
            key_words = []
            text_lower = page_text.lower()
            
            career_keywords = {
                "politics": ["politics", "office", "aoc", "debate", "speech"],
                "librarian": ["librarian", "library", "scholarship", "research"],
                "truck": ["truck", "driver", "semi", "highway"],
                "lawyer": ["lawyer", "legal", "court", "case"],
                "podcast": ["podcast", "microphone", "show", "broadcast"],
                "gamer": ["gamer", "gaming", "video", "controller"],
                "mattress": ["mattress", "tester", "sleep", "bed"],
                "hamster": ["hamster", "guard", "lobster", "fisher"],
                "golf": ["golf", "ball", "diver", "underwater"],
                "water": ["water", "slide", "netflix", "line"],
                "food": ["food", "styling", "photo", "beautiful"],
                "stock": ["stock", "photo", "model", "pose"],
                "yodel": ["yodel", "pigeon", "dance", "studio"]
            }
            
            found_career = None
            for career, keywords in career_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    found_career = career
                    break
            
            if found_career:
                if has_wrong_prompt:
                    issues.append({
                        "page": page_num,
                        "issue": f"Should be {found_career} but has wrong prompt",
                        "text": page_text[:50] + "..."
                    })
                else:
                    print(f"   ✅ {found_career.title()} content")
            else:
                print("   ❓ Unclear career type")
        
        print()
    
    # Summary
    if issues:
        print(f"🚨 FOUND {len(issues)} PAGES WITH ISSUES:\n")
        for issue in issues:
            print(f"   Page {issue['page']}: {issue['issue']}")
            print(f"                   Text: {issue['text']}")
            print()
        
        print("These pages need to be regenerated with correct prompts!")
    else:
        print("✅ All regenerated pages appear to have correct content!")

if __name__ == "__main__":
    main()
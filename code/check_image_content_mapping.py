#!/usr/bin/env python3
"""
Check if existing images just need to be remapped rather than regenerated.
"""

from pathlib import Path

def get_page_text_keywords(page_num):
    """Get key content words from page text."""
    prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    if not prompt_file.exists():
        return []
    
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
    
    text = page_text.strip().lower()
    
    # Extract career keywords
    career_keywords = []
    if "computer" in text or "ai" in text or "program" in text:
        career_keywords.append("AI programming")
    if "lego" in text or "engineer" in text:
        career_keywords.append("LEGO engineer") 
    if "actor" in text or "tv" in text or "bear" in text:
        career_keywords.append("Actor")
    if "politics" in text or "office" in text or "aoc" in text:
        career_keywords.append("Politics")
    if "librarian" in text or "library" in text:
        career_keywords.append("Librarian")
    if "truck" in text or "reverse" in text:
        career_keywords.append("Truck driver")
    if "lawyer" in text or "legal" in text:
        career_keywords.append("Lawyer")
    if "podcast" in text or "cat" in text:
        career_keywords.append("Podcast")
    if "gamer" in text or "fortnite" in text or "esports" in text:
        career_keywords.append("Pro gamer")
    if "mattress" in text or "sleep" in text:
        career_keywords.append("Mattress tester")
    if "hamster" in text or "lobster" in text:
        career_keywords.append("Hamster guard/Lobster fisher")
    if "golf" in text or "ball" in text or "diver" in text:
        career_keywords.append("Golf ball diver")
    if "water" in text or "slide" in text or "netflix" in text:
        career_keywords.append("Water slides/Netflix/Line-standing")
    if "food" in text and "styling" in text:
        career_keywords.append("Food styling")
    if "stock" in text and "photo" in text:
        career_keywords.append("Stock photos")
    if "yodel" in text or "pigeon" in text:
        career_keywords.append("Yodeling/Pigeons")
    if "spinning" in text or "head" in text:
        career_keywords.append("Head spinning")
    if "right" in text and "shouted" in text:
        career_keywords.append("Family declaration")
    if "cheered" in text and "hug" in text:
        career_keywords.append("Family hug")
    
    return career_keywords

def main():
    """Check what each problematic page should actually show."""
    print("🔍 Checking what each page should actually show:\n")
    
    # Pages that were flagged as having wrong prompts
    problem_pages = [26, 27, 28, 31, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47]
    
    print("CURRENT PAGE → EXPECTED CONTENT:")
    print("=" * 50)
    
    for page_num in problem_pages:
        keywords = get_page_text_keywords(page_num)
        content = " / ".join(keywords) if keywords else "Unknown content"
        print(f"Page {page_num:02d} → {content}")
    
    print("\n" + "=" * 50)
    print("\nNow we need to check what each EXISTING image actually shows")
    print("and see if any can be remapped instead of regenerated.")
    
    # Current page mapping from the book creation script
    current_mapping = {
        26: 24, 27: 25, 28: 26, 29: 27, 30: 28, 31: 29, 32: 30, 33: 31, 34: 32, 35: 33,
        36: 34, 37: 35, 38: 36, 39: 37, 40: 38, 41: 39, 42: 40, 43: 41, 44: 42, 45: 43, 
        46: 44, 47: 45
    }
    
    print(f"\nCURRENT IMAGE MAPPING:")
    print("=" * 50)
    for page_num in problem_pages:
        original_img = current_mapping.get(page_num, "?")
        print(f"Page {page_num:02d} uses image: page{original_img}.png/jpg")
        
    print("\n💡 NEXT STEPS:")
    print("1. Manually check a few key images to see what they actually show")
    print("2. See if we can remap existing images instead of regenerating") 
    print("3. Only regenerate images that truly don't exist or are wrong")

if __name__ == "__main__":
    main()
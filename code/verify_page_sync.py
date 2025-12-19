#!/usr/bin/env python3
"""
Verify that page text, prompts, and images are all synchronized correctly.
"""

import os
from pathlib import Path
import re

def get_page_text_summary(page_num):
    """Get a brief summary of the page text content."""
    if page_num == 0:
        prompt_file = Path("page-prompts/page-00-cover.md")
    elif page_num == 52:
        prompt_file = Path("page-prompts/page-52.md")
    else:
        prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    
    if not prompt_file.exists():
        return "FILE NOT FOUND"
    
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
        
        if in_page_text and line.strip():
            page_text += line.strip() + " "
    
    # Return first 100 chars as summary
    return page_text[:100].strip() if page_text else "NO TEXT"

def get_image_description(page_num, page_map):
    """Get description of what image should be shown."""
    mapped = page_map.get(page_num)
    if mapped is None:
        return "NO MAPPING"
    
    # Image descriptions based on the mapping
    descriptions = {
        "Cover": "Store at Five Corners (cover)",
        1: "Store abandoned/sad",
        2: "Corey arriving with cart",
        3: "Corey cleaning",
        4: "Corey serving customers",
        5: "Corey with phone (reviews)",
        "6_unique": "Reviews explosion/bubbles",
        6: "Tablet with reviews",
        7: "Visitors/hikers",
        "9_unique": "Guest book signing",
        8: "Money troubles",
        9: "Road crews/roundabout",
        10: "E.coli/water problems",
        11: "November customers stopping",
        12: "Corey alone in café",
        13: "Corey saying goodbye",
        14: "Family arrives",
        15: "Emily's encouragement",
        16: "Zephyr's first suggestion",
        17: "Emily with list",
        18: "Astronaut fantasy",
        19: "Punk rock guitarist",
        20: "Ship captain",
        21: "Crypto mogul",
        22: "Self-driving cars",
        23: "Dreams filling air",
        24: "AI programming",
        25: "Lego engineer",
        26: "Actor",
        27: "Politics",
        28: "Librarian",
        29: "Big truck driver",
        30: "Lawyer",
        31: "Podcast",
        32: "Pro gamer",
        33: "Mattress tester",
        34: "Guitar teacher/lobster fisher",
        35: "Golf ball diver",
        36: "Water slides",
        37: "Food styling",
        38: "Stock photos",
        39: "Yodeling/pigeons",
        40: "Head spinning",
        41: "Transformation",
        42: "Tackle hug",
        43: "Family declaration",
        44: "Store farewell",
        45: "Final family scene",
        "new": "NEW IMAGE NEEDED",
        "47-back-cover": "Back cover montage"
    }
    
    return descriptions.get(mapped, f"Image {mapped}")

def verify_sync():
    """Verify all pages are correctly synchronized."""
    # Page mapping from create_final_corrected_book.py
    page_map = {
        0: "Cover",
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: "6_unique",
        7: 6,
        8: 7,
        9: "9_unique",
        10: 8,
        11: 9,
        12: 10,
        13: 11,
        14: 12,
        15: 13,
        16: 14,
        17: 15,
        18: 16,
        19: 17,
        20: 18,
        21: 19,
        22: 20,
        23: 21,
        24: 22,
        25: 23,
        26: 24,
        27: 25,
        28: 26,
        29: 27,
        30: 28,
        31: 29,
        32: 30,
        33: 31,
        34: 32,
        35: 33,
        36: 34,
        37: 35,
        38: 36,
        39: 37,
        40: 38,
        41: 39,
        42: 40,
        43: 41,
        44: 42,
        45: 43,
        46: 44,
        47: 45,
        48: "new",
        49: "new",
        50: "new",
        51: "new",
        52: "47-back-cover",
    }
    
    print("📚 Verifying Page Synchronization")
    print("=" * 80)
    print(f"{'Page':^6} | {'Text Summary':^40} | {'Expected Image':^30}")
    print("-" * 80)
    
    issues = []
    
    for page_num in range(53):  # 0-52
        text_summary = get_page_text_summary(page_num)
        image_desc = get_image_description(page_num, page_map)
        
        # Truncate summaries for display
        if len(text_summary) > 40:
            text_summary = text_summary[:37] + "..."
        
        print(f"{page_num:^6} | {text_summary:<40} | {image_desc:<30}")
        
        # Check for known issues
        if "astronaut" in text_summary.lower() and "Astronaut" not in image_desc:
            issues.append(f"Page {page_num}: Text mentions astronaut but image is {image_desc}")
        elif "punk rock" in text_summary.lower() and "Punk rock" not in image_desc:
            issues.append(f"Page {page_num}: Text mentions punk rock but image is {image_desc}")
        elif "FILE NOT FOUND" in text_summary:
            issues.append(f"Page {page_num}: Missing page prompt file")
        elif image_desc == "NEW IMAGE NEEDED":
            issues.append(f"Page {page_num}: Needs new image generated")
    
    print("\n" + "=" * 80)
    
    if issues:
        print("\n❌ Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ All pages appear to be correctly synchronized!")
    
    # Check for missing images
    print("\n📸 Checking Image Files:")
    leonardo_dir = Path("cartoon-characters/leonardo")
    
    for page_num, mapped in page_map.items():
        if mapped == "new":
            print(f"   - Page {page_num}: Needs new image")
        elif mapped == "Cover":
            if not leonardo_dir.joinpath("Cover_with_store.jpg").exists():
                print(f"   - Page {page_num}: Missing Cover_with_store.jpg")
        elif mapped == "6_unique":
            if not leonardo_dir.joinpath("page6_phil_foglio.png").exists():
                print(f"   - Page {page_num}: Missing page6_phil_foglio.png")
        elif mapped == "9_unique":
            if not leonardo_dir.joinpath("page9_phil_foglio.png").exists():
                print(f"   - Page {page_num}: Missing page9_phil_foglio.png")
        elif mapped == "47-back-cover":
            if not leonardo_dir.joinpath("page47-back-cover-montage.png").exists():
                print(f"   - Page {page_num}: Missing back cover image")
        elif isinstance(mapped, int):
            jpg = leonardo_dir / f"page{mapped}.jpg"
            png = leonardo_dir / f"page{mapped}.png"
            if not jpg.exists() and not png.exists():
                print(f"   - Page {page_num}: Missing image for page{mapped}")

if __name__ == "__main__":
    verify_sync()
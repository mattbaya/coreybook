#!/usr/bin/env python3
"""
Restore original text content from backup prompts.
"""

import os
from pathlib import Path
import re

def extract_page_text_from_backup(backup_file):
    """Extract the PAGE TEXT section from a backup file."""
    if not backup_file.exists():
        return None
    
    with open(backup_file, 'r') as f:
        content = f.read()
    
    # Find PAGE TEXT section
    lines = content.split('\n')
    page_text = ""
    in_page_text = False
    
    for line in lines:
        if line.strip().startswith("## PAGE TEXT"):
            in_page_text = True
            continue
        elif line.strip().startswith("## ") and in_page_text:
            break
        
        if in_page_text:
            page_text += line + "\n"
    
    return page_text.strip() if page_text.strip() else None

def get_correct_text_mapping():
    """Get the correct text for each new page number based on originals."""
    # Mapping: new_page -> original_page (for text content)
    text_mapping = {}
    
    # Pages 1-4 stay the same
    for i in range(1, 5):
        text_mapping[i] = i
    
    # Page 5 original becomes pages 5-6 (split)
    text_mapping[5] = 5
    text_mapping[6] = 5  # Will need to split this manually
    
    # Page 6 original becomes page 7
    text_mapping[7] = 6
    
    # Page 7 original becomes pages 8-9 (split)
    text_mapping[8] = 7
    text_mapping[9] = 7  # Will need to split this manually
    
    # Rest shift by 2
    for i in range(8, 46):  # Original pages 8-45
        text_mapping[i + 2] = i
    
    return text_mapping

def restore_original_texts():
    """Restore all original text content."""
    print("🔄 Restoring original text content...")
    
    backup_dir = Path("page-prompts/backup")
    prompts_dir = Path("page-prompts")
    
    text_mapping = get_correct_text_mapping()
    
    # Special cases for manually split text
    special_texts = {
        5: "Corey checked his phone with growing delight—\nThe reviews were coming in day and night!\nFood's FINALLY discovered the review sites awoke,\n'Ridiculously Good!' they wrote.\n'5 stars! Thumbs Up!'\n'Clearly someone who knows what they're doing!'\nwrote another woman or man.",
        
        6: "'Beautifully composed sandwiches!'\n'Food obsessed in the best way!'\ntyped another neighbor with a smile!\n'What a find!'\nThe praise for Corey floated everywhere!\nHis phone buzzed and ping with each new review,\nAnd cars overflowed his tiny parking lot too!\n'Great baked goods!' 'Crispy chicken sandwich!'\n'Worth the stop!' The five-star ratings just wouldn't stop!\nAnd Corey stood beaming in his kitchen so bright,\nLike bathed in holographic light.",
        
        8: "And hikers and bikers and locals came too,\nThere's Duncan, Rosalie, and Cecilia who\nstopped by for lunch and made my whole day shine!\n\"This Chef is a wizard!\" wrote one in the guest book,\n\"His soups are amazing!\" and \"He sings like a crook!\"\n\"Your pizza is BEST!\" and \"Sammies divine!\"\nYoung Lucas had written, then came back to nap.",
        
        9: "\"My favorite café!\" and \"Such welcoming vibes!\"\n\"This place lifts my mood!\" all the visitors scribe.\nThe journal pages filled up, line after line,\nWith praise for his cooking and space so divine.\nQUOTES FROM REAL JOURNAL ENTRIES:\n\"Worth the drive!\"\n\"Delicious! So neat!\"\n\"Great spot for a break on a backcountry ride!\"\n\"My compliments to the chef!\""
    }
    
    # Process each new page
    for new_page in range(1, 48):
        current_file = prompts_dir / f"page-{new_page:02d}.md"
        
        if not current_file.exists():
            continue
        
        # Read current file
        with open(current_file, 'r') as f:
            current_content = f.read()
        
        # Get correct text
        if new_page in special_texts:
            correct_text = special_texts[new_page]
        elif new_page in text_mapping:
            original_page = text_mapping[new_page]
            backup_file = backup_dir / f"page-{original_page:02d}.md"
            correct_text = extract_page_text_from_backup(backup_file)
        else:
            continue
        
        if not correct_text:
            print(f"  ⚠️ No text found for page {new_page}")
            continue
        
        # Replace the PAGE TEXT section
        lines = current_content.split('\n')
        new_lines = []
        in_page_text = False
        found_page_text = False
        
        for line in lines:
            if line.strip().startswith("## PAGE TEXT"):
                new_lines.append(line)
                new_lines.append(correct_text)
                in_page_text = True
                found_page_text = True
                continue
            elif line.strip().startswith("## ") and in_page_text:
                in_page_text = False
                new_lines.append(line)
            elif not in_page_text:
                new_lines.append(line)
        
        # Write back to file
        if found_page_text:
            with open(current_file, 'w') as f:
                f.write('\n'.join(new_lines))
            print(f"  ✅ Restored page {new_page}")
        else:
            print(f"  ⚠️ Could not find PAGE TEXT section in page {new_page}")

def main():
    """Restore original text content."""
    restore_original_texts()
    print("\n✅ Original text content restored!")
    print("   All pages now have their correct original text")

if __name__ == "__main__":
    main()
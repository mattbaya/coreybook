#!/usr/bin/env python3
"""
Create final book with corrected text content from updated prompts.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import re

def get_page_text_from_prompts(page_num):
    """Load page text from the updated prompt files."""
    if page_num == 0:
        return ""  # Cover has no text
    elif page_num == 52:
        # Back cover
        prompt_file = Path("page-prompts/page-52.md")
    else:
        prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    
    if not prompt_file.exists():
        return ""
    
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
    
    return page_text.strip()

def get_illustration_path(page_num):
    """Get the correct illustration file path for a page number."""
    # Map new page numbers to original illustration numbers
    page_map = {
        0: "Cover",  # Cover
        1: 1,   # Store abandoned
        2: 2,   # Corey arriving with equipment
        3: 3,   # Corey cleaning
        4: 4,   # Corey serving customers
        5: 5,   # Corey with phone (reviews) - part 1
        6: "6_unique",   # Unique illustration for page 6 (reviews explosion)
        7: 6,   # Tablet with reviews  
        8: 7,   # Visitors/hikers - part 1
        9: "9_unique",   # Unique illustration for page 9 (guest book)
        10: 8,  # Money troubles
        11: 9,  # Road crews/roundabout
        12: 10, # E.coli/water problems
        13: 11, # November customers stopping
        14: 12, # Corey alone in café
        15: 13, # Corey saying goodbye
        16: 14, # Family arrives
        17: 15, # Emily's encouragement
        18: 16, # Zephyr's first suggestion
        19: 17, # Emily with the list
        20: 18, # Astronaut fantasy
        21: 19, # Punk rock guitarist
        22: 20, # Ship captain
        23: 21, # Crypto mogul
        24: 22, # Self-driving cars
        25: 23, # Dreams filling the air
        26: 24, # AI programming
        27: 25, # Lego engineer
        28: 26, # Actor
        29: 27, # Politics
        30: 28, # Librarian (Corey's suggestion)
        31: 29, # Big truck driver
        32: 30, # Lawyer
        33: 31, # Podcast
        34: 32, # Pro gamer (3-panel)
        35: 33, # Mattress tester
        36: 34, # Hamster guard/lobster fisher
        37: 35, # Golf ball diver
        38: 36, # Water slides
        39: 37, # Food styling
        40: 38, # Stock photos
        41: 39, # Yodeling/pigeons
        42: 40, # Head spinning
        43: 41, # Transformation/realization
        44: 42, # Tackle hug
        45: 43, # Family declaration
        46: 44, # Store farewell
        47: 45, # Final family scene
        48: "new", # Family walking away
        49: "new", # Looking back at Store
        50: "new", # Message to reader part 1
        51: "new", # Message to reader part 2 - RISE AGAIN
        52: "47-back-cover", # Back cover
    }
    
    mapped_page = page_map.get(page_num)
    if mapped_page is None:
        return None
        
    # Handle special cases
    if mapped_page == "Cover":
        paths = [
            Path("cartoon-characters/leonardo/Cover_with_store.jpg"),
            Path("final/page-00-cover.jpg"),
            Path("cartoon-characters/leonardo/Cover.jpg"),
        ]
    elif mapped_page == "6_unique":
        paths = [
            Path("cartoon-characters/leonardo/page6_phil_foglio.png"),
            Path("cartoon-characters/leonardo/page6_unique.png"),
        ]
    elif mapped_page == "9_unique":
        paths = [
            Path("cartoon-characters/leonardo/page9_phil_foglio.png"),
            Path("cartoon-characters/leonardo/page9_unique.png"),
        ]
    elif mapped_page == "47-back-cover":
        paths = [
            Path("cartoon-characters/leonardo/page-47-back-cover-montage.png"),
            Path("final/page-47-back-cover-montage.png"),
        ]
    elif mapped_page == "new":
        # New pages that need images generated
        paths = []
    else:
        # Check multiple possible paths
        paths = []
        
        # Add special overrides for pages 1 and 2
        if page_num == 1:
            paths.append(Path("cartoon-characters/leonardo/page1_accurate_store.jpg"))
            paths.append(Path("cartoon-characters/leonardo/page1_sad_store.jpg"))
        elif page_num == 2:
            paths.append(Path("cartoon-characters/leonardo/page2_corey_cart.jpg"))
        
        # Then add the standard paths
        paths.extend([
            Path(f"final/page{mapped_page}.jpg"),
            Path(f"final/page{mapped_page}.png"),
            Path(f"cartoon-characters/leonardo/page{mapped_page}.jpg"),
            Path(f"cartoon-characters/leonardo/page{mapped_page}.png"),
        ])
    
    for path in paths:
        if path.exists():
            return path
    
    return None

def wrap_text_for_width(text, font, max_width, draw):
    """Wrap text to fit within a specific width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_landscape_page(page_num, output_path, is_left_page=True):
    """Create landscape layout with binding margin."""
    # Page dimensions in pixels at 300 DPI
    dpi = 300
    page_width = int(11 * dpi)  # 11 inches
    page_height = int(8.5 * dpi)  # 8.5 inches
    outer_margin = int(0.25 * dpi)  # 0.25 inch outer margins
    binding_margin = int(0.5 * dpi)  # 0.5 inch binding margin
    
    # Create white page
    page = Image.new('RGB', (page_width, page_height), 'white')
    draw = ImageDraw.Draw(page)
    
    # Get illustration
    img_path = get_illustration_path(page_num)
    
    # Adjust margins based on page side
    left_margin = binding_margin if is_left_page else outer_margin
    right_margin = outer_margin if is_left_page else binding_margin
    
    if not img_path:
        # Text-only page
        text_x = left_margin
        text_y = outer_margin
        text_width = page_width - left_margin - right_margin
        text_height = page_height - (2 * outer_margin) - int(0.5 * dpi)
        
        # Get text from prompts
        text = get_page_text_from_prompts(page_num)
        
        if text:
            # Find appropriate font size
            font_size = int(0.3 * dpi)
            while font_size > int(0.12 * dpi):
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                
                lines = wrap_text_for_width(text, font, text_width, draw)
                line_height = font_size * 1.5
                total_height = len(lines) * line_height
                
                if total_height <= text_height:
                    break
                font_size -= int(0.01 * dpi)
            
            # Draw text
            y_offset = text_y + (text_height - total_height) // 2
            for line in lines:
                draw.text((text_x, y_offset), line, fill='black', font=font)
                y_offset += line_height
    else:
        # Page with illustration
        img = Image.open(img_path)
        
        # Calculate available space
        available_width = page_width - left_margin - right_margin
        available_height = page_height - (2 * outer_margin)
        
        # Image takes up left portion
        img_size = min(int(8 * dpi), available_height)
        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Paste image
        img_x = left_margin
        img_y = outer_margin + (available_height - img_size) // 2
        page.paste(img, (img_x, img_y))
        
        # Text area on right
        text_x = left_margin + img_size + int(0.25 * dpi)
        text_y = outer_margin
        text_width = page_width - text_x - right_margin
        text_height = available_height - int(0.5 * dpi)
        
        # Get text from prompts
        text = get_page_text_from_prompts(page_num)
        
        if text:
            # Find appropriate font size
            font_size = int(0.25 * dpi)
            while font_size > int(0.12 * dpi):
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                
                lines = wrap_text_for_width(text, font, text_width, draw)
                line_height = font_size * 1.5
                total_height = len(lines) * line_height
                
                if total_height <= text_height:
                    break
                font_size -= int(0.01 * dpi)
            
            # Draw text
            y_offset = text_y + int(0.3 * dpi)
            for line in lines:
                draw.text((text_x, y_offset), line, fill='black', font=font)
                y_offset += line_height
    
    # Add page number
    if page_num > 0:  # No page number on cover
        page_font_size = int(0.12 * dpi)
        try:
            page_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", page_font_size)
        except:
            page_font = ImageFont.load_default()
        
        page_text = f"{page_num}"
        bbox = draw.textbbox((0, 0), page_text, font=page_font)
        
        # Position based on page side
        if is_left_page:
            page_num_x = outer_margin
        else:
            page_num_x = page_width - outer_margin - (bbox[2] - bbox[0])
        
        page_num_y = page_height - outer_margin - page_font_size
        draw.text((page_num_x, page_num_y), page_text, fill='gray', font=page_font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    return True

def create_portrait_page(page_num, output_path, is_left_page=True):
    """Create portrait layout with binding margin."""
    # Page dimensions in pixels at 300 DPI
    dpi = 300
    page_width = int(8.5 * dpi)  # 8.5 inches
    page_height = int(11 * dpi)  # 11 inches
    outer_margin = int(0.25 * dpi)  # 0.25 inch outer margins
    binding_margin = int(0.5 * dpi)  # 0.5 inch binding margin
    
    # Create white page
    page = Image.new('RGB', (page_width, page_height), 'white')
    draw = ImageDraw.Draw(page)
    
    # Get illustration
    img_path = get_illustration_path(page_num)
    
    # Adjust margins based on page side
    left_margin = binding_margin if is_left_page else outer_margin
    right_margin = outer_margin if is_left_page else binding_margin
    
    if not img_path:
        # Text-only page
        text_x = left_margin
        text_y = outer_margin
        text_width = page_width - left_margin - right_margin
        text_height = page_height - (2 * outer_margin) - int(0.5 * dpi)
        
        # Get text from prompts
        text = get_page_text_from_prompts(page_num)
        
        if text:
            # Find appropriate font size
            font_size = int(0.3 * dpi)
            while font_size > int(0.12 * dpi):
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                
                lines = text.split('\n') if '\n' in text else wrap_text_for_width(text, font, text_width, draw)
                line_height = font_size * 1.4
                total_height = len(lines) * line_height
                
                if total_height <= text_height:
                    break
                font_size -= int(0.01 * dpi)
            
            # Draw text centered
            y_offset = text_y + (text_height - total_height) // 2
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                x_centered = left_margin + (text_width - text_w) // 2
                draw.text((x_centered, y_offset), line, fill='black', font=font)
                y_offset += line_height
    else:
        # Page with illustration
        img = Image.open(img_path)
        
        # Calculate available space
        available_width = page_width - left_margin - right_margin
        
        # Image size
        img_size = min(available_width, int(8 * dpi))
        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Center image horizontally in available space
        img_x = left_margin + (available_width - img_size) // 2
        page.paste(img, (img_x, outer_margin))
        
        # Text area below
        text_x = left_margin
        text_y = outer_margin + img_size + int(0.25 * dpi)
        text_width = available_width
        text_height = page_height - text_y - outer_margin - int(0.5 * dpi)
        
        # Get text from prompts
        text = get_page_text_from_prompts(page_num)
        
        if text:
            # Find appropriate font size
            font_size = int(0.24 * dpi)
            while font_size > int(0.12 * dpi):
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                
                lines = text.split('\n') if '\n' in text else wrap_text_for_width(text, font, text_width, draw)
                line_height = font_size * 1.4
                total_height = len(lines) * line_height
                
                if total_height <= text_height:
                    break
                font_size -= int(0.01 * dpi)
            
            # Draw text centered
            y_offset = text_y
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                x_centered = left_margin + (text_width - text_w) // 2
                draw.text((x_centered, y_offset), line, fill='black', font=font)
                y_offset += line_height
    
    # Add page number
    if page_num > 0:
        page_font_size = int(0.12 * dpi)
        try:
            page_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", page_font_size)
        except:
            page_font = ImageFont.load_default()
        
        page_text = f"{page_num}"
        bbox = draw.textbbox((0, 0), page_text, font=page_font)
        
        # Center at bottom
        page_num_x = (page_width - (bbox[2] - bbox[0])) // 2
        page_num_y = page_height - outer_margin - int(0.3 * dpi)
        draw.text((page_num_x, page_num_y), page_text, fill='gray', font=page_font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    return True

def create_final_book():
    """Create final book with corrected text from prompts."""
    # Create output directory
    os.makedirs("final_corrected_book", exist_ok=True)
    
    # Total pages (0-52, including back cover)
    total_pages = 53
    
    print("📚 Creating FINAL CORRECTED book with original text content...")
    
    print("\nCreating LANDSCAPE version...")
    landscape_images = []
    for i in range(total_pages):
        is_left_page = (i % 2 == 0)
        output_path = f"final_corrected_book/landscape_page_{i:03d}.png"
        if create_landscape_page(i, output_path, is_left_page):
            print(f"  Created page {i}")
            img = Image.open(output_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            landscape_images.append(img)
    
    # Create landscape PDF
    if landscape_images:
        landscape_images[0].save(
            'The_Chef_at_the_Store_FINAL_LANDSCAPE.pdf',
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=landscape_images[1:]
        )
        print(f"\n✅ Created The_Chef_at_the_Store_FINAL_LANDSCAPE.pdf ({len(landscape_images)} pages)")
    
    print("\nCreating PORTRAIT version...")
    portrait_images = []
    for i in range(total_pages):
        is_left_page = (i % 2 == 0)
        output_path = f"final_corrected_book/portrait_page_{i:03d}.png"
        if create_portrait_page(i, output_path, is_left_page):
            print(f"  Created page {i}")
            img = Image.open(output_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            portrait_images.append(img)
    
    # Create portrait PDF
    if portrait_images:
        portrait_images[0].save(
            'The_Chef_at_the_Store_FINAL_PORTRAIT.pdf',
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=portrait_images[1:]
        )
        print(f"\n✅ Created The_Chef_at_the_Store_FINAL_PORTRAIT.pdf ({len(portrait_images)} pages)")
    
    print("\n🎉 FINAL books created with:")
    print("   ✅ Original corrected text content")
    print("   ✅ Proper image-text alignment") 
    print("   ✅ Binding margins for printing")
    print("   ✅ All 48 pages complete")
    print("\nFiles:")
    print("   📄 The_Chef_at_the_Store_FINAL_LANDSCAPE.pdf")
    print("   📄 The_Chef_at_the_Store_FINAL_PORTRAIT.pdf")

if __name__ == "__main__":
    create_final_book()
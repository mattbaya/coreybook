#!/usr/bin/env python3
"""
Create improved mockups with proper text wrapping and scaling for 16 pages.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import textwrap

def get_page_text(page_num):
    """Get the text content for pages 1-16."""
    texts = {
        1: "At the corner of Five Roads (yes, five! Not just four!) Stood a rickety, wonderful, old country Store. It had stood there for ages—two hundred and MORE! But it sat there all dusty. It sat there all sad. The shelves were all empty. The windows looked bad.",
        
        2: "Then along came young Corey, a chef with a dream, With his pans and his spatulas, all shiny and clean. \"I will OPEN this Store!\" Corey said with delight. \"I'll make sandwiches, coffees! I'll set this place RIGHT!\"",
        
        3: "So he scrubbed and he polished from ceiling to floor, He hung up new menus and opened the door! The neighbors came running! The farmers came too! They said, \"Corey! Oh Corey! We've been WAITING for you!\"",
        
        4: "For three wonderful years, Corey cooked in that place. He served up his bagels and scones with a smile on his face. YELP filled up with love, many customers thought, \"Life in the MOUNTAINS doesn't GET better than this!\"",
        
        5: "Corey checked his phone with growing delight— The reviews were coming in day and night! Food's FINALLY discovered the review sites awoke, 'Ridiculously Good!' they wrote. '5 stars! Thumbs Up!' 'Clearly someone who knows what they're doing!' wrote another woman or man. 'Beautifully composed sandwiches!' 'Food obsessed in the best way!' typed another neighbor with a smile! 'What a find!' The praise for Corey floated everywhere! His phone buzzed and ping with each new review, And cars overflowed his tiny parking lot too! 'Great baked goods!' 'Crispy chicken sandwich!' 'Worth the stop!' The five-star ratings just wouldn't stop! And Corey stood beaming in his kitchen so bright, Like bathed in holographic light.",
        
        6: "The tablet glowed bright with review after review, Each one more delightful than the last one he knew! The nicest reviews that he'd ever seen! From 'Captain of this ship' to 'Best croissant in life'— He couldn't wait to share this with Emily, his wife! 'Four years of work and the dream is now PACKED! The folks are all talking and our café's on track!'",
        
        7: "And hikers and bikers and locals came too, There's Duncan, Rosalie, and Cecilia who stopped by for lunch and made my whole day shine! \"This Chef is a wizard!\" wrote one in the guest book, \"His soups are amazing!\" and \"He sings like a crook!\" \"Your pizza is BEST!\" and \"Sammies divine!\" Young Lucas had written, then came back to nap. \"My favorite café!\" and \"Such welcoming vibes!\" \"This place lifts my mood!\" all the visitors scribe. The journal pages filled up, line after line, With praise for his cooking and space so divine. QUOTES FROM REAL JOURNAL ENTRIES: \"Worth the drive!\" \"Delicious! So neat!\" \"Great spot for a break on a backcountry ride!\" \"My compliments to the chef!\"",
        
        8: "But the money was tight—oh, so terribly tight! He'd count up his pennies by dim kitchen light. But his dream still lived! It would fly like a bird to the sky!",
        
        9: "Then the road crews arrived with their cones and their trucks, They shut down the crossroads for \"upgrades and such.\" \"It will help!\" said the town. But no cars could get through. \"A ROUNDABOUT!\" they announced. \"Done by next year!\" But Corey's café disappeared from all view.",
        
        10: "Still Corey kept cooking through summer and fall. But then came the dreadful, most worrisome call: When the water turned BAD in the worst sort of way! \"E. COLI!\" they shouted. \"Don't drink! Do not sip!\" And the customers vanished on that terrible trip.",
        
        11: "He closed for a day. Then he opened once more. But in NOVEMBER, what happened shook him to his core: The customers, one by one, just stopped coming by. His café sat empty beneath the gray sky.",
        
        12: "And Corey sat down in the quiet café, Convinced that his dream had just slipped away. The roundabout project had won the day.",
        
        13: "Now Corey must go, though it hurt quite a lot. He whispered, \"Goodbye to this beautiful spot.\" He stood there alone as the sun sank away. At the end of his final and difficult day?",
        
        14: "He turned and he saw them—his family, his CREW! Running toward him and shouting, \"We're HERE! We're here, too!\" There was Emily smiling, and the Super Three: Remi, Oona, and Zephyr—as happy as can be! Emily hugged him and said with emotion so true, \"Oh my darling, you're NOT nearly done!\"",
        
        15: "\"This chapter is closing, but here's the great news: A NEW book is starting! And YOU get to choose!\"",
        
        16: "\"Papa,\" said Zephyr (the littlest one), \"You can do ANYTHING! Your next job's begun!\""
    }
    return texts.get(page_num, "")

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

def create_landscape_layout(page_num, output_path):
    """Create landscape layout with proper text wrapping."""
    # Page dimensions in pixels at 300 DPI
    dpi = 300
    page_width = int(11 * dpi)  # 11 inches
    page_height = int(8.5 * dpi)  # 8.5 inches
    margin = int(0.25 * dpi)  # 0.25 inch margins
    
    # Create white page
    page = Image.new('RGB', (page_width, page_height), 'white')
    draw = ImageDraw.Draw(page)
    
    # Load illustration
    img_path = Path(f"final/page{page_num}.jpg")
    if not img_path.exists():
        img_path = Path(f"final/page{page_num}.png")
    
    if img_path.exists():
        img = Image.open(img_path)
        
        # Calculate image size (square, fitting within margins)
        img_size = page_height - (2 * margin)
        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Paste image on left side
        page.paste(img, (margin, margin))
        
        # Text area on right
        text_x = margin + img_size + int(0.25 * dpi)  # Extra 0.25" gap
        text_y = margin
        text_width = page_width - text_x - margin - int(0.1 * dpi)  # Extra padding
        text_height = page_height - (2 * margin) - int(0.5 * dpi)  # Space for page number
        
        # Get text
        text = get_page_text(page_num)
        
        # Start with larger font and scale down if needed
        font_size = int(0.25 * dpi)  # Start at 0.25"
        while font_size > int(0.12 * dpi):  # Minimum 0.12"
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            lines = wrap_text_for_width(text, font, text_width, draw)
            
            # Calculate total height needed
            line_height = font_size * 1.5
            total_height = len(lines) * line_height
            
            # Check if it fits
            if total_height <= text_height:
                break
            
            font_size -= int(0.01 * dpi)  # Decrease by 0.01"
        
        # Draw wrapped text
        y_offset = text_y + int(0.3 * dpi)  # Start text a bit lower
        
        for line in lines:
            draw.text((text_x, y_offset), line, fill='black', font=font)
            y_offset += line_height
        
        # Add page number at bottom right
        page_font_size = int(0.12 * dpi)
        try:
            page_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", page_font_size)
        except:
            page_font = ImageFont.load_default()
        
        page_text = f"Page {page_num}"
        bbox = draw.textbbox((0, 0), page_text, font=page_font)
        page_num_x = page_width - margin - (bbox[2] - bbox[0])
        page_num_y = page_height - margin - page_font_size
        draw.text((page_num_x, page_num_y), page_text, fill='gray', font=page_font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    print(f"Created landscape layout: {output_path}")

def create_portrait_layout(page_num, output_path):
    """Create portrait layout with text that scales to fit."""
    # Page dimensions in pixels at 300 DPI
    dpi = 300
    page_width = int(8.5 * dpi)  # 8.5 inches
    page_height = int(11 * dpi)  # 11 inches
    margin = int(0.25 * dpi)  # 0.25 inch margins
    
    # Create white page
    page = Image.new('RGB', (page_width, page_height), 'white')
    draw = ImageDraw.Draw(page)
    
    # Load illustration
    img_path = Path(f"final/page{page_num}.jpg")
    if not img_path.exists():
        img_path = Path(f"final/page{page_num}.png")
        
    if img_path.exists():
        img = Image.open(img_path)
        
        # Calculate image size (square, fitting within width)
        img_size = page_width - (2 * margin)
        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Paste image at top
        page.paste(img, (margin, margin))
        
        # Text area below
        text_x = margin
        text_y = margin + img_size + int(0.25 * dpi)  # Extra 0.25" gap
        text_width = page_width - (2 * margin)
        # Leave space for page number
        text_height = page_height - text_y - margin - int(0.5 * dpi)
        
        # Get text
        text = get_page_text(page_num)
        
        # Start with larger font and scale down if needed
        font_size = int(0.24 * dpi)  # Start at 0.24"
        while font_size > int(0.12 * dpi):  # Minimum 0.12"
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                font = ImageFont.load_default()
            
            # Split into lines and calculate height
            lines = text.split('\n') if '\n' in text else wrap_text_for_width(text, font, text_width, draw)
            line_height = font_size * 1.4
            total_height = len(lines) * line_height
            
            # Check if it fits
            if total_height <= text_height:
                break
            
            font_size -= int(0.01 * dpi)  # Decrease by 0.01"
        
        # Draw text centered
        y_offset = text_y
        
        for line in lines:
            # Get text size for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x_centered = margin + (text_width - text_w) // 2
            
            draw.text((x_centered, y_offset), line, fill='black', font=font)
            y_offset += line_height
        
        # Add page number at bottom center (well above bottom margin)
        page_font_size = int(0.12 * dpi)
        try:
            page_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", page_font_size)
        except:
            page_font = ImageFont.load_default()
        
        page_text = f"Page {page_num}"
        bbox = draw.textbbox((0, 0), page_text, font=page_font)
        page_num_x = (page_width - (bbox[2] - bbox[0])) // 2
        page_num_y = page_height - margin - int(0.3 * dpi)  # Higher up from bottom
        draw.text((page_num_x, page_num_y), page_text, fill='gray', font=page_font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    print(f"Created portrait layout: {output_path}")

def create_mockups():
    """Create mockups for first 16 pages in both layouts."""
    # Create output directory
    os.makedirs("layout_mockups_16", exist_ok=True)
    
    # Create landscape versions
    print("\nCreating LANDSCAPE layouts for 16 pages...")
    for i in range(1, 17):
        create_landscape_layout(i, f"layout_mockups_16/landscape_page_{i}.png")
    
    # Create portrait versions
    print("\nCreating PORTRAIT layouts for 16 pages...")
    for i in range(1, 17):
        create_portrait_layout(i, f"layout_mockups_16/portrait_page_{i}.png")
    
    # Combine into comparison PDFs
    print("\nCreating comparison PDFs...")
    
    # Landscape PDF
    landscape_images = []
    for i in range(1, 17):
        img = Image.open(f"layout_mockups_16/landscape_page_{i}.png")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        landscape_images.append(img)
    
    landscape_images[0].save(
        'layout_mockups_16/landscape_layout_16pages.pdf',
        'PDF',
        resolution=100.0,
        save_all=True,
        append_images=landscape_images[1:]
    )
    
    # Portrait PDF
    portrait_images = []
    for i in range(1, 17):
        img = Image.open(f"layout_mockups_16/portrait_page_{i}.png")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        portrait_images.append(img)
    
    portrait_images[0].save(
        'layout_mockups_16/portrait_layout_16pages.pdf',
        'PDF',
        resolution=100.0,
        save_all=True,
        append_images=portrait_images[1:]
    )
    
    print("\n✅ Created improved mockups in 'layout_mockups_16' folder:")
    print("   - landscape_layout_16pages.pdf (16 pages with proper text wrapping)")
    print("   - portrait_layout_16pages.pdf (16 pages with text scaling)")
    print("   - Individual PNG files for each page")

if __name__ == "__main__":
    create_mockups()
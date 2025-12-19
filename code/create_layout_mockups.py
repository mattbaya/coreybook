#!/usr/bin/env python3
"""
Create mockups of landscape and portrait layouts for printing on 8.5"x11" paper.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def get_page_text(page_num):
    """Get the text content for a specific page."""
    texts = {
        1: "At the corner of Five Roads (yes, five! Not just four!)\nStood a rickety, wonderful, old country Store.\nIt had stood there for ages—two hundred and MORE!\nBut it sat there all dusty. It sat there all sad.\nThe shelves were all empty. The windows looked bad.",
        
        2: "Then along came young Corey, a chef with a dream,\nWith his pans and his spatulas, all shiny and clean.\n\"I will OPEN this Store!\" Corey said with delight.\n\"I'll make sandwiches, coffees! I'll set this place RIGHT!\"",
        
        3: "So he scrubbed and he polished from ceiling to floor,\nHe hung up new menus and opened the door!\nThe neighbors came running! The farmers came too!\nThey said, \"Corey! Oh Corey! We've been WAITING for you!\"",
        
        4: "For three wonderful years, Corey cooked in that place.\nHe served up his bagels and scones\nwith a smile on his face.\nYELP filled up with love, many customers thought,\n\"Life in the MOUNTAINS doesn't GET better than this!\""
    }
    return texts.get(page_num, "")

def create_landscape_layout(page_num, output_path):
    """Create landscape layout with image on left, text column on right."""
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
        text_width = page_width - text_x - margin
        
        # Add text
        text = get_page_text(page_num)
        
        # Try to use a nice font, fallback to default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(0.18 * dpi))
        except:
            font = ImageFont.load_default()
        
        # Draw text with line wrapping
        lines = text.split('\n')
        y_offset = text_y + int(0.5 * dpi)  # Start text a bit lower
        
        for line in lines:
            draw.text((text_x, y_offset), line, fill='black', font=font)
            y_offset += int(0.35 * dpi)
        
        # Add page number
        draw.text((page_width - margin - int(0.5 * dpi), page_height - margin - int(0.5 * dpi)), 
                  f"Page {page_num}", fill='gray', font=font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    print(f"Created landscape layout: {output_path}")

def create_portrait_layout(page_num, output_path):
    """Create portrait layout with image on top, text below."""
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
        
        # Add text
        text = get_page_text(page_num)
        
        # Try to use a nice font, fallback to default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(0.2 * dpi))
        except:
            font = ImageFont.load_default()
        
        # Draw text centered
        lines = text.split('\n')
        y_offset = text_y
        
        for line in lines:
            # Get text size for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x_centered = margin + (text_width - text_w) // 2
            
            draw.text((x_centered, y_offset), line, fill='black', font=font)
            y_offset += int(0.4 * dpi)
        
        # Add page number
        draw.text((page_width // 2 - int(0.25 * dpi), page_height - margin - int(0.5 * dpi)), 
                  f"Page {page_num}", fill='gray', font=font)
    
    # Save
    page.save(output_path, dpi=(dpi, dpi))
    print(f"Created portrait layout: {output_path}")

def create_mockups():
    """Create mockups for first 4 pages in both layouts."""
    # Create output directory
    os.makedirs("layout_mockups", exist_ok=True)
    
    # Create landscape versions
    print("\nCreating LANDSCAPE layouts...")
    for i in range(1, 5):
        create_landscape_layout(i, f"layout_mockups/landscape_page_{i}.png")
    
    # Create portrait versions
    print("\nCreating PORTRAIT layouts...")
    for i in range(1, 5):
        create_portrait_layout(i, f"layout_mockups/portrait_page_{i}.png")
    
    # Combine into comparison PDFs
    print("\nCreating comparison PDFs...")
    
    # Landscape PDF
    landscape_images = []
    for i in range(1, 5):
        img = Image.open(f"layout_mockups/landscape_page_{i}.png")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        landscape_images.append(img)
    
    landscape_images[0].save(
        'layout_mockups/landscape_layout_sample.pdf',
        'PDF',
        resolution=100.0,
        save_all=True,
        append_images=landscape_images[1:]
    )
    
    # Portrait PDF
    portrait_images = []
    for i in range(1, 5):
        img = Image.open(f"layout_mockups/portrait_page_{i}.png")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        portrait_images.append(img)
    
    portrait_images[0].save(
        'layout_mockups/portrait_layout_sample.pdf',
        'PDF',
        resolution=100.0,
        save_all=True,
        append_images=portrait_images[1:]
    )
    
    print("\n✅ Created mockups in 'layout_mockups' folder:")
    print("   - landscape_layout_sample.pdf (4 pages)")
    print("   - portrait_layout_sample.pdf (4 pages)")
    print("   - Individual PNG files for each page")

if __name__ == "__main__":
    create_mockups()
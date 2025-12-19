#!/usr/bin/env python3
"""
Combine all book images into a single PDF in correct order.
"""

import os
from pathlib import Path
from PIL import Image
import re

def natural_sort_key(filename):
    """Sort filenames with numbers naturally (1, 2, 10, not 1, 10, 2)"""
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]
    return alphanum_key(filename)

def create_book_pdf():
    # Paths
    final_dir = Path("final")
    output_pdf = "The_Chef_at_the_Store_Complete.pdf"
    
    # Collect all images
    all_images = []
    
    # First, add the cover
    cover_path = final_dir / "page-00-cover.jpg"
    if cover_path.exists():
        print(f"Adding cover: {cover_path.name}")
        all_images.append(str(cover_path))
    
    # Then add pages 1-47 in order (alternating illustration and text)
    for i in range(1, 48):
        # Add illustration page
        illustration_files = list(final_dir.glob(f"page{i}.*")) + list(final_dir.glob(f"page{i:02d}.*"))
        illustration_files = [f for f in illustration_files if "-text" not in f.name]
        
        if illustration_files:
            # Use the first match (should only be one)
            print(f"Adding illustration page {i}: {illustration_files[0].name}")
            all_images.append(str(illustration_files[0]))
        
        # Add text page (if exists)
        text_files = list(final_dir.glob(f"page-{i}-text.png")) + list(final_dir.glob(f"page-{i:02d}-text.png"))
        
        if text_files:
            print(f"Adding text page {i}: {text_files[0].name}")
            all_images.append(str(text_files[0]))
        elif i == 47:
            # Special case for back cover text
            back_text = final_dir / "page-47-text.png"
            if back_text.exists():
                print(f"Adding text page 47: {back_text.name}")
                all_images.append(str(back_text))
    
    # Convert all images to PIL Image objects
    print(f"\nConverting {len(all_images)} images to PDF...")
    pil_images = []
    
    for img_path in all_images:
        try:
            img = Image.open(img_path)
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            pil_images.append(img)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
    
    # Save as PDF
    if pil_images:
        print(f"\nSaving PDF as: {output_pdf}")
        # First image is saved with all others appended
        pil_images[0].save(
            output_pdf,
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=pil_images[1:]
        )
        
        print(f"✅ Successfully created {output_pdf}")
        print(f"   Total pages: {len(pil_images)}")
        
        # Get file size
        file_size = os.path.getsize(output_pdf) / (1024 * 1024)  # Convert to MB
        print(f"   File size: {file_size:.1f} MB")
    else:
        print("❌ No images found to create PDF")

if __name__ == "__main__":
    create_book_pdf()
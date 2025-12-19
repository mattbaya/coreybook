#!/usr/bin/env python3
"""
Create full book layouts with proper binding margins and split text-heavy pages.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import textwrap

def get_page_text(page_num):
    """Get the text content for all pages, with text-heavy pages split."""
    texts = {
        1: "At the corner of Five Roads (yes, five! Not just four!) Stood a rickety, wonderful, old country Store. It had stood there for ages—two hundred and MORE! But it sat there all dusty. It sat there all sad. The shelves were all empty. The windows looked bad.",
        
        2: "Then along came young Corey, a chef with a dream, With his pans and his spatulas, all shiny and clean. \"I will OPEN this Store!\" Corey said with delight. \"I'll make sandwiches, coffees! I'll set this place RIGHT!\"",
        
        3: "So he scrubbed and he polished from ceiling to floor, He hung up new menus and opened the door! The neighbors came running! The farmers came too! They said, \"Corey! Oh Corey! We've been WAITING for you!\"",
        
        4: "For three wonderful years, Corey cooked in that place. He served up his bagels and scones with a smile on his face. YELP filled up with love, many customers thought, \"Life in the MOUNTAINS doesn't GET better than this!\"",
        
        # Page 5 split into two pages
        5: "Corey checked his phone with growing delight— The reviews were coming in day and night! Food's FINALLY discovered the review sites awoke, 'Ridiculously Good!' they wrote. '5 stars! Thumbs Up!' 'Clearly someone who knows what they're doing!' wrote another woman or man.",
        
        6: "'Beautifully composed sandwiches!' 'Food obsessed in the best way!' typed another neighbor with a smile! 'What a find!' The praise for Corey floated everywhere! His phone buzzed and ping with each new review, And cars overflowed his tiny parking lot too! 'Great baked goods!' 'Crispy chicken sandwich!' 'Worth the stop!' The five-star ratings just wouldn't stop! And Corey stood beaming in his kitchen so bright, Like bathed in holographic light.",
        
        7: "The tablet glowed bright with review after review, Each one more delightful than the last one he knew! The nicest reviews that he'd ever seen! From 'Captain of this ship' to 'Best croissant in life'— He couldn't wait to share this with Emily, his wife! 'Four years of work and the dream is now PACKED! The folks are all talking and our café's on track!'",
        
        # Page 7 (old) split into two pages
        8: "And hikers and bikers and locals came too, There's Duncan, Rosalie, and Cecilia who stopped by for lunch and made my whole day shine! \"This Chef is a wizard!\" wrote one in the guest book, \"His soups are amazing!\" and \"He sings like a crook!\"",
        
        9: "\"Your pizza is BEST!\" and \"Sammies divine!\" Young Lucas had written, then came back to nap. \"My favorite café!\" and \"Such welcoming vibes!\" \"This place lifts my mood!\" all the visitors scribe. The journal pages filled up, line after line, With praise for his cooking and space so divine.",
        
        10: "But the money was tight—oh, so terribly tight! He'd count up his pennies by dim kitchen light. But his dream still lived! It would fly like a bird to the sky!",
        
        11: "Then the road crews arrived with their cones and their trucks, They shut down the crossroads for \"upgrades and such.\" \"It will help!\" said the town. But no cars could get through. \"A ROUNDABOUT!\" they announced. \"Done by next year!\" But Corey's café disappeared from all view.",
        
        12: "Still Corey kept cooking through summer and fall. But then came the dreadful, most worrisome call: When the water turned BAD in the worst sort of way! \"E. COLI!\" they shouted. \"Don't drink! Do not sip!\" And the customers vanished on that terrible trip.",
        
        13: "He closed for a day. Then he opened once more. But in NOVEMBER, what happened shook him to his core: The customers, one by one, just stopped coming by. His café sat empty beneath the gray sky.",
        
        14: "And Corey sat down in the quiet café, Convinced that his dream had just slipped away. The roundabout project had won the day.",
        
        15: "Now Corey must go, though it hurt quite a lot. He whispered, \"Goodbye to this beautiful spot.\" He stood there alone as the sun sank away. At the end of his final and difficult day?",
        
        16: "He turned and he saw them—his family, his CREW! Running toward him and shouting, \"We're HERE! We're here, too!\" There was Emily smiling, and the Super Three: Remi, Oona, and Zephyr—as happy as can be! Emily hugged him and said with emotion so true, \"Oh my darling, you're NOT nearly done!\"",
        
        17: "\"This chapter is closing, but here's the great news: A NEW book is starting! And YOU get to choose!\"",
        
        18: "\"Papa,\" said Zephyr (the littlest one), \"You can do ANYTHING! Your next job's begun!\"",
        
        19: "And Emily laughed and she pulled out a list— A list that was long! It could hardly be missed! A scroll full of choices, of jobs by the ton! \"My darling,\" she said, \"Your next chapter's begun!\"",
        
        20: "\"You could be an ASTRONAUT!\" Zephyr declared, \"Flying through space with your bald head all bared! Your café in orbit! Your soup in a ball! Serving space sandwiches, weightless for all!\"",
        
        21: "\"Or a PUNK ROCK GUITARIST!\" shouted Remi with glee, \"Up on stage for the whole world to see! You'd shred on guitar! You'd rock and you'd roll! 'Corey CHAOS' they'd chant! You'd sing from your soul!\"",
        
        22: "\"You could captain a SHIP!\" shouted Oona with cheer, \"Sailing the seas without worry or fear! You'd sing to your sailors a song of the sea: 'What do you DO with a drunken sailor?'—key of C!\"",
        
        23: "\"You could be a CRYPTO MOGUL!\" the Super Three said, \"Buying Bitcoin and NFTs instead! Making millions on memes! On computer you'd stare! Till your eyes would go square and you'd lose all your hair!\"",
        
        24: "\"You could test SELF-DRIVING CARS!\" Zephyr proclaimed, \"Just ride and ride till your bottom gets maimed!\"",
        
        25: "The list just kept going! The dreams filled the air! With so many choices, he'd find something there!",
        
        26: "\"You could PROGRAM COMPUTERS with the help of AI! Build weird apps and gadgets—give anything a try! Make the toaster play music! The doorbell tell jokes! Design socks with rockets for reasonable folks!\"",
        
        27: "\"You could be a LEGO ENGINEER!\" Oona cried out, \"Build a life-sized giraffe or a castle, no doubt!\"",
        
        28: "\"You could be an ACTOR on screens and TV! You could star on a soap—As the WORLD CHURNS, you see!\"",
        
        29: "\"You could go into POLITICS and run for an office! You could be the PRESIDENT—leader and boss-est! You could fix all the problems! Make everything right! Though half of the country would put up a fight!\"",
        
        30: "Corey paused for a moment, then said with a grin: \"Or maybe pro BOWLING? I'd practice my spin!\"",
        
        31: "\"You could drive a BIG TRUCK, but always REVERSE! You'd confuse other drivers and make them all curse!\"",
        
        32: "\"You could be a LAWYER to help those in need! Save chefs from bad landlords and do each good deed!\"",
        
        33: "\"You could start a PODCAST! Everyone's got one! Interview your mother about how she taught you fun!\"",
        
        34: "\"Or be a PRO GAMER in esports so grand! The best Fortnite player in all of the land!\"",
        
        35: "\"Or a PROFESSIONAL MATTRESS TESTER!\" Remi said with a yawn, \"Get paid just for sleeping from dusk until dawn!\"",
        
        36: "\"Uma Thurman's HAMSTER GUARD!\" cried Zephyr with glee, \"A Maine LOBSTER FISHER on a boat called 'Corey!'\"",
        
        37: "\"You could dive for GOLF BALLS at the bottom of ponds!\" \"Or teach YODELING LESSONS to folks and beyond!\"",
        
        38: "\"You could test WATER SLIDES—wheeeee!—all day long!\" \"Or TAG MIGRATING MOOSE—but that might go wrong!\"",
        
        39: "\"You could STYLE FOOD for commercials and ads!\" \"Or APOLOGIZE professionally when companies make people mad!\"",
        
        40: "\"Your FACE could be famous on stock photos worldwide! On PowerPoints everywhere—you'd be the main slide! Or you could sell LUXURY DIRT to the richest of rich! (Yes, that's a real job—life's stranger than kitsch!)\"",
        
        41: "\"You could yodel on mountains! Teach pigeons to WALTZ! You could harvest the TEARS of Himalayan salts! Or work as a pirate (but only part-time). Professional whistler! Or poet (like this rhyme)!\"",
        
        42: "Corey's head was now SPINNING with all he had heard! So many ideas! Some quite absurd! He looked at their faces all shining with joy— His family, who loved him, this fortunate boy!",
        
        43: "(Okay, maybe not goo. That was Zephyr's idea. But you get the whole point—the future was CLEAR!) He looked at his family—his team and his crew. At Emily's smile. At the Super Three too. And something inside him switched ON like a light! His shoulders un-slumped! And his frown became BRIGHT!",
        
        44: "\"You're RIGHT!\" Corey shouted. \"This ISN'T the end! The future is waiting around every bend! I've learned how to cook! I've learned how to DREAM! I'll find my next chapter—we're all on one team!\"",
        
        45: "And Emily joined in and whispered, \"You know, Whatever comes next, we'll be RIGHT here.\"",
        
        46: "The Store stood behind them, still lovely and old, With three hundred years of stories untold. It wasn't goodbye—just \"see you later, friend.\" For stories like this one don't really end.",
        
        47: "Remember young Corey and all his great crew, And know that TOMORROW is waiting for you. Your story's not over. Not even begun! So dream your big dreams... **...so WALK RIGHT ON IN!** 🚀🎸🌟⚓🐧💎🎮📚🌮🎬 **THE END** *(...or is it just THE BEGINNING?)*"
    }
    return texts.get(page_num, "")

def get_illustration_path(page_num):
    """Get the illustration file path for a page number."""
    # Handle pages that share illustrations after the split
    illustration_map = {
        6: 5,  # Page 6 uses page 5's illustration
        8: 7,  # Page 8 uses page 7's illustration
        9: 7,  # Page 9 also uses page 7's illustration
    }
    
    actual_page = illustration_map.get(page_num, page_num)
    
    # Check multiple possible paths
    paths = [
        Path(f"final/page{actual_page}.jpg"),
        Path(f"final/page{actual_page}.png"),
        Path(f"final/page-{actual_page:02d}.jpg"),
        Path(f"final/page-{actual_page:02d}.png"),
    ]
    
    if actual_page == 0:
        paths.extend([
            Path("final/page-00-cover.jpg"),
            Path("final/page-00-cover.png"),
            Path("cartoon-characters/leonardo/Cover.jpg"),
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
    
    # If no illustration (text-only pages), just add text
    if not img_path:
        # Text-only page
        left_margin = binding_margin if is_left_page else outer_margin
        right_margin = outer_margin if is_left_page else binding_margin
        
        text_x = left_margin
        text_y = outer_margin
        text_width = page_width - left_margin - right_margin
        text_height = page_height - (2 * outer_margin) - int(0.5 * dpi)
        
        # Get text
        text = get_page_text(page_num)
        
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
            y_offset = text_y + (text_height - total_height) // 2  # Center vertically
            for line in lines:
                draw.text((text_x, y_offset), line, fill='black', font=font)
                y_offset += line_height
    else:
        # Page with illustration
        img = Image.open(img_path)
        
        # Adjust margins based on page side
        left_margin = binding_margin if is_left_page else outer_margin
        right_margin = outer_margin if is_left_page else binding_margin
        
        # Calculate available space
        available_width = page_width - left_margin - right_margin
        available_height = page_height - (2 * outer_margin)
        
        # Image takes up left 8" of available space
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
        
        # Get text
        text = get_page_text(page_num)
        
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
        
        # Get text
        text = get_page_text(page_num)
        
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
        
        # Get text
        text = get_page_text(page_num)
        
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

def create_full_book():
    """Create full book layouts with all pages."""
    # Create output directories
    os.makedirs("full_book_landscape", exist_ok=True)
    os.makedirs("full_book_portrait", exist_ok=True)
    
    # Total pages (0-47 with text-heavy pages split)
    total_pages = 48  # 0-47
    
    print("\nCreating FULL LANDSCAPE book...")
    landscape_images = []
    for i in range(total_pages):
        is_left_page = (i % 2 == 0)  # Even pages on left, odd on right
        output_path = f"full_book_landscape/page_{i:03d}.png"
        if create_landscape_page(i, output_path, is_left_page):
            print(f"  Created page {i}")
            img = Image.open(output_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            landscape_images.append(img)
    
    # Create landscape PDF
    if landscape_images:
        landscape_images[0].save(
            'The_Chef_at_the_Store_LANDSCAPE.pdf',
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=landscape_images[1:]
        )
        print(f"\n✅ Created The_Chef_at_the_Store_LANDSCAPE.pdf ({len(landscape_images)} pages)")
    
    print("\nCreating FULL PORTRAIT book...")
    portrait_images = []
    for i in range(total_pages):
        is_left_page = (i % 2 == 0)  # Even pages on left, odd on right
        output_path = f"full_book_portrait/page_{i:03d}.png"
        if create_portrait_page(i, output_path, is_left_page):
            print(f"  Created page {i}")
            img = Image.open(output_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            portrait_images.append(img)
    
    # Create portrait PDF
    if portrait_images:
        portrait_images[0].save(
            'The_Chef_at_the_Store_PORTRAIT.pdf',
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=portrait_images[1:]
        )
        print(f"\n✅ Created The_Chef_at_the_Store_PORTRAIT.pdf ({len(portrait_images)} pages)")
    
    print("\n📚 Full books created with:")
    print("   - Proper binding margins (0.5\" on binding side, 0.25\" elsewhere)")
    print("   - Text-heavy pages split for better readability")
    print("   - All 48 pages including cover")

if __name__ == "__main__":
    create_full_book()
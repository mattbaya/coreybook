# Claude AI Development Notes

This project was developed with assistance from Claude AI (Anthropic). This file contains important development context and automation instructions for future Claude sessions.

## Project Overview
**"The Chef at the Store"** - A 53-page illustrated children's book about chef Corey Wentworth who loses his restaurant but discovers infinite career possibilities with family support.

## Key Characters (with Cartoon References)
- **Corey**: Completely bald chef, reference `cartoon-characters/corey1.jpg`
- **Emily**: Short silver pixie hair, librarian, reference `cartoon-characters/emily.jpg` 
- **Remi**: 11-year-old with dark brown straight hair, reference `cartoon-characters/remi.jpg`
- **Oona**: 11-year-old with long honey blonde hair, reference `cartoon-characters/Oona.jpg`
- **Zephyr**: 9-year-old with light brown hair, reference `cartoon-characters/zephyr.jpg`
- **Matt**: Music student, reference `cartoon-characters/matt.jpg` (make much thinner)
- **Store**: The Store at Five Corners, reference `cartoon-characters/store-cartoon.jpg`

## Important Details
- **Super3 Logo**: Red diamond shield with yellow "3" and corner letters Z, O, R (reference: `images/super3v3.png`)
- **Art Style**: Modern 2D cartoon with Phil Foglio influences and cel-shading
- **Store Architecture**: Historic cream building with 4 two-story white columns
- **Page Count**: 53 pages (page-00-cover.md through page-52.md)
- **Page Structure**: Cover (0) + Content (1-51) + Back Cover (52)
- **Image Format**: All images should be square (1:1 aspect ratio)
- **Character Ethnicity**: All family members (Corey, Emily, Remi, Oona, Zephyr) are Caucasian white with same skin tone

## Automation
- **Image Generation**: `python generate_images.py` (uses Google Gemini API)
- **Generation Costs**: Various fixes and improvements (~$0.75 total)
- **New Images**: 4 new ending pages (48-51) for complete story
- **API Key**: Set `GEMINI_API_KEY` in `.env` file
- **Character Consistency**: All prompts reference cartoon character images

## Recent Updates
- **Page Consolidation**: Reduced from 56 to 53 pages with proper story ending
- **Text Synchronization**: Fixed misaligned page text (pages 39-41)
- **File Organization**: 
  - Renamed page-47-back-cover.md → page-52.md
  - Created master files: all_page_prompts.md and all_page_text.md
  - Added comprehensive automation scripts in code/ folder
- **Image Quality Improvements**:
  - Fixed 14 non-square images ($0.55)
  - Improved Store at Five Corners accuracy on page 1
  - Generated missing ending pages 48-51 with inspirational message
- **Automation Enhancements**:
  - Page synchronization verification (verify_page_sync.py)
  - Text content restoration from backups
  - Print-ready PDF generation with binding margins

## Commands to Remember
```bash
# Generate all images
python generate_images.py

# Generate specific page range
python generate_images.py --start 1 --end 10

# Create master files
python code/create_master_files.py

# Verify page synchronization
python code/verify_page_sync.py

# Fix text synchronization issues
python code/fix_page_text_sync.py

# Generate print-ready PDFs
python code/create_final_corrected_book.py

# Fix non-square images
python code/fix_non_square_images.py
```

## File Structure
- `page-prompts/` - 53 individual page prompts (page-00 through page-52)
- `character-profiles/` - Detailed character descriptions
- `cartoon-characters/leonardo/` - Generated illustrations
- `cartoon-characters/` - Visual reference images
- `images/` - Store photos and Super3 logo
- `code/` - Automation and utility scripts
- `generate_images.py` - Main image generation script
- `all_page_prompts.md` - Master file with all prompts
- `all_page_text.md` - Master file with story text only
- `art-direction.md` - Comprehensive visual style guide

## Key Generated Files
- `The_Chef_at_the_Store_FINAL_LANDSCAPE.pdf` - Print-ready landscape version
- `The_Chef_at_the_Store_FINAL_PORTRAIT.pdf` - Print-ready portrait version

## Critical Fixes Applied
- Page text/image alignment corrected via comprehensive mapping
- Original text content restored from backups
- Non-square images regenerated as perfect squares
- Complete story ending with inspirational "Rise Again" message
- Store architectural accuracy improved with detailed prompts

## Page Mapping System
The book uses a sophisticated page mapping system to ensure proper alignment:
- Physical page numbers (0-52) map to illustration numbers
- Special pages: Cover, unique pages 6&9, new ending pages 48-51
- Back cover uses dedicated montage illustration
- Text extraction and verification automated for quality control
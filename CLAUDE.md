# Claude AI Development Notes

This project was developed with assistance from Claude AI (Anthropic). This file contains important development context and automation instructions for future Claude sessions.

## Project Overview
**"The Chef at the Store"** - A 56-page illustrated children's book about chef Corey Wentworth who loses his restaurant but discovers infinite career possibilities with family support.

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
- **Page Count**: 56 pages (page-00-cover.md through page-56-back-cover.md)
- **Image Format**: All images should be square (1:1 aspect ratio)
- **Character Ethnicity**: All family members (Corey, Emily, Remi, Oona, Zephyr) are Caucasian white with same skin tone

## Automation
- **Image Generation**: `python generate_images.py` (uses Google Gemini API)
- **Estimated Cost**: $2.18 for all 56 images (56 × $0.039)
- **API Key**: Set `GEMINI_API_KEY` in `.env` file
- **Character Consistency**: All prompts reference cartoon character images

## Recent Updates
- Fixed character consistency: Remi now has straight dark brown hair (not curly)
- Added explicit Caucasian/white ethnicity to all family members for consistency
- Updated all prompts to generate square images (1:1 aspect ratio)
- Fixed Leonardo prompt duplication issues
- Clarified panel labels are for organization only (not to appear in images)
- Added guitar tutor career fantasy (page 34)
- Updated lobster fishing with "Corey Chaos" boat from Verona Island, Maine
- Enhanced automation with cartoon character references
- Integrated store architectural details (4 white columns)

## Commands to Remember
```bash
# Generate all images
python generate_images.py

# Generate specific page range
python generate_images.py --start 1 --end 10

# Update Super3 logo references
python update_super3_logo.py

# Update store references  
python update_store_references.py
```

## File Structure
- `page-prompts/` - 56 individual page prompts
- `character-profiles/` - Detailed character descriptions
- `cartoon-characters/` - Visual reference images
- `images/` - Store photos and Super3 logo
- `generate_images.py` - Main automation script
- `art-direction.md` - Comprehensive visual style guide
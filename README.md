# The Chef at the Store

A heartwarming 53-page illustrated children's book about infinite possibilities, family support, and finding hope when one chapter ends.

## 📖 Story Summary

Meet Corey Wentworth, a chef whose beloved restaurant at The Store at Five Corners faces unexpected closure. When his loving family arrives to rescue him from despair, they embark on an imaginative journey exploring dozens of possible career paths - from astronaut to punk rocker, from Uma Thurman's hamster guard to GWAR special effects engineer. 

This story celebrates the power of family love, the magic of imagination, and the truth that every ending is just a new beginning waiting to happen.

## 🎨 Visual Style

- **Art Direction**: Modern 2D cartoon style with Phil Foglio influences
- **Technique**: Cel-shading with bold outlines and flat colors
- **Character Design**: Expressive faces, dynamic poses, family-friendly aesthetic
- **Setting**: Historic New England charm meets whimsical cartoon adventure

## 👨‍👩‍👧‍👦 Main Characters

### The Wentworth Family
- **Corey**: The completely bald chef with infinite potential (Caucasian)
- **Emily**: The supportive wife and librarian with short silver pixie hair (Caucasian)
- **The Super Three**: Remi (11, boy, dark brown straight hair), Oona (11, girl, honey blonde hair), and Zephyr (9, girl, light brown hair) - the superhero children in blue shirts (all Caucasian)

### Supporting Characters  
- **Matt**: Guitar student with questionable musical abilities
- **The Store at Five Corners**: Historic 1787 building with 4 two-story white columns

## 📄 Book Structure

**53 Total Pages (0-52):**
- Cover page (page-00-cover.md)
- Story pages 1-51
- Back cover (page-52.md)

**Key Story Sections:**
- The store closure and Corey's despair
- Family rescue and support
- Career brainstorming sessions with wild fantasies
- Real customer reviews and community love
- New beginnings and infinite possibilities

## 🤖 Image Generation

This project includes automated image generation using Google's Gemini API:

```bash
# Generate all images
python generate_images.py

# Generate specific pages
python generate_images.py --start 1 --end 10

# Create master files
python code/create_master_files.py
```

**Features:**
- Consistent character appearance via cartoon reference images
- Square image format (1:1 aspect ratio) for all illustrations
- Proper Super3 logo integration (not generic Superman logo)
- Phil Foglio cartoon style with cel-shading
- Explicit character ethnicity for consistent rendering
- Panel labels clarified as organizational only (not in images)
- Cost tracking: ~$0.039 per image

## 🏪 The Real Store

Based on the actual **Store at Five Corners** in Williamstown, Massachusetts - a historic general store established in 1787 that serves as a real community gathering place.

## 🎭 Career Fantasy Highlights

The story features dozens of imaginative career possibilities including:
- **Astronaut** (with Space Café on Mars!)
- **Punk Rock Guitarist** for band "Big Dogs"  
- **Sea Captain** sailing with dolphins
- **Uma Thurman's Hamster Guard** (with tiny security checkpoint)
- **Maine Lobster Fisherman** on boat "Corey Chaos"
- **GWAR Special Effects Engineer** (pouring fake blood!)
- **Guitar Tutor** (suffering through Matt's "I'm a Vegetarian Now!")

## 📁 Project Structure

```
CoreyBook/
├── page-prompts/           # 53 individual page descriptions
├── character-profiles/     # Detailed character references  
├── cartoon-characters/     # Visual reference images
├── images/                 # Photos and logos
├── code/                   # Automation scripts
├── generate_images.py      # AI image generation script
├── all_page_prompts.md     # Master file with all prompts
├── all_page_text.md        # Master file with story text only
├── art-direction.md        # Complete visual style guide
├── CLAUDE.md              # AI development notes
└── README.md              # This file
```

## 🚀 Getting Started

1. **Set up environment:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```

3. **Generate images:**
   ```bash
   python generate_images.py
   ```

## 💰 Cost Estimate

- **Total Pages**: 53 (4 new ending pages generated)
- **Cost Per Image**: $0.039  
- **Recent Generation Costs**: 
  - Page 1 accuracy improvements: $0.039
  - Non-square image fixes (14 images): $0.55
  - New ending pages: $0.156

## 🎨 Art References

All character designs reference cartoon illustrations in the `cartoon-characters/leonardo/` folder to ensure visual consistency across all pages. The art style combines modern 2D animation techniques with Phil Foglio's expressive character work.

## 📝 Development Notes

This project was developed with AI assistance. See `CLAUDE.md` for technical development context, automation details, and important character/story specifications.

### Recent Updates
- **Page Structure**: Consolidated from 56 to 53 pages with proper ending
- **Text Synchronization**: Fixed page text alignment issues
- **File Organization**: Renamed page-47-back-cover.md → page-52.md
- **Master Files**: Created all_page_prompts.md and all_page_text.md
- **Image Quality**: Fixed non-square images, improved Store accuracy
- **Automation**: Added comprehensive verification and fix scripts in code/ folder

---

*A story about discovering that when one door closes, infinite windows open - you just need family to help you see them all.*
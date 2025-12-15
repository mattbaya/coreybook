# Image Generation Automation for "The Chef at the Store"

This automation script generates all 50 book illustrations using Google's nano-banana (Gemini 2.5 Flash Image) API.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
1. Get API key from: https://makersuite.google.com/app/apikey
2. Create `.env` file in project root:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   GOOGLE_AI_API_KEY=your_actual_api_key_here
   ```

### 3. Verify File Structure
Make sure you have:
```
CoreyBook/
├── page-prompts/           # 50 individual page prompt files
├── character-profiles/     # Character consistency files
├── art-direction.md       # Visual style guide  
├── generate_images.py     # Main automation script
└── requirements.txt       # Python dependencies
```

## Usage

### Generate All Images (1-50)
```bash
python generate_images.py
```

### Generate Specific Range
```bash
# Just Book 1 (pages 1-10)
python generate_images.py --start 1 --end 10

# Books 3-4 (pages 21-40)  
python generate_images.py --start 21 --end 40
```

### Custom Options
```bash
python generate_images.py \\
  --output my_images \\
  --delay 3.0 \\
  --start 5 \\
  --end 15
```

## Script Features

### ✅ Automatic Prompt Enhancement
- Combines page image prompts with character profiles
- Includes art direction guidelines
- Adds story context for better results

### ✅ Character Consistency
- References detailed character profiles (Corey's baldness, Emily's silver hair, etc.)
- Maintains visual consistency across all 50 images
- Uses character-specific styling notes

### ✅ Cost Management
- Tracks cost in real-time ($0.039 per image)
- Estimates total cost before starting
- Shows actual cost at completion

### ✅ Error Handling
- Retries failed generations (up to 3 attempts)
- Skips existing images (resume capability)
- Graceful error handling with detailed logging

### ✅ Rate Limiting
- Built-in delays between API calls
- Respects Gemini API limits
- Configurable request timing

## Cost Estimation

| Images | Cost |
|--------|------|
| 10 pages (1 book) | $0.39 |
| 25 pages | $0.98 |
| 50 pages (all books) | $1.95 |

## Output Structure

Generated images will be saved as:
```
generated_images/
├── book1-page01.png
├── book1-page02.png
├── ...
├── book5-page09.png
└── book5-page10.png
```

## Character Profiles Used

The script automatically includes:
- **Corey**: Completely bald, navy apron, warm smile
- **Emily**: Short silver pixie hair, confident demeanor  
- **Remi**: Dark curly hair, blue Super3 shirt, brave leader
- **Oona**: Long honey blonde hair, blue Super3 shirt, joyful energy
- **Zephyr**: Light brown messy hair, blue Super3 shirt, loudest voice

## Art Style Applied

All images use **modern 2D cartoon style with cel-shading**:
- Bold, clean outlines
- Flat colors with cel-shading
- No gradients - sharp shadow edges
- Contemporary animation aesthetic
- High contrast for print reproduction

## Troubleshooting

### API Key Issues
```bash
# Test your API key
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('API key works!')"
```

### Rate Limiting
If you hit rate limits, increase delay:
```bash
python generate_images.py --api-key YOUR_KEY --delay 5.0
```

### Resume Failed Generation
The script automatically skips existing images, so just re-run:
```bash
python generate_images.py --api-key YOUR_KEY
```

### Character Reference Images

If you have reference images for characters:
1. Place them in `character-profiles/images/`
2. Update character profile .md files with image paths
3. The script will include them in prompts for better consistency

## Advanced Usage

### Test Single Page
```bash
python generate_images.py --api-key YOUR_KEY --start 1 --end 1
```

### Generate Books Separately
```bash
# Book 1
python generate_images.py --api-key YOUR_KEY --start 1 --end 10 --output book1_images

# Book 2  
python generate_images.py --api-key YOUR_KEY --start 11 --end 20 --output book2_images
```

## Integration with Your Workflow

1. **Generate test images** first (1-2 pages) to verify style
2. **Review and adjust** character profiles if needed
3. **Generate in batches** by book for easier review
4. **Use generated images** as reference for human artists or further AI refinement

This automation gives you a complete set of consistent illustrations ready for your book production process!
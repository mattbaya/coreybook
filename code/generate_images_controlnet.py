#!/usr/bin/env python3
"""
Generate images using ControlNet on Replicate for character consistency.
Uses reference images to maintain consistent character appearance.
"""

import os
import time
import glob
import json
import replicate
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse
from dotenv import load_dotenv
import requests
import base64
from PIL import Image
import io

# Load environment variables
load_dotenv()

class ControlNetGenerator:
    def __init__(self, api_token: str, output_dir: str = "generated_images/controlnet"):
        """
        Initialize the ControlNet generator.
        
        Args:
            api_token: Replicate API token
            output_dir: Directory to save generated images
        """
        self.api_token = api_token
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up Replicate client
        os.environ["REPLICATE_API_TOKEN"] = api_token
        
        # Rate limiting
        self.request_delay = 2.0
        
        # Cost tracking
        self.cost_per_image = 0.034  # $0.034 per ControlNet generation
        self.generated_count = 0
        self.total_cost = 0.0
        
        # Load reference images
        self.reference_images = self.load_reference_images()
        
    def load_reference_images(self) -> Dict[str, str]:
        """Load and encode reference images as base64."""
        references = {}
        ref_paths = {
            "corey": "cartoon-characters/corey1.jpg",
            "emily": "cartoon-characters/emily.jpg",
            "store": "cartoon-characters/store-cartoon.jpg",
            "family": "cartoon-characters/wentworth-family-foglio.jpg"
        }
        
        for name, path in ref_paths.items():
            if os.path.exists(path):
                with open(path, "rb") as f:
                    image_data = f.read()
                    # Convert to data URI
                    base64_data = base64.b64encode(image_data).decode()
                    references[name] = f"data:image/jpeg;base64,{base64_data}"
                print(f"✅ Loaded reference: {name}")
            else:
                print(f"❌ Reference not found: {path}")
                
        return references
    
    def load_page_prompt(self, file_path: Path) -> Dict:
        """Load and parse a page prompt markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('# ', '') if lines else "Unknown Page"
        
        # Extract sections
        page_text = ""
        image_prompt = ""
        
        in_page_text = False
        in_image_prompt = False
        
        for line in lines:
            if line.startswith("## PAGE TEXT"):
                in_page_text = True
                in_image_prompt = False
                continue
            elif line.startswith("## IMAGE PROMPT"):
                in_page_text = False
                in_image_prompt = True
                continue
            elif line.startswith("## "):
                in_page_text = False
                in_image_prompt = False
                continue
            
            if in_page_text and line.strip():
                page_text += line.strip() + " "
            elif in_image_prompt and line.strip() and not line.startswith("**Art Style**"):
                image_prompt += line.strip() + " "
        
        return {
            'title': title.strip(),
            'page_text': page_text.strip(), 
            'image_prompt': image_prompt.strip(),
            'file_path': str(file_path)
        }
    
    def create_controlnet_prompt(self, page_data: Dict) -> str:
        """Create a prompt optimized for ControlNet consistency."""
        
        # Simpler, more direct prompt for ControlNet
        prompt = "children's book illustration, cartoon style, "
        
        # Add the scene description
        prompt += page_data['image_prompt']
        
        # Key character descriptions (brief)
        prompt += " Corey is a completely bald chef in navy apron. "
        prompt += "Modern 2D cartoon style, bright colors, clean lines."
        
        return prompt
    
    def determine_reference_image(self, page_data: Dict) -> Optional[str]:
        """Determine which reference image to use based on the scene."""
        prompt_lower = page_data['image_prompt'].lower()
        
        # Priority order for reference selection
        if "corey" in prompt_lower:
            if "family" in prompt_lower or "emily" in prompt_lower:
                return self.reference_images.get("family")
            else:
                return self.reference_images.get("corey")
        elif "store" in prompt_lower and "building" in prompt_lower:
            return self.reference_images.get("store")
        elif "emily" in prompt_lower:
            return self.reference_images.get("emily")
        else:
            # Default to Corey since he's the main character
            return self.reference_images.get("corey")
    
    def generate_image(self, prompt: str, reference_image: str, output_path: Path) -> bool:
        """Generate a single image using ControlNet."""
        
        try:
            print(f"  Generating with ControlNet...")
            print(f"  Using reference: {reference_image[:50]}..." if reference_image else "  No reference image")
            
            # Using the rossjillian/controlnet model
            output = replicate.run(
                "rossjillian/controlnet:795433b19458d0f4fa172a7ccf93178d2adb1cb8ab2ad6c8fdc33fdbcd49f477",
                input={
                    "prompt": prompt,
                    "image": reference_image,
                    "scale": 7,  # How closely to follow the prompt
                    "num_samples": 1,
                    "ddim_steps": 20,
                    "seed": -1,  # Random seed
                    "eta": 0.0,
                    "a_prompt": "best quality, extremely detailed, cartoon illustration, children's book",
                    "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, blurry",
                }
            )
            
            # Download the generated image
            if output and len(output) > 0:
                image_url = output[0]
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    self.generated_count += 1
                    self.total_cost += self.cost_per_image
                    
                    file_size_mb = len(response.content) / (1024 * 1024)
                    print(f"  ✅ Image saved: {output_path} ({file_size_mb:.1f} MB)")
                    print(f"  💰 Cost: ${self.cost_per_image:.3f}")
                    
                    return True
            
            print("  ❌ No image generated")
            return False
                
        except Exception as e:
            print(f"  ❌ Error generating image: {str(e)}")
            return False
    
    def generate_all_images(self, prompts_dir: str = "page-prompts", 
                          start_page: int = 0, end_page: int = 3) -> None:
        """Generate images for specified pages using ControlNet."""
        
        print(f"🎨 Starting ControlNet generation for pages {start_page}-{end_page}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🔧 Using reference images for consistency")
        
        # Find page files
        prompt_files = sorted(glob.glob(f"{prompts_dir}/page-*.md"))
        
        if not prompt_files:
            print(f"❌ No page prompt files found in {prompts_dir}")
            return
            
        # Filter to requested range
        if start_page == 0:
            start_idx = 0
        else:
            start_idx = start_page
            
        if end_page >= 56:
            end_idx = len(prompt_files)
        else:
            end_idx = end_page + 1
        
        selected_files = prompt_files[start_idx:end_idx]
        estimated_cost = len(selected_files) * self.cost_per_image
        
        print(f"📄 Generating {len(selected_files)} images")
        print(f"💰 Estimated cost: ${estimated_cost:.2f}")
        
        # Generate images
        start_time = datetime.now()
        success_count = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            output_path = self.output_dir / f"{base_name}.png"
            
            print(f"\n🖼️  [{i}/{len(selected_files)}] Processing {base_name}...")
            
            try:
                # Load page data
                page_data = self.load_page_prompt(file_path)
                print(f"   Title: {page_data['title']}")
                
                # Create prompt
                prompt = self.create_controlnet_prompt(page_data)
                
                # Determine reference image
                reference_image = self.determine_reference_image(page_data)
                
                # Generate image
                if self.generate_image(prompt, reference_image, output_path):
                    success_count += 1
                else:
                    print(f"   ❌ Failed to generate image for {base_name}")
                
                # Rate limiting
                if i < len(selected_files):
                    print(f"   ⏳ Waiting {self.request_delay}s...")
                    time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"   ❌ Error processing {base_name}: {str(e)}")
                continue
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n📊 ControlNet Generation Summary:")
        print(f"   ✅ Successful: {success_count}/{len(selected_files)}")
        print(f"   💰 Actual cost: ${self.total_cost:.2f}")
        print(f"   ⏱️  Total time: {duration}")
        print(f"   📁 Images saved to: {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate images using ControlNet")
    parser.add_argument("--token", help="Replicate API token (or set REPLICATE_API_TOKEN)")
    parser.add_argument("--output", default="generated_images/controlnet", help="Output directory")
    parser.add_argument("--start", type=int, default=0, help="Start page")
    parser.add_argument("--end", type=int, default=3, help="End page")
    
    args = parser.parse_args()
    
    # Get API token
    api_token = args.token or os.getenv('REPLICATE_API_TOKEN')
    
    if not api_token:
        print("❌ Replicate API token required!")
        print("   Get one at: https://replicate.com/account/api-tokens")
        print("   Set REPLICATE_API_TOKEN in .env or use --token")
        return
    
    # Create generator
    generator = ControlNetGenerator(api_token, args.output)
    
    # Generate images
    generator.generate_all_images(
        start_page=args.start,
        end_page=args.end
    )

if __name__ == "__main__":
    main()
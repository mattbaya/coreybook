#!/usr/bin/env python3
"""
Generate images using Hyperbolic AI's Stable Diffusion API.
Cost-effective at ~$0.01 per image.
"""

import os
import time
import glob
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HyperbolicGenerator:
    def __init__(self, api_key: str, output_dir: str = "generated_images/hyperbolic"):
        """
        Initialize the Hyperbolic AI generator.
        
        Args:
            api_key: Hyperbolic AI API key
            output_dir: Directory to save generated images
        """
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # API endpoint
        self.api_url = "https://api.hyperbolic.xyz/v1/image/generation"
        
        # Rate limiting
        self.request_delay = 1.0
        
        # Cost tracking
        self.cost_per_image = 0.01  # $0.01 per image
        self.generated_count = 0
        self.total_cost = 0.0
        
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
    
    def create_sd_prompt(self, page_data: Dict) -> str:
        """Create a prompt optimized for Stable Diffusion."""
        
        # Start with quality tags
        prompt = "(best quality:1.2), (masterpiece:1.2), ultra-detailed, "
        
        # Art style
        prompt += "children's book illustration, cartoon style, cel-shading, bold outlines, "
        
        # Character consistency emphasis
        prompt += "CONSISTENT CHARACTER DESIGN: Corey the chef - completely bald head, no hair, shiny bald, round face, navy blue apron, "
        
        # Scene description
        prompt += page_data['image_prompt']
        
        # Additional style tags
        prompt += ", vibrant colors, professional illustration, clean artwork"
        
        return prompt
    
    def generate_image(self, prompt: str, output_path: Path, model: str = "SDXL1.0-base") -> bool:
        """Generate a single image using Hyperbolic AI."""
        
        try:
            print(f"  Generating with Hyperbolic AI ({model})...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model_name": model,
                "prompt": prompt,
                "height": 1024,
                "width": 1024,
                "backend": "auto",
                "negative_prompt": "low quality, blurry, pixelated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers",
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "num_images": 1,
                "seed": -1  # Random seed
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Get image data (base64 or URL)
                if "images" in result and len(result["images"]) > 0:
                    image_data = result["images"][0]
                    
                    # If it's base64
                    if image_data.get("image"):
                        import base64
                        image_bytes = base64.b64decode(image_data["image"])
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                    # If it's a URL
                    elif image_data.get("url"):
                        img_response = requests.get(image_data["url"])
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                    else:
                        print("  ❌ No image data in response")
                        return False
                    
                    self.generated_count += 1
                    self.total_cost += self.cost_per_image
                    
                    print(f"  ✅ Image saved: {output_path}")
                    print(f"  💰 Cost: ${self.cost_per_image:.3f}")
                    
                    return True
                else:
                    print("  ❌ No images in response")
                    return False
            else:
                print(f"  ❌ API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error generating image: {str(e)}")
            return False
    
    def generate_all_images(self, prompts_dir: str = "page-prompts", 
                          start_page: int = 0, end_page: int = 3) -> None:
        """Generate images for specified pages using Hyperbolic AI."""
        
        print(f"🎨 Starting Hyperbolic AI generation for pages {start_page}-{end_page}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"💰 Low cost: $0.01 per image")
        
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
                prompt = self.create_sd_prompt(page_data)
                
                # Generate image
                if self.generate_image(prompt, output_path):
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
        
        print(f"\n📊 Hyperbolic AI Generation Summary:")
        print(f"   ✅ Successful: {success_count}/{len(selected_files)}")
        print(f"   💰 Actual cost: ${self.total_cost:.2f}")
        print(f"   ⏱️  Total time: {duration}")
        print(f"   📁 Images saved to: {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate images using Hyperbolic AI")
    parser.add_argument("--api-key", help="Hyperbolic AI API key (or set HYPERBOLIC_API_KEY)")
    parser.add_argument("--output", default="generated_images/hyperbolic", help="Output directory")
    parser.add_argument("--start", type=int, default=0, help="Start page")
    parser.add_argument("--end", type=int, default=3, help="End page")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('HYPERBOLIC_API_KEY')
    
    if not api_key:
        print("❌ Hyperbolic AI API key required!")
        print("   Get one at: https://hyperbolic.ai")
        print("   Set HYPERBOLIC_API_KEY in .env or use --api-key")
        print("\n💡 Note: You'll need to sign up for a Hyperbolic account first")
        return
    
    # Create generator
    generator = HyperbolicGenerator(api_key, args.output)
    
    # Generate images
    generator.generate_all_images(
        start_page=args.start,
        end_page=args.end
    )

if __name__ == "__main__":
    main()
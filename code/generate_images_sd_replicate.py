#!/usr/bin/env python3
"""
Generate images using standard Stable Diffusion XL on Replicate.
Most affordable option at ~$0.012 per image.
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

# Load environment variables
load_dotenv()

class SDReplicateGenerator:
    def __init__(self, api_token: str, output_dir: str = "generated_images/sd_replicate"):
        """
        Initialize the SD Replicate generator.
        
        Args:
            api_token: Replicate API token
            output_dir: Directory to save generated images
        """
        self.api_token = api_token
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up Replicate
        os.environ["REPLICATE_API_TOKEN"] = api_token
        
        # Rate limiting
        self.request_delay = 1.0
        
        # Cost tracking
        self.cost_per_image = 0.012  # ~$0.012 per SDXL generation
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
    
    def create_sdxl_prompt(self, page_data: Dict) -> str:
        """Create a prompt optimized for SDXL."""
        
        # SDXL responds well to natural language descriptions
        prompt = "Professional children's book illustration, cartoon style with cel-shading. "
        
        # Emphasize character consistency
        prompt += "IMPORTANT: Corey is a completely bald chef (no hair at all) wearing a navy blue apron. "
        prompt += "He has a round friendly face and warm smile. "
        
        # Add the scene
        prompt += page_data['image_prompt']
        
        # Style reinforcement
        prompt += " Modern 2D animation style, bright saturated colors, bold black outlines, "
        prompt += "expressive characters, Phil Foglio inspired artwork, high quality illustration"
        
        return prompt
    
    def generate_image(self, prompt: str, output_path: Path) -> bool:
        """Generate a single image using SDXL on Replicate."""
        
        try:
            print(f"  Generating with SDXL on Replicate...")
            
            # Using Stable Diffusion XL
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "width": 1024,
                    "height": 1024,
                    "prompt": prompt,
                    "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5,
                    "scheduler": "K_EULER",
                    "seed": -1,  # Random seed
                    "num_outputs": 1,
                    "refine": "expert_ensemble_refiner",
                    "high_noise_frac": 0.8
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
        """Generate images for specified pages using SDXL."""
        
        print(f"🎨 Starting SDXL/Replicate generation for pages {start_page}-{end_page}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"💰 Affordable: ~$0.012 per image")
        
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
                prompt = self.create_sdxl_prompt(page_data)
                
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
        
        print(f"\n📊 SDXL/Replicate Generation Summary:")
        print(f"   ✅ Successful: {success_count}/{len(selected_files)}")
        print(f"   💰 Actual cost: ${self.total_cost:.2f}")
        print(f"   ⏱️  Total time: {duration}")
        print(f"   📁 Images saved to: {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate images using SDXL on Replicate")
    parser.add_argument("--token", help="Replicate API token (or set REPLICATE_API_TOKEN)")
    parser.add_argument("--output", default="generated_images/sd_replicate", help="Output directory")
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
    generator = SDReplicateGenerator(api_token, args.output)
    
    # Generate images
    generator.generate_all_images(
        start_page=args.start,
        end_page=args.end
    )

if __name__ == "__main__":
    main()
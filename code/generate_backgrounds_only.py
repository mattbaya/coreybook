#!/usr/bin/env python3
"""
Generate background scenes only using Hyperbolic AI.
Then manually composite Corey from reference images for perfect consistency.
"""

import os
import time
import glob
from pathlib import Path
from datetime import datetime
import argparse
from dotenv import load_dotenv
import requests
import json

load_dotenv()

class BackgroundGenerator:
    def __init__(self, api_key: str, output_dir: str = "generated_images/backgrounds"):
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_url = "https://api.hyperbolic.xyz/v1/image/generation"
        self.request_delay = 1.0
        self.cost_per_image = 0.01
        self.generated_count = 0
        self.total_cost = 0.0
        
    def load_page_prompt(self, file_path: Path) -> dict:
        """Load page prompt."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('# ', '') if lines else "Unknown Page"
        
        image_prompt = ""
        in_image_prompt = False
        
        for line in lines:
            if line.startswith("## IMAGE PROMPT"):
                in_image_prompt = True
                continue
            elif line.startswith("## "):
                in_image_prompt = False
                continue
            
            if in_image_prompt and line.strip():
                image_prompt += line.strip() + " "
        
        return {
            'title': title.strip(),
            'image_prompt': image_prompt.strip()
        }
    
    def create_background_prompt(self, page_data: dict) -> str:
        """Create prompt focused on backgrounds and settings, not characters."""
        
        # Remove character descriptions, focus on setting/background
        prompt = page_data['image_prompt']
        
        # Replace character mentions with placeholder or remove
        replacements = {
            'Corey': 'a person',
            'chef': 'person',
            'Emily': 'a person', 
            'Remi': 'a child',
            'Oona': 'a child',
            'Zephyr': 'a child'
        }
        
        for old, new in replacements.items():
            prompt = prompt.replace(old, new)
        
        # Add background focus
        background_prompt = "detailed background scene, "
        background_prompt += prompt
        background_prompt += " empty scene without main characters, children's book illustration style, cartoon, vibrant colors, detailed environment"
        
        return background_prompt
    
    def generate_background(self, prompt: str, output_path: Path) -> bool:
        """Generate background scene."""
        try:
            print(f"  Generating background...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model_name": "SDXL1.0-base",
                "prompt": prompt,
                "height": 1024,
                "width": 1024,
                "negative_prompt": "people, characters, faces, person, human, chef, children",
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "num_images": 1,
                "seed": -1
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if "images" in result and len(result["images"]) > 0:
                    image_data = result["images"][0]
                    
                    if image_data.get("image"):
                        import base64
                        image_bytes = base64.b64decode(image_data["image"])
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                    elif image_data.get("url"):
                        img_response = requests.get(image_data["url"])
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                    else:
                        return False
                    
                    self.generated_count += 1
                    self.total_cost += self.cost_per_image
                    print(f"  ✅ Background saved: {output_path}")
                    return True
            
            print(f"  ❌ API error: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def generate_all_backgrounds(self, prompts_dir: str = "page-prompts", 
                                start_page: int = 0, end_page: int = 3):
        """Generate background scenes for all pages."""
        
        print(f"🎨 Generating backgrounds for pages {start_page}-{end_page}")
        print(f"📁 Output: {self.output_dir}")
        print("🎯 Strategy: Generate backgrounds only, manually add characters later")
        
        prompt_files = sorted(glob.glob(f"{prompts_dir}/page-*.md"))
        
        if not prompt_files:
            print(f"❌ No page files found in {prompts_dir}")
            return
            
        if start_page == 0:
            start_idx = 0
        else:
            start_idx = start_page
            
        end_idx = min(len(prompt_files), end_page + 1)
        selected_files = prompt_files[start_idx:end_idx]
        
        estimated_cost = len(selected_files) * self.cost_per_image
        print(f"💰 Estimated cost: ${estimated_cost:.2f}")
        
        start_time = datetime.now()
        success_count = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            output_path = self.output_dir / f"{base_name}_background.png"
            
            print(f"\n🖼️ [{i}/{len(selected_files)}] {base_name}...")
            
            try:
                page_data = self.load_page_prompt(file_path)
                print(f"   Title: {page_data['title']}")
                
                background_prompt = self.create_background_prompt(page_data)
                print(f"   Prompt: {background_prompt[:80]}...")
                
                if self.generate_background(background_prompt, output_path):
                    success_count += 1
                
                if i < len(selected_files):
                    time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        duration = datetime.now() - start_time
        print(f"\n📊 Background Generation Complete:")
        print(f"   ✅ Generated: {success_count}/{len(selected_files)}")
        print(f"   💰 Cost: ${self.total_cost:.2f}")
        print(f"   ⏱️ Time: {duration}")
        
        if success_count > 0:
            print(f"\n🎯 Next Steps:")
            print(f"   1. Download backgrounds from: {self.output_dir}")
            print(f"   2. Use photo editing software (GIMP, Photoshop, Photopea.com)")
            print(f"   3. Composite Corey from cartoon-characters/corey1.jpg onto backgrounds")
            print(f"   4. Perfect character consistency guaranteed!")

def main():
    parser = argparse.ArgumentParser(description="Generate background scenes only")
    parser.add_argument("--api-key", help="Hyperbolic API key")
    parser.add_argument("--start", type=int, default=0, help="Start page")
    parser.add_argument("--end", type=int, default=3, help="End page")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv('HYPERBOLIC_API_KEY')
    
    if not api_key:
        print("❌ Hyperbolic API key required!")
        return
    
    generator = BackgroundGenerator(api_key)
    generator.generate_all_backgrounds(
        start_page=args.start,
        end_page=args.end
    )

if __name__ == "__main__":
    main()
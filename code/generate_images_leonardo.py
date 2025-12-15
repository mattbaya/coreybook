#!/usr/bin/env python3
"""
Generate images using Leonardo.ai API from leonardo/ prompts.
"""

import os
import time
import json
import requests
from pathlib import Path
import glob
import re

class LeonardoImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}"
        }
        self.output_dir = "generated_images/leonardo"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_user_info(self):
        """Get user information and available tokens."""
        response = requests.get(
            f"{self.base_url}/me", 
            headers=self.headers
        )
        if response.status_code == 200:
            data = response.json()
            # Handle different response formats
            if isinstance(data, dict):
                user_details = data.get('user_details', {})
                if isinstance(user_details, dict):
                    tokens = user_details.get('tokenBalance', 'Unknown')
                else:
                    tokens = 'Unknown'
                print(f"✅ API Connected - Tokens available: {tokens}")
            else:
                print(f"✅ API Connected - Response: {data}")
            return data
        else:
            print(f"❌ API Connection failed: {response.status_code} - {response.text}")
            return None

    def create_generation(self, prompt, negative_prompt, page_num):
        """Create an image generation job."""
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "modelId": "6b645e3a-d64f-4341-a6d8-7a3690fbf042",  # Leonardo Anime XL
            "width": 1024,
            "height": 1024,
            "num_images": 1,
            "guidance_scale": 7,
            "num_inference_steps": 30,
            "scheduler": "LEONARDO",
            "public": False,
            "tiling": False,
            "alchemy": True,  # Enable Alchemy for better quality
            "photoReal": False,  # Keep false for cartoon style
            "presetStyle": "ILLUSTRATION"  # Use illustration preset for cartoon style
        }
        
        response = requests.post(
            f"{self.base_url}/generations",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            generation_id = data.get("sdGenerationJob", {}).get("generationId")
            print(f"✅ Generation started for page {page_num}: {generation_id}")
            return generation_id
        else:
            print(f"❌ Generation failed for page {page_num}: {response.status_code} - {response.text}")
            return None

    def check_generation_status(self, generation_id):
        """Check the status of a generation job."""
        response = requests.get(
            f"{self.base_url}/generations/{generation_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            generation = data.get("generations_by_pk", {})
            status = generation.get("status")
            
            if status == "COMPLETE":
                images = generation.get("generated_images", [])
                if images:
                    return {
                        "status": "complete",
                        "url": images[0].get("url")
                    }
            elif status == "FAILED":
                return {"status": "failed"}
            else:
                return {"status": "pending"}
        
        return {"status": "error"}

    def download_image(self, url, page_num):
        """Download image from URL."""
        output_path = f"{self.output_dir}/page-{page_num:02d}.png"
        
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {output_path}")
            return True
        else:
            print(f"❌ Download failed for page {page_num}")
            return False

    def process_page(self, prompt_file):
        """Process a single page prompt file."""
        # Extract page number from filename
        filename = Path(prompt_file).name
        match = re.search(r'page-(\d+)', filename)
        if match:
            page_num = int(match.group(1))
        else:
            print(f"❌ Could not extract page number from {filename}")
            return False
        
        # Read prompt and negative prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract prompts
        prompt_match = re.search(r'\[PROMPT\]\n(.+?)(?=\n\n\[NEGATIVE PROMPT\])', content, re.DOTALL)
        negative_match = re.search(r'\[NEGATIVE PROMPT\]\n(.+?)(?=\n*$)', content, re.DOTALL)
        
        if not prompt_match:
            print(f"❌ Could not extract prompt from {filename}")
            return False
        
        prompt = prompt_match.group(1).strip()
        negative_prompt = negative_match.group(1).strip() if negative_match else ""
        
        print(f"\n📄 Processing page {page_num}...")
        print(f"   Prompt: {prompt[:60]}...")
        
        # Create generation
        generation_id = self.create_generation(prompt, negative_prompt, page_num)
        if not generation_id:
            return False
        
        # Poll for completion
        max_attempts = 60  # 5 minutes max
        for attempt in range(max_attempts):
            time.sleep(5)  # Check every 5 seconds
            
            result = self.check_generation_status(generation_id)
            
            if result["status"] == "complete":
                # Download the image
                return self.download_image(result["url"], page_num)
            elif result["status"] == "failed":
                print(f"❌ Generation failed for page {page_num}")
                return False
            elif result["status"] == "pending":
                if attempt % 6 == 0:  # Print status every 30 seconds
                    print(f"   ⏳ Still generating... ({attempt * 5}s)")
        
        print(f"❌ Generation timed out for page {page_num}")
        return False

    def generate_all(self, start_page=0, end_page=None):
        """Generate all images from leonardo prompts."""
        # Get all prompt files
        prompt_files = glob.glob("leonardo/page-*-leonardo.txt")
        prompt_files.sort()
        
        if end_page is not None:
            prompt_files = [f for f in prompt_files if self._get_page_num(f) >= start_page and self._get_page_num(f) <= end_page]
        else:
            prompt_files = [f for f in prompt_files if self._get_page_num(f) >= start_page]
        
        print(f"\n🎨 Leonardo.ai Image Generation")
        print(f"📄 Found {len(prompt_files)} prompts to process")
        
        # Check API connection
        if not self.get_user_info():
            return
        
        successful = 0
        failed = 0
        
        for i, prompt_file in enumerate(prompt_files):
            print(f"\n{'='*50}")
            print(f"Progress: {i+1}/{len(prompt_files)}")
            
            if self.process_page(prompt_file):
                successful += 1
            else:
                failed += 1
            
            # Rate limiting - Leonardo has limits
            if i < len(prompt_files) - 1:
                print("⏳ Waiting 10s before next generation...")
                time.sleep(10)
        
        print(f"\n{'='*50}")
        print(f"📊 Generation Complete!")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Output folder: {self.output_dir}")
    
    def _get_page_num(self, filename):
        """Extract page number from filename."""
        match = re.search(r'page-(\d+)', filename)
        return int(match.group(1)) if match else -1

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate images using Leonardo.ai API')
    parser.add_argument('--start', type=int, default=0, help='Starting page number')
    parser.add_argument('--end', type=int, help='Ending page number')
    parser.add_argument('--api-key', default="78cc6ab2-acc1-4365-beb2-ac16762ad8b6", help='Leonardo API key')
    
    args = parser.parse_args()
    
    generator = LeonardoImageGenerator(args.api_key)
    generator.generate_all(args.start, args.end)

if __name__ == "__main__":
    main()
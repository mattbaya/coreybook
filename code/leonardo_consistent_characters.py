#!/usr/bin/env python3
"""
Generate consistent characters using Leonardo.ai's Character Reference and Fixed Seed features.
"""

import os
import time
import json
import requests
from pathlib import Path
import glob
import re

class LeonardoConsistentCharacterGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}"
        }
        self.output_dir = "generated_images/leonardo_consistent"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Store character seeds for consistency
        self.character_seeds = {
            "corey": None,      # Bald chef
            "emily": None,      # Silver pixie cut
            "remi": None,       # Dark curly hair boy
            "oona": None,       # Honey blonde girl
            "zephyr": None      # Light brown hair girl
        }
        
        # Store generation IDs for character references
        self.character_refs = {}

    def upload_reference_image(self, image_path):
        """Upload a reference image to Leonardo for character consistency."""
        print(f"📤 Uploading reference image: {image_path}")
        
        # First, get presigned upload details
        init_response = requests.post(
            f"{self.base_url}/init-image",
            headers=self.headers,
            json={"extension": "jpg"}
        )
        
        if init_response.status_code != 200:
            print(f"❌ Failed to initialize upload: {init_response.text}")
            return None
            
        upload_data = init_response.json()
        upload_id = upload_data.get("uploadInitImage", {}).get("id")
        upload_url = upload_data.get("uploadInitImage", {}).get("url")
        
        # Upload the image
        with open(image_path, 'rb') as f:
            image_data = f.read()
            
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={"Content-Type": "image/jpeg"}
        )
        
        if upload_response.status_code == 200:
            print(f"✅ Reference image uploaded: {upload_id}")
            return upload_id
        else:
            print(f"❌ Failed to upload image: {upload_response.status_code}")
            return None

    def create_character_base(self, character_name, description):
        """Create a base character image to use as reference."""
        print(f"\n🎨 Creating base image for {character_name}...")
        
        payload = {
            "prompt": description,
            "negative_prompt": "multiple people, crowd, group photo, blurry, bad anatomy",
            "modelId": "6b645e3a-d64f-4341-a6d8-7a3690fbf042",  # Leonardo Anime XL
            "width": 1024,
            "height": 1024,
            "num_images": 4,  # Generate 4 to pick the best
            "guidance_scale": 7,
            "num_inference_steps": 30,
            "scheduler": "LEONARDO",
            "alchemy": True,
            "photoReal": False,
            "presetStyle": "ILLUSTRATION"
        }
        
        response = requests.post(
            f"{self.base_url}/generations",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            generation_id = data.get("sdGenerationJob", {}).get("generationId")
            print(f"✅ Generation started: {generation_id}")
            return generation_id
        else:
            print(f"❌ Generation failed: {response.text}")
            return None

    def wait_and_get_best_image(self, generation_id, character_name):
        """Wait for generation and save the best image with its seed."""
        print(f"⏳ Waiting for {character_name} generation...")
        
        for attempt in range(60):
            time.sleep(5)
            
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
                        # For now, take the first image
                        best_image = images[0]
                        image_url = best_image.get("url")
                        seed = best_image.get("seed")
                        
                        # Save the seed
                        self.character_seeds[character_name] = seed
                        
                        # Download the image
                        output_path = f"{self.output_dir}/{character_name}_base.png"
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(img_response.content)
                            print(f"✅ Base image saved: {output_path}")
                            print(f"🌱 Seed saved: {seed}")
                            return output_path, seed
                        
                elif status == "FAILED":
                    print(f"❌ Generation failed")
                    return None, None
        
        print(f"❌ Generation timed out")
        return None, None

    def create_consistent_generation(self, prompt, negative_prompt, page_num, character_seeds):
        """Create generation with fixed seeds for character consistency."""
        
        # If we have a seed for the main character in this scene, use it
        seed_to_use = None
        for character, seed in character_seeds.items():
            if character in prompt.lower() and seed:
                seed_to_use = seed
                break
        
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "modelId": "6b645e3a-d64f-4341-a6d8-7a3690fbf042",
            "width": 1024,
            "height": 1024,
            "num_images": 1,
            "guidance_scale": 7,
            "num_inference_steps": 30,
            "scheduler": "LEONARDO",
            "alchemy": True,
            "photoReal": False,
            "presetStyle": "ILLUSTRATION"
        }
        
        # Add seed if available
        if seed_to_use:
            payload["seed"] = seed_to_use
            print(f"   🌱 Using fixed seed: {seed_to_use}")
        
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
            print(f"❌ Generation failed for page {page_num}: {response.text}")
            return None

    def create_base_characters(self):
        """Create base images for all main characters."""
        character_descriptions = {
            "corey": "2D cartoon portrait, Phil Foglio style, completely BALD man, no hair whatsoever, shiny bald head, round friendly face, huge warm smile, dark olive-green apron, white shirt, medium build, clean-shaven, no facial hair, cartoon character portrait, simple background",
            "emily": "2D cartoon portrait, Phil Foglio style, woman with short silver pixie cut hair, black rectangular glasses, gray hoodie, green shirt, confident smile, cartoon character portrait, simple background",
            "remi": "2D cartoon portrait, Phil Foglio style, 11-year-old boy with dark curly brown hair, blue shirt with red diamond logo with number 3, energetic expression, cartoon character portrait, simple background",
            "oona": "2D cartoon portrait, Phil Foglio style, 11-year-old girl with long honey blonde hair, blue shirt with red diamond logo with number 3, athletic pose, cartoon character portrait, simple background",
            "zephyr": "2D cartoon portrait, Phil Foglio style, 9-year-old girl with light brown shoulder-length hair, smallest of three children, blue shirt with red diamond logo with number 3, biggest smile, cartoon character portrait, simple background"
        }
        
        print("🎭 Creating base character images for consistency...")
        
        for character, description in character_descriptions.items():
            if not self.character_seeds.get(character):
                gen_id = self.create_character_base(character, description)
                if gen_id:
                    image_path, seed = self.wait_and_get_best_image(gen_id, character)
                    time.sleep(10)  # Rate limiting
        
        # Save seeds for future use
        with open(f"{self.output_dir}/character_seeds.json", 'w') as f:
            json.dump(self.character_seeds, f, indent=2)
        print(f"\n💾 Character seeds saved to {self.output_dir}/character_seeds.json")

    def load_character_seeds(self):
        """Load previously saved character seeds."""
        seeds_file = f"{self.output_dir}/character_seeds.json"
        if os.path.exists(seeds_file):
            with open(seeds_file, 'r') as f:
                self.character_seeds = json.load(f)
            print(f"📥 Loaded character seeds from {seeds_file}")
            return True
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate consistent characters with Leonardo.ai')
    parser.add_argument('--create-base', action='store_true', help='Create base character images first')
    parser.add_argument('--api-key', default="78cc6ab2-acc1-4365-beb2-ac16762ad8b6", help='Leonardo API key')
    
    args = parser.parse_args()
    
    generator = LeonardoConsistentCharacterGenerator(args.api_key)
    
    if args.create_base:
        generator.create_base_characters()
    else:
        # Load existing seeds
        if generator.load_character_seeds():
            print("✅ Character seeds loaded. Ready to generate consistent images.")
        else:
            print("❌ No character seeds found. Run with --create-base first.")

if __name__ == "__main__":
    main()
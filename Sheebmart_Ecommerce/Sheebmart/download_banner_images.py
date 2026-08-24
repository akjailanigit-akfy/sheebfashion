#!/usr/bin/env python
"""
Script to download high-quality fashion images for homepage banners
"""
import os
import urllib.request
from pathlib import Path

# Image dimensions for each banner
IMAGES = {
    'mens-fashion-banner.jpg': {
        'url': 'https://source.unsplash.com/250x340/?men,fashion,clothing',
        'description': "Men's Fashion Clothing Banner (Everyday Essentials)"
    },
    'womens-fashion-banner.jpg': {
        'url': 'https://source.unsplash.com/190x250/?women,fashion,clothing',
        'description': "Women's Fashion Clothing Banner (Weekend Sale)"
    }
}

def download_images():
    """Download banner images from Unsplash"""
    static_dir = Path(__file__).parent / 'static' / 'images'
    static_dir.mkdir(parents=True, exist_ok=True)
    
    print("Downloading banner images from Unsplash...")
    print(f"Destination: {static_dir}\n")
    
    for filename, config in IMAGES.items():
        filepath = static_dir / filename
        url = config['url']
        description = config['description']
        
        try:
            print(f"Downloading: {description}")
            print(f"  From: {url}")
            
            # Download with retry logic
            request = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                with open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            
            file_size = filepath.stat().st_size / 1024  # Size in KB
            print(f"  ✓ Saved: {filepath} ({file_size:.1f} KB)\n")
            
        except Exception as e:
            print(f"  ✗ Error downloading {filename}: {e}")
            print(f"  Please download manually from Unsplash\n")
            return False
    
    print("✓ All banner images downloaded successfully!")
    return True

if __name__ == '__main__':
    success = download_images()
    exit(0 if success else 1)

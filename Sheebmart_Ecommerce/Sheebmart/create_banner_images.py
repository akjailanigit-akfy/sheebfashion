#!/usr/bin/env python
"""
Create professional placeholder banner images using PIL
"""
import os
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

def create_mens_banner():
    """Create men's fashion banner image"""
    # Create base image with sophisticated gradient
    width, height = 500, 680  # 2x scale for quality
    img = Image.new('RGB', (width, height))
    
    # Create sophisticated gradient (dark to light blues/grays - professional menswear)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw gradient from dark navy to lighter gray-blue
    for y in range(height):
        # Create a gradient that's darker at top, lighter at bottom
        r = int(40 + (80 * y / height))  # 40 to 120
        g = int(60 + (90 * y / height))  # 60 to 150
        b = int(100 + (70 * y / height))  # 100 to 170
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add subtle texture overlay
    for i in range(0, width, 80):
        for j in range(0, height, 80):
            draw.rectangle(
                [(i, j), (i+80, j+80)],
                outline=(255, 255, 255, 3),
                width=1
            )
    
    # Apply slight blur for smooth quality
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    
    # Resize to final dimensions
    img = img.resize((250, 340), Image.Resampling.LANCZOS)
    return img

def create_womens_banner():
    """Create women's fashion banner image"""
    # Create base image with warm gradient
    width, height = 380, 500  # 2x scale for quality
    img = Image.new('RGB', (width, height))
    
    # Create warm gradient (rose/warm tones - sophisticated feminine)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw gradient from warm brown to rose pink
    for y in range(height):
        # Create a warm, luxurious gradient
        r = int(180 + (60 * y / height))  # 180 to 240
        g = int(120 + (40 * y / height))  # 120 to 160
        b = int(140 + (50 * y / height))  # 140 to 190
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add elegant texture
    for i in range(0, width, 76):
        for j in range(0, height, 76):
            draw.ellipse(
                [(i, j), (i+40, j+40)],
                outline=(255, 255, 255, 2),
                width=1
            )
    
    # Apply slight blur for smooth quality
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    
    # Resize to final dimensions
    img = img.resize((190, 250), Image.Resampling.LANCZOS)
    return img

def save_images():
    """Save banner images"""
    static_dir = Path(__file__).parent / 'static' / 'images'
    static_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating professional fashion banner images...")
    print(f"Destination: {static_dir}\n")
    
    try:
        # Create men's fashion banner
        print("Creating: Men's Fashion Clothing Banner (Everyday Essentials)")
        print("  Size: 250x340px, Professional Blue Gradient")
        mens_img = create_mens_banner()
        mens_path = static_dir / 'mens-fashion-banner.jpg'
        mens_img.save(mens_path, 'JPEG', quality=95)
        print(f"  ✓ Saved: {mens_path}\n")
        
        # Create women's fashion banner
        print("Creating: Women's Fashion Clothing Banner (Weekend Sale)")
        print("  Size: 190x250px, Professional Rose Gradient")
        womens_img = create_womens_banner()
        womens_path = static_dir / 'womens-fashion-banner.jpg'
        womens_img.save(womens_path, 'JPEG', quality=95)
        print(f"  ✓ Saved: {womens_path}\n")
        
        print("✓ All banner images created successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error creating images: {e}")
        return False

if __name__ == '__main__':
    success = save_images()
    exit(0 if success else 1)

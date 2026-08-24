#!/usr/bin/env python
"""
Create more visible banner images with clear patterns
"""
from PIL import Image, ImageDraw
from pathlib import Path

def create_mens_banner_v2():
    """Create men's fashion banner with pattern and overlay"""
    width, height = 250, 340
    img = Image.new('RGB', (width, height), color=(45, 70, 100))  # Dark blue
    
    draw = ImageDraw.Draw(img)
    
    # Create diagonal stripe pattern
    for i in range(-height, width, 20):
        draw.line([(i, 0), (i+height, height)], fill=(60, 90, 130), width=10)
    
    # Add some text to make it obviously a banner
    try:
        draw.text((width//2-30, height//2-20), "MEN", fill=(200, 180, 150))
        draw.text((width//2-50, height//2), "FASHION", fill=(180, 160, 130))
    except:
        pass
    
    return img

def create_womens_banner_v2():
    """Create women's fashion banner with pattern and overlay"""
    width, height = 190, 250
    img = Image.new('RGB', (width, height), color=(200, 120, 150))  # Rose/pink
    
    draw = ImageDraw.Draw(img)
    
    # Create geometric pattern
    for i in range(0, width, 30):
        for j in range(0, height, 30):
            draw.ellipse([(i, j), (i+20, j+20)], fill=(180, 100, 130))
    
    # Add some text
    try:
        draw.text((width//2-30, height//2-20), "WOMEN", fill=(255, 240, 220))
        draw.text((width//2-40, height//2), "SALE", fill=(255, 240, 220))
    except:
        pass
    
    return img

def save_images():
    """Save banner images"""
    static_dir = Path(__file__).parent / 'static' / 'images'
    static_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating updated fashion banner images...\n")
    
    # Create men's fashion banner
    print("Creating: Men's Fashion Banner (with visible pattern)")
    mens_img = create_mens_banner_v2()
    mens_path = static_dir / 'mens-fashion-banner.jpg'
    mens_img.save(mens_path, 'JPEG', quality=95)
    print(f"  ✓ Saved: {mens_path}\n")
    
    # Create women's fashion banner
    print("Creating: Women's Fashion Banner (with visible pattern)")
    womens_img = create_womens_banner_v2()
    womens_path = static_dir / 'womens-fashion-banner.jpg'
    womens_img.save(womens_path, 'JPEG', quality=95)
    print(f"  ✓ Saved: {womens_path}\n")
    
    print("✓ All banner images updated!")

if __name__ == '__main__':
    save_images()

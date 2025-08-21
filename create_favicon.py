#!/usr/bin/env python3
"""
Script to create favicon files for the website
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont
    import os

def create_favicon():
    """Create a simple favicon with a chart/trading symbol"""
    
    # Create a 32x32 base image
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple chart-like symbol (green upward trend)
    # Background circle
    draw.ellipse([2, 2, size-2, size-2], fill=(102, 126, 234, 255))  # Blue from your theme
    
    # Draw a simple chart line (white)
    points = [(8, 24), (12, 20), (16, 16), (20, 12), (24, 8)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(255, 255, 255, 255), width=2)
    
    # Draw small dots at data points
    for point in points:
        draw.ellipse([point[0]-1, point[1]-1, point[0]+1, point[1]+1], fill=(255, 255, 255, 255))
    
    # Save different sizes
    favicon_dir = "netlify-deploy"
    
    # Create directory if it doesn't exist
    os.makedirs(favicon_dir, exist_ok=True)
    
    # Save ICO file (32x32)
    img.save(f"{favicon_dir}/favicon.ico", format='ICO')
    
    # Save PNG files in different sizes
    sizes = [16, 32, 180]
    for s in sizes:
        resized_img = img.resize((s, s), Image.Resampling.LANCZOS)
        if s == 16:
            resized_img.save(f"{favicon_dir}/favicon-16x16.png", format='PNG')
        elif s == 32:
            resized_img.save(f"{favicon_dir}/favicon-32x32.png", format='PNG')
        elif s == 180:
            resized_img.save(f"{favicon_dir}/apple-touch-icon.png", format='PNG')
    
    print("✅ Favicon files created successfully!")
    print(f"📁 Files saved in: {favicon_dir}/")
    print("   - favicon.ico")
    print("   - favicon-16x16.png")
    print("   - favicon-32x32.png")
    print("   - apple-touch-icon.png")

if __name__ == "__main__":
    create_favicon()
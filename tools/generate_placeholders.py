"""Generate example placeholder images for the Kivy app.
Creates `icon.png` (512x512) and `presplash.png` (2732x2732) in the repository root.
If Pillow is not installed this script will attempt to pip install it automatically.

Run:
    python tools/generate_placeholders.py
"""
from __future__ import annotations
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    print("Pillow not found; attempting to install it via pip...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"]) 
        from PIL import Image, ImageDraw, ImageFont
    except Exception as e:
        print("Failed to install Pillow. Please install it manually and re-run this script.")
        raise

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ICON_PATH = os.path.join(ROOT, 'icon.png')
PRESPLASH_PATH = os.path.join(ROOT, 'presplash.png')

def make_icon(path: str, size=(512,512)):
    img = Image.new('RGBA', size, (30,144,255,255))
    draw = ImageDraw.Draw(img)
    # draw a light circle
    cx, cy = size[0]//2, size[1]//2
    r = int(min(size)*0.35)
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(255,255,255,230))
    # small inner circle
    draw.ellipse((cx-r//2, cy-r//2, cx+r//2, cy+r//2), fill=(30,144,255,255))
    # label text
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        font = ImageFont.load_default()
    text = "AllergyDB"
    # compute text width/height in a Pillow-compatible way
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = font.getsize(text)
    draw.text((cx - tw//2, cy + r + 10), text, fill=(255,255,255,255), font=font)
    img.save(path)
    print(f"Wrote {path}")


def make_presplash(path: str, size=(2732,2732)):
    img = Image.new('RGB', size, (250,250,250))
    draw = ImageDraw.Draw(img)
    w, h = size
    # draw a large rounded rectangle band
    band_h = int(h * 0.22)
    draw.rectangle((0, (h-band_h)//2, w, (h+band_h)//2), fill=(30,144,255))
    # title text
    try:
        font = ImageFont.truetype("arial.ttf", 220)
    except Exception:
        font = ImageFont.load_default()
    text = "Food Allergy Database"
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = font.getsize(text)
    draw.text(((w-tw)//2, (h-th)//2), text, fill=(255,255,255), font=font)
    # small footer
    try:
        font2 = ImageFont.truetype("arial.ttf", 60)
    except Exception:
        font2 = ImageFont.load_default()
    footer = "Example placeholder presplash"
    try:
        bbox2 = draw.textbbox((0, 0), footer, font=font2)
        fw, fh = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    except Exception:
        fw, fh = font2.getsize(footer)
    draw.text(((w-fw)//2, (h+band_h)//2 + 30), footer, fill=(120,120,120), font=font2)
    img.save(path)
    print(f"Wrote {path}")


if __name__ == '__main__':
    make_icon(ICON_PATH)
    make_presplash(PRESPLASH_PATH)
    print("Placeholder images generated. Replace these with your production assets as needed.")

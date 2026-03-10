#!/usr/bin/env python3
"""Generate images for Run Our House marketing site via OpenAI DALL-E 3.

Usage:
    OPENAI_API_KEY=your-key python3 scripts/generate-images.py

"No AI glow" philosophy — images should feel like real snapshots of family life,
not polished stock photos. Target audience: busy moms, 30-45, Reno/Northern Nevada.
"""

import os
import sys
import json
import subprocess
import urllib.request
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "public" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OG image: social sharing preview (1200x630). Should convey
# "calm household management" — a phone with WhatsApp on a kitchen counter
OG_PROMPT = (
    "Color photograph of a phone on a kitchen counter showing a WhatsApp "
    "conversation. Next to the phone is a coffee mug, a grocery list on a "
    "notepad, and a small succulent plant. Morning light coming through the "
    "kitchen window. The counter is clean but lived-in — a few crumbs, a "
    "kid's drawing held by a magnet on the fridge in the background. "
    "Warm, homey, not staged. Looks like a mom snapped a quick photo "
    "of her morning routine. Color photo."
)

# Hero image: homepage hero background. Conveys "the mental load is real"
# then the product lifts it. Mom at kitchen table, relaxed, phone in hand.
HERO_PROMPT = (
    "Color photograph of a woman in her mid-30s sitting at a kitchen table "
    "looking relaxed, smiling slightly while looking at her phone. On the "
    "table is a cup of coffee, a planner that's closed, and a kid's water "
    "bottle. The kitchen behind her is tidy but real — magnets on the fridge, "
    "a fruit bowl, mail on the counter. Soft morning light. She looks like "
    "she just got good news. Shot from across the table. Casual, not posed. "
    "Color photo."
)

# How it works: phone with WhatsApp chat visible, close-up.
# Shows the actual product interface concept.
PHONE_CHAT_PROMPT = (
    "Close-up color photograph of hands holding a smartphone showing a chat "
    "conversation on the screen. The person is sitting on a couch with a "
    "blanket over their lap. A toddler's toy is visible on the couch cushion "
    "next to them. Living room setting, afternoon light from a window. "
    "Cozy and relaxed. The screen shows green and white chat bubbles. "
    "Shot from slightly above. Casual snapshot feel. Color photo."
)

# Pricing page: family calendar on a fridge, representing the chaos that
# the product replaces.
FAMILY_CALENDAR_PROMPT = (
    "Color photograph of a paper family calendar pinned to a refrigerator door "
    "with magnets. The calendar has lots of handwritten entries in different "
    "colored pens — soccer practice, dentist, pickup, dinner at grandma's. "
    "Some entries are crossed out, some have arrows. A few kids' drawings and "
    "school photos are also stuck to the fridge. Close-up shot, slightly "
    "angled. Feels busy and overwhelming but loving. Color photo."
)

# About page: Reno cityscape / local feel. Establishes the "local business"
# trust factor.
RENO_LOCAL_PROMPT = (
    "Color photograph looking down a quiet residential street in Reno, Nevada "
    "with the Sierra Nevada mountains visible in the background. A few houses "
    "with front yards, a sidewalk, one parked car. Clear blue sky, golden "
    "afternoon light. It feels like a nice neighborhood where families live. "
    "Not a postcard — more like a photo someone took while walking their dog. "
    "Color photo."
)

IMAGES = {
    "og-image": {
        "prompt": OG_PROMPT,
        "size": "1792x1024",
    },
    "hero": {
        "prompt": HERO_PROMPT,
        "size": "1792x1024",
    },
    "phone-chat": {
        "prompt": PHONE_CHAT_PROMPT,
        "size": "1024x1024",
    },
    "family-calendar": {
        "prompt": FAMILY_CALENDAR_PROMPT,
        "size": "1024x1024",
    },
    "reno-local": {
        "prompt": RENO_LOCAL_PROMPT,
        "size": "1792x1024",
    },
}


def generate_dalle(api_key, name, image):
    """Generate via OpenAI DALL-E 3 API."""
    print(f"  Generating {name} ({image['size']})...")
    data = json.dumps({
        "model": "dall-e-3",
        "prompt": image["prompt"],
        "n": 1,
        "size": image["size"],
        "quality": "standard",
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    url = result["data"][0]["url"]

    # Download as PNG first
    png_out = OUTPUT_DIR / f"{name}.png"
    urllib.request.urlretrieve(url, str(png_out))
    print(f"  Saved PNG: {png_out.name}")

    # Convert to JPEG with sips (macOS)
    jpg_out = OUTPUT_DIR / f"{name}.jpg"
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
         str(png_out), "--out", str(jpg_out)],
        capture_output=True,
    )
    png_out.unlink()
    print(f"  Converted: {jpg_out.name}")
    return jpg_out


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set.")
        print("Usage: OPENAI_API_KEY=your-key python3 scripts/generate-images.py")
        sys.exit(1)

    print(f"Output: {OUTPUT_DIR}/\n")

    for name, image in IMAGES.items():
        print(f"--- {name} ---")
        try:
            generate_dalle(api_key, name, image)
        except Exception as e:
            print(f"  ERROR: {e}")
        print()

    print("Done. Check public/images/ for results.")
    print("\nImage placement:")
    print("  og-image.jpg      → OG meta tags (all pages)")
    print("  hero.jpg           → Homepage hero section background")
    print("  phone-chat.jpg     → How It Works page, near conversation examples")
    print("  family-calendar.jpg → Pricing page, near comparison section")
    print("  reno-local.jpg     → About page, near origin story")


if __name__ == "__main__":
    main()

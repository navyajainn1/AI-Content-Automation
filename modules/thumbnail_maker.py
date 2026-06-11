from PIL import Image, ImageDraw, ImageFont
import os, textwrap
import re

def make_thumbnail(title: str) -> str:
    os.makedirs("output/thumbnails", exist_ok=True)
    safe_title = re.sub(r'[^\w\s-]', '', title).replace(" ", "_")[:50]
    path = f"output/thumbnails/{safe_title}.png"

    img = Image.new("RGB", (1280, 720), color=(15, 15, 40))
    draw = ImageDraw.Draw(img)

    # Gradient-style accent bar
    for x in range(1280):
        r = int(80 + (x / 1280) * 100)
        draw.line([(x, 0), (x, 10)], fill=(r, 50, 200))

    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("assets/fonts/Arial_Bold.ttf", 80)
        small_font = ImageFont.truetype("assets/fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = font

    # Wrap and draw title
    wrapped = textwrap.fill(title, width=20)
    draw.multiline_text((80, 200), wrapped, fill="white", font=font, spacing=20)
    draw.text((80, 620), "AI Media Platform", fill=(150, 150, 255), font=small_font)

    img.save(path)
    print(f"[✓] Thumbnail saved: {path}")
    return path
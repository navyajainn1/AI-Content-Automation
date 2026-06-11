from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip
from config.settings import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS
import os
import re
import textwrap
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def safe_filename(title):
    name = re.sub(r'[^\w\s-]', '', title)
    name = name.replace(" ", "_")[:50]
    return name

def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def get_pexels_image(keyword):
    """Fetch a relevant image from Pexels based on keyword."""
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": keyword, "per_page": 1, "orientation": "portrait"}
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=10)
        data = response.json()
        if data.get("photos"):
            img_url = data["photos"][0]["src"]["large"]
            img_data = requests.get(img_url, timeout=10).content
            from io import BytesIO
            img = Image.open(BytesIO(img_data)).convert("RGB")
            # Crop to vertical 9:16
            img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.LANCZOS)
            return img
    except Exception as e:
        print(f"      [Pexels] Could not fetch image for '{keyword}': {e}")
    return None

def make_frame(text, title, width, height, show_title=False, bg_image=None):
    """Create a frame with Pexels background + dark overlay + text."""
    if bg_image:
        img = bg_image.copy()
    else:
        img = Image.new("RGB", (width, height), color=(10, 10, 30))

    # Dark overlay so text is readable
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 160))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Top gradient bar
    for x in range(width):
        r = int(60 + (x / width) * 80)
        draw.line([(x, 0), (x, 10)], fill=(r, 40, 180))

    if show_title:
        font = get_font(52)
        wrapped = textwrap.fill(title, width=25)
        draw.multiline_text(
            (width // 2, 120),
            wrapped,
            font=font,
            fill=(255, 220, 50),
            anchor="mm",
            align="center",
            spacing=10
        )

    # Main text — centered vertically
    font = get_font(46)
    wrapped = textwrap.fill(text, width=28)
    draw.multiline_text(
        (width // 2, height // 2),
        wrapped,
        font=font,
        fill=(255, 255, 255),
        anchor="mm",
        align="center",
        spacing=16
    )

    # Bottom watermark
    small = get_font(26)
    draw.text((30, height - 50), "AI Media Platform", font=small, fill=(180, 180, 255))

    return img

def extract_keyword(text):
    """Extract a short search keyword from a chunk of text."""
    words = text.split()
    # Pick first 3 meaningful words as keyword
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "are", "was", "were", "will", "can", "this", "that", "it", "we", "you", "i"}
    keywords = [w for w in words if w.lower() not in stopwords and len(w) > 3]
    return " ".join(keywords[:3]) if keywords else "technology"

def build_video(audio_path, script, title):
    os.makedirs("output/videos", exist_ok=True)
    os.makedirs("output/frames", exist_ok=True)

    safe = safe_filename(title)
    output_path = "output/videos/" + safe + ".mp4"

    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()

    words = script.split()
    chunk_size = 30
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    time_per_chunk = duration / len(chunks)

    print(f"      {len(chunks)} slides, {time_per_chunk:.1f}s each")

    # Fetch one background image per slide
    img_paths = []
    for i, chunk in enumerate(chunks):
        keyword = extract_keyword(chunk)
        print(f"      Fetching image for slide {i+1}/{len(chunks)}: '{keyword}'")
        bg = get_pexels_image(keyword)
        frame = make_frame(chunk, title, VIDEO_WIDTH, VIDEO_HEIGHT, show_title=(i == 0), bg_image=bg)
        p = f"output/frames/{safe}_{i:03d}.png"
        frame.save(p)
        img_paths.append(p)

    list_path = "output/frames/slides.txt"
    with open(list_path, "w") as fp:
        for p in img_paths:
            fp.write(f"file '{os.path.abspath(p)}'\n")
            fp.write(f"duration {time_per_chunk:.4f}\n")
        fp.write(f"file '{os.path.abspath(img_paths[-1])}'\n")

    silent_video = f"output/videos/{safe}_silent.mp4"

    print("      Building silent video...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-r", str(VIDEO_FPS),
        silent_video
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("      Merging audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", silent_video,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for p in img_paths:
        os.remove(p)
    os.remove(silent_video)
    os.remove(list_path)

    print("[OK] Video saved: " + output_path)
    return output_path
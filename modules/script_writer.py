from groq import Groq
from config.settings import GROQ_API_KEY
import os
import re

client = Groq(api_key=GROQ_API_KEY)

def write_script(title: str, topic: str) -> str:
    prompt = (
    "Write a YouTube Shorts script for:\n"
    "Title: " + title + "\n"
    "Topic: " + topic + "\n\n"
    "STRICT RULES:\n"
    "- Maximum 55 seconds when read aloud\n"
    "- That means MAXIMUM 130 words total\n"
    "- First sentence must be a hook that grabs attention\n"
    "- Fast, punchy, short sentences only\n"
    "- End with 'Follow for more AI content'\n"
    "- No stage directions, plain speech only\n"
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    script = response.choices[0].message.content

    # Save to file
    os.makedirs("output/scripts", exist_ok=True)
    safe_title = re.sub(r'[^\w\s-]', '', title)   # remove special chars
    safe_title = safe_title.replace(" ", "_")[:50]
    path = f"output/scripts/{safe_title}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(script)

    # Trim to 130 words max
    words = script.split()
    if len(words) > 130:
        script = " ".join(words[:130])

    print(f"[✓] Script saved: {path}")
    return script
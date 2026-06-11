import edge_tts
import asyncio
import os
import re

# Available voices: en-US-GuyNeural, en-US-JennyNeural, en-GB-RyanNeural
VOICE = "en-US-GuyNeural"

async def _generate(script: str, output_path: str):
    communicate = edge_tts.Communicate(script, VOICE)
    await communicate.save(output_path)

def generate_voice(script: str, title: str) -> str:
    os.makedirs("output/audio", exist_ok=True)
    safe_title = re.sub(r'[^\w\s-]', '', title).replace(" ", "_")[:50]
    path = f"output/audio/{safe_title}.mp3"
    asyncio.run(_generate(script, path))
    print(f"[✓] Audio saved: {path}")
    return path
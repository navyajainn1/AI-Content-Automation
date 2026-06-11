from groq import Groq
from config.settings import GROQ_API_KEY, NICHE
import re

client = Groq(api_key=GROQ_API_KEY)

def clean(text):
    text = re.sub(r'[\*\_\"\'\`]', '', text)
    text = re.sub(r'^(TITLE|TOPIC)\s*:\s*', '', text, flags=re.IGNORECASE)
    return text.strip()

def generate_idea():
    prompt = (
        "You are a YouTube content strategist for the niche: " + NICHE + ".\n"
        "Generate 1 highly engaging YouTube video idea.\n"
        "Return ONLY these two lines, no markdown, no asterisks, no quotes:\n"
        "TITLE: your title here\n"
        "TOPIC: one sentence description here\n"
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    lines = [l.strip() for l in raw.split("\n") if l.strip()]

    if len(lines) >= 2:
        title = clean(lines[0])
        topic = clean(lines[1])
    elif len(lines) == 1:
        title = clean(lines[0])
        topic = "Exploring AI trends"
    else:
        title = "AI Video"
        topic = "Exploring AI trends"

    return title, topic
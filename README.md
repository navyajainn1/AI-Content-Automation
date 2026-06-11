# AI Media Pipeline — Automated YouTube Shorts Generator

A fully automated AI-powered content pipeline that generates YouTube Shorts from scratch — idea, script, voice, video, and upload — with zero human input and zero cost.

---

## What It Does

```
Groq AI → Script → Edge-TTS Voice → Pexels Images → MP4 Video → YouTube Upload
```

| Step | Tool | Cost |
|------|------|------|
| Idea + Script | Groq API (Llama 3) | Free |
| Text-to-Speech | Edge-TTS (Microsoft) | Free |
| Background Images | Pexels API | Free |
| Video Building | FFmpeg + MoviePy + Pillow | Free |
| YouTube Upload | YouTube Data API v3 | Free |

---

##  Project Structure

```
ai_media_pipeline/
│
├── config/
│   └── settings.py              # Resolution, FPS, niche config
│
├── modules/
│   ├── idea_generator.py        # Groq → trending video idea
│   ├── script_writer.py         # Groq → Shorts script (max 130 words)
│   ├── voice_generator.py       # Edge-TTS → MP3 audio
│   ├── video_builder.py         # Pexels + Pillow + FFmpeg → MP4
│   ├── thumbnail_maker.py       # Pillow → thumbnail PNG
│   └── uploader.py              # YouTube Data API v3 → upload
│
├── assets/
│   ├── backgrounds/             # Fallback background images
│   └── fonts/                   # Optional custom fonts
│
├── output/
│   ├── scripts/                 # Generated .txt scripts
│   ├── audio/                   # Generated .mp3 files
│   ├── videos/                  # Final .mp4 videos
│   └── thumbnails/              # Generated .png thumbnails
│
├── pipeline.py                  # Master runner — runs full pipeline
├── requirements.txt
├── .env                         # API keys (never commit this)
├── .gitignore
└── README.md
```

---

## Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-media-pipeline.git
cd ai-media-pipeline
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to system PATH.

Verify:
```bash
ffmpeg -version
```

### 5. Get free API keys

| API | Link | Notes |
|-----|------|-------|
| Groq | [console.groq.com](https://console.groq.com) | Free, no card needed |
| Pexels | [pexels.com/api](https://www.pexels.com/api/) | Free, instant approval |
| YouTube Data API | [console.cloud.google.com](https://console.cloud.google.com) | Free 10k units/day |

### 6. Configure `.env`

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
```

### 7. Set up YouTube API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Go to **Credentials → Create OAuth 2.0 Client ID** (Desktop App)
5. Download `client_secret.json` and place it in the project root
6. Go to **OAuth consent screen → Test users** and add your Gmail
7. Under **Authorized redirect URIs** add: `http://localhost:8080/`

### 8. Create a YouTube channel

Make sure your Google account has a YouTube channel created at [youtube.com](https://youtube.com) before running.

---

## Run the Pipeline

```bash
python pipeline.py
```

First run will open a browser for YouTube OAuth. After approving, `token.pickle` is saved and future runs are fully automatic.

---

## Output Example

```
========== AI MEDIA PIPELINE ==========
Started: 2026-06-10 18:08

[1/6] Generating video idea...
      Title : The Unseen Revolution: Can AI Actually Dream?
      Topic : Exploring artificial neural dreams and AI consciousness

[2/6] Writing script with Groq...
      Script length: 128 words

[3/6] Generating AI voice (Edge-TTS)...
      Audio saved: output/audio/The_Unseen_Revolution.mp3

[4/6] Building video with MoviePy...
      6 slides, 8.2s each
      Building silent video...
      Merging audio...
      Video saved: output/videos/The_Unseen_Revolution.mp4

[5/6] Creating thumbnail...
      Thumbnail saved: output/thumbnails/The_Unseen_Revolution.png

[6/6] Uploading to YouTube...
      Uploaded! https://youtu.be/xxxxxxxxxx

========== DONE ==========
```

---

## Schedule Daily Runs

**Windows Task Scheduler:**
- Action: `python C:\path\to\ai_media_pipeline\pipeline.py`
- Trigger: Daily at your preferred time

**Linux/Mac cron** (runs daily at 9 AM):
```bash
# you can schedule it as per your project type , mine was just a task so I skipped.

0 9 * * * cd /path/to/ai_media_pipeline && python pipeline.py
```

---

## Known Limitations

| Limitation | Reason |
|------------|--------|
| Custom thumbnails don't upload | YouTube requires 500+ subscribers for API thumbnail upload |
| Max ~6 uploads/day | YouTube Data API free quota is 10,000 units/day |
| First run requires browser | OAuth sign-in needed once; saved automatically after |

---

## Requirements

```
groq
edge-tts
moviepy
pillow
google-api-python-client
google-auth-oauthlib
python-dotenv
requests
```

---

## Built With

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Edge-TTS](https://github.com/rany2/edge-tts) — Microsoft neural text-to-speech
- [Pexels API](https://www.pexels.com/api/) — Free stock photos
- [MoviePy](https://zulko.github.io/moviepy/) — Video processing
- [FFmpeg](https://ffmpeg.org) — Video encoding
- [YouTube Data API v3](https://developers.google.com/youtube/v3) — Auto upload

---

## License

MIT License — free to use and modify.
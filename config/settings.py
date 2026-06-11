import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YOUTUBE_CLIENT_SECRET_FILE = "client_secret.json"  # from Google Cloud Console
PEXEL_API_KEY = os.getenv("PEXEL_API_KEY")

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 24
FONT_SIZE = 60

# Channel niche — change this to your topic
NICHE = "AI and Technology"
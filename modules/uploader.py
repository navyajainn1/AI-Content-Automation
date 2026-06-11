from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_youtube_client():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=True)
        with open("token.pickle", "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(video_path: str, thumbnail_path: str, title: str, description: str, tags: list):
    youtube = get_youtube_client()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print("[→] Uploading to YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"[✓] Uploaded! https://youtu.be/{video_id}")

    # Set thumbnail
    print("[!] Thumbnail skipped (requires 500+ subscribers to set via API).")

    return video_id
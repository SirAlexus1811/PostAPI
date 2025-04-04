import requests
import time
import threading
from flask import Flask, request
import webbrowser

# TikTok API Credentials (ersetzen mit deinen Werten)
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:3000/auth/callback"

# Flask Webserver zur Code-Abfrage
app = Flask(__name__)
auth_code = None

@app.route("/auth/callback")
def auth_callback():
    global auth_code
    auth_code = request.args.get("code")
    return "Erfolgreich authentifiziert! Du kannst das Fenster jetzt schließen."

# Starte den Webserver in einem separaten Thread
server_thread = threading.Thread(target=app.run, kwargs={"port": 3000})
server_thread.start()

# Öffne den TikTok-Login-Link im Browser
auth_url = f"https://www.tiktok.com/auth/authorize?client_key={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=user.info.basic,video.upload,video.publish"
print("Bitte logge dich in TikTok ein, um Zugriff zu gewähren.")
webbrowser.open(auth_url)

# Warte auf den Code
while auth_code is None:
    time.sleep(1)

# Tausche Code gegen Access Token
token_url = "https://open.tiktokapis.com/v2/oauth/token/"
token_data = {
    "client_key": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": auth_code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}
token_response = requests.post(token_url, data=token_data).json()
ACCESS_TOKEN = token_response.get("access_token")

if not ACCESS_TOKEN:
    print("Fehler: Konnte kein Access Token erhalten.")
    exit()

print("Erfolgreich authentifiziert! Access Token erhalten.")

# Video hochladen
video_path = "dein_video.mp4"  # Pfad zum Video
upload_url = "https://open.tiktokapis.com/v2/video/upload/"

with open(video_path, "rb") as video_file:
    upload_response = requests.post(
        upload_url,
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        files={"video": video_file}
    ).json()

video_id = upload_response.get("data", {}).get("video_id")
if not video_id:
    print("Fehler beim Hochladen des Videos.")
    exit()

print(f"Video erfolgreich hochgeladen! Video ID: {video_id}")

# Optional: Video direkt veröffentlichen
publish_url = "https://open.tiktokapis.com/v2/video/publish/"
publish_data = {
    "video_id": video_id,
    "description": "Automatisch hochgeladen mit der TikTok API!"
}

publish_response = requests.post(
    publish_url,
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    json=publish_data
).json()

if publish_response.get("data", {}).get("status") == "success":
    print("Video wurde erfolgreich gepostet! 🎉")
else:
    print("Fehler beim Posten des Videos.")

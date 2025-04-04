import time
import threading
from flask import Flask, request
import webbrowser

# Dummy-Credentials
CLIENT_ID = "DEINE_CLIENT_ID"
REDIRECT_URI = "http://localhost:3000/auth/callback"

# Flask Webserver
app = Flask(__name__)
auth_code = None

@app.route("/auth/callback")
def auth_callback():
    global auth_code
    auth_code = request.args.get("code", "dummy_auth_code")
    return "Erfolgreich authentifiziert! (Demo-Modus)"

# Starte Webserver
server_thread = threading.Thread(target=app.run, kwargs={"port": 3000})
server_thread.start()

# Öffne TikTok-Login-Seite
auth_url = f"https://www.tiktok.com/auth/authorize?client_key={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
print("Bitte logge dich in TikTok ein (Demo-Modus).")
webbrowser.open(auth_url)

time.sleep(5)

# Warte auf den Code (Simulation)
time.sleep(3)
auth_code = "dummy_auth_code"

print(f"Authentifizierung erfolgreich! Code erhalten: {auth_code}")

# Simuliere den Upload
time.sleep(2)
video_id = "dummy_video_12345"
print(f"Video erfolgreich hochgeladen! Video ID: {video_id}")

# Simuliere das Posten des Videos
time.sleep(2)
print("Video wurde erfolgreich gepostet! 🎉 (Demo-Modus)")

#This will be the file for Instagram
import requests

ACCESS_TOKEN = "DEIN_LONG_LIVED_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "DEINE_INSTAGRAM_ACCOUNT_ID"
IMAGE_URL = "https://example.com/dein_bild.jpg"
CAPTION = "Mein erster automatischer Instagram-Post! 🚀"

# Schritt 1: Medien-Upload erstellen
upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
payload = {
    "image_url": IMAGE_URL,
    "caption": CAPTION,
    "access_token": ACCESS_TOKEN
}

response = requests.post(upload_url, data=payload)
response_data = response.json()
print(response_data)

if "id" in response_data:
    media_id = response_data["id"]

    # Schritt 2: Medien-Post veröffentlichen
    publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN
    }

    publish_response = requests.post(publish_url, data=publish_payload)
    print(publish_response.json())
else:
    print("Fehler beim Hochladen des Bildes.")

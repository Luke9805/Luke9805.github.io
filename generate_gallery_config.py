#!/usr/bin/env python3
"""
Script to generate gallery-config.json from Google Drive folders.
Requires: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

First time setup:
1. Create a Google Cloud project: https://console.cloud.google.com/
2. Enable Google Drive API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download the credentials as JSON and save as 'credentials.json'
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core.exceptions import GoogleAPICallError
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
CONFIG_FILE = 'gallery_folders.json'


def authenticate():
    """Authenticate with Google Drive API."""
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, create new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"❌ {CREDENTIALS_FILE} not found!\n"
                    "Visit https://console.cloud.google.com/ to create credentials"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def load_folder_config():
    """Load folder configuration from gallery_folders.json."""
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️  {CONFIG_FILE} not found!")
        print("Creating template file. Please fill in the folder IDs and run again.\n")

        template = {
            "folders": {
                "Compleanni": {
                    "id": "YOUR_FOLDER_ID_HERE",
                    "description": "Birthday photos"
                },
                "Ritratti": {
                    "id": "YOUR_FOLDER_ID_HERE",
                    "description": "Portrait photos"
                },
                "Varie": {
                    "id": "YOUR_FOLDER_ID_HERE",
                    "description": "Various photos"
                },
                "Esibizioni": {
                    "id": "YOUR_FOLDER_ID_HERE",
                    "description": "Exhibition photos"
                }
            }
        }

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"✅ Template created: {CONFIG_FILE}")
        print("📝 Please edit this file with your Google Drive folder IDs")
        print("   Find folder IDs in the URL: https://drive.google.com/drive/folders/FOLDER_ID")
        return None

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_images_from_folder(service, folder_id, category_name):
    """Get all images from a Google Drive folder."""
    print(f"📂 Scanning folder '{category_name}'...", end=" ", flush=True)

    images = []
    try:
        # Query for image files in the folder
        query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=1000
        ).execute()

        files = results.get('files', [])

        if not files:
            print("⚠️  No images found")
            return images

        # Sort by name
        files.sort(key=lambda x: x['name'])

        for file in files:
            images.append({
                "fileId": file['id'],
                "name": file['name']
            })

        print(f"✅ Found {len(images)} images")
        return images

    except GoogleAPICallError as e:
        print(f"❌ Error: {e}")
        return []


def main():
    """Main function to generate gallery config."""
    print("🚀 Google Drive Gallery Config Generator\n")

    # Load folder configuration
    config = load_folder_config()
    if config is None:
        return

    # Authenticate
    print("\n🔐 Authenticating with Google Drive...")
    try:
        service = authenticate()
        print("✅ Authentication successful\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return

    # Build gallery config
    gallery_config = {}

    for category, folder_info in config['folders'].items():
        folder_id = folder_info['id']

        if folder_id == "YOUR_FOLDER_ID_HERE":
            print(f"⏭️  Skipping '{category}' (folder ID not configured)")
            continue

        images = get_images_from_folder(service, folder_id, category)
        if images:
            gallery_config[category] = images

    # Save gallery config
    output_file = 'gallery-config.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gallery_config, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Gallery config saved to: {output_file}")
    print(f"📊 Categories: {', '.join(gallery_config.keys())}")
    total_images = sum(len(v) for v in gallery_config.values())
    print(f"📸 Total images: {total_images}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Script to generate gallery-config.json from Google Drive folders.
Requires: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client pillow requests
"""

import json
import os
import requests
from io import BytesIO
from PIL import Image
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'service-account.json'
CONFIG_FILE = 'gallery_folders.json'
THUMBNAILS_DIR = 'thumbnails'

os.makedirs(THUMBNAILS_DIR, exist_ok=True)

def generate_thumbnail(file_id, thumbnail_link, max_size=(800, 800)):
    """Scarica il thumbnail da Google Drive, lo ridimensiona e salva in WebP."""
    thumbnail_path = os.path.join(THUMBNAILS_DIR, f"{file_id}.webp")
    
    if os.path.exists(thumbnail_path):
        return thumbnail_path
        
    try:
        if '=' in thumbnail_link:
            hi_res_link = thumbnail_link.split('=')[0] + '=s800'
        else:
            hi_res_link = thumbnail_link + '=s800'
            
        response = requests.get(hi_res_link)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, "WEBP", quality=80)
            return thumbnail_path
        else:
            print(f"Failed to download thumbnail for {file_id}, status {response.status_code}")
    except Exception as e:
        print(f"Error generating thumbnail for {file_id}: {e}")
        
    return None


def authenticate():
    service_account_json = None
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            service_account_json = json.load(f)
    else:
        env_credentials = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
        if env_credentials:
            try:
                service_account_json = json.loads(env_credentials)
            except json.JSONDecodeError as e:
                print(f"Failed to parse GOOGLE_SERVICE_ACCOUNT environment variable: {e}")
                raise
    
    if not service_account_json:
        raise FileNotFoundError(
            f"Service account credentials not found!\n"
            f"Place '{SERVICE_ACCOUNT_FILE}' in the current directory or set GOOGLE_SERVICE_ACCOUNT environment variable"
        )
    
    creds = service_account.Credentials.from_service_account_info(
        service_account_json, 
        scopes=SCOPES
    )
    
    return build('drive', 'v3', credentials=creds)


def load_folder_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"{CONFIG_FILE} not found!")
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

        print(f"Template created: {CONFIG_FILE}")
        print("Please edit this file with your Google Drive folder IDs")
        print("Find folder IDs in the URL: https://drive.google.com/drive/folders/FOLDER_ID")
        return None

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_images_from_folder(service, folder_id, category_name):
    print(f"Scanning folder '{category_name}'...", end=" ", flush=True)

    images = []
    try:
        query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, thumbnailLink)',
            pageSize=1000
        ).execute()

        files = results.get('files', [])

        if not files:
            print("No images found")
            return images

        files.sort(key=lambda x: x['name'])

        for file in files:
            file_id = file['id']
            thumbnail_link = file.get('thumbnailLink')
            local_thumb = None
            
            if thumbnail_link:
                local_thumb = generate_thumbnail(file_id, thumbnail_link)
                
            images.append({
                "fileId": file_id,
                "name": file['name'],
                "thumbnail": local_thumb.replace('\\', '/') if local_thumb else None
            })

        print(f"Found {len(images)} images")
        return images

    except GoogleAPICallError as e:
        print(f"Error: {e}")
        return []


def main():
    print("Google Drive Gallery Config Generator\n")

    config = load_folder_config()
    if config is None:
        return

    print("\nAuthenticating with Google Drive...")
    try:
        service = authenticate()
        print("Authentication successful\n")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    gallery_config = {}

    for category, folder_info in config['folders'].items():
        folder_id = folder_info['id']

        if folder_id == "YOUR_FOLDER_ID_HERE":
            print(f"Skipping '{category}' (folder ID not configured)")
            continue

        images = get_images_from_folder(service, folder_id, category)
        if images:
            gallery_config[category] = images

    output_file = 'gallery-config.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gallery_config, f, indent=2, ensure_ascii=False)

    print(f"\nGallery config saved to: {output_file}")
    print(f"Categories: {', '.join(gallery_config.keys())}")
    total_images = sum(len(v) for v in gallery_config.values())
    print(f"Total images: {total_images}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

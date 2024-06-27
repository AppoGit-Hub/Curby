import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from curby.core import (
    CLIENT_SECRETS, 
    YOUTUBE_SCOPES
)

def get_uploader():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, YOUTUBE_SCOPES)
    credentials = flow.run_local_server(port=8080)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def get_request_data(title: str, description: str, tags: list, privacy="private"):
    return {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": privacy
        }
    }

def upload(video_filepath: str, video_data: dict):
    youtube = get_uploader()
    request_body = get_request_data(video_data["title"], video_data["description"], video_data["tags"], video_data["privacy"])
    
    media_file = googleapiclient.http.MediaFileUpload(video_filepath, chunksize=-1, resumable=True)
    upload_request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)

    response = None
    while response is None:
        status, response = upload_request.next_chunk()
        if status:
            return response
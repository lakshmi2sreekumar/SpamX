from googleapiclient.discovery import build
from django.conf import settings


def fetch_comments(video_id, max_results=50):

    youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1,
        textFormat="plainText"
    )

    response = request.execute()

    comments = []
    for item in response.get("items", []):
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(text)

    return comments

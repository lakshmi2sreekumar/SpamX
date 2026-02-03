from .youtube import fetch_comments
from .models import predict_spam


def analyze_youtube_video(video_id):
    comments = fetch_comments(video_id)

    results = []
    for comment in comments:
        prediction = predict_spam(comment)

        results.append({
            "comment": comment,
            "prediction": prediction
        })

    return results

from .youtube import fetch_comments
from .ml_model import predict_spam

def analyze_youtube_video(video_id):

    try:
        comments = fetch_comments(video_id)

    except Exception as e:
        return [{
            "comment": "",
            "label": "error",
            "error": str(e)
        }]

    results = []

    for comment in comments:

        prediction = predict_spam(comment)

        results.append({
            "comment": comment,
            "label": prediction["label"],
            "confidence": prediction["confidence"]
        })

    return results

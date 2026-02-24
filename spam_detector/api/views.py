from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import analyze_youtube_video


@api_view(["GET"])
def analyze_video(request):
    video_id = request.GET.get("video_id")

    if not video_id:
        return Response({"error": "video_id is required"}, status=400)

    try:
        results = analyze_youtube_video(video_id)
        return Response({
            "video_id": video_id,
            "total_comments": len(results),
            "results": results
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)



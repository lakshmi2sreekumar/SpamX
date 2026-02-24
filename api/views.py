# Django REST imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Django standard imports
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Your services
from .services import analyze_youtube_video
from .ml_model import predict_spam


# ============================================
# 1. Analyze YouTube Video Comments (GET)
# ============================================

@api_view(["GET"])
def analyze_video(request):

    video_id = request.GET.get("video_id")

    if not video_id:
        return Response(
            {"error": "video_id is required"},
            status=400
        )

    results = analyze_youtube_video(video_id)

    return Response({

        "video_id": video_id,

        "total_comments": len(results),

        "results": results

    })


# ============================================
# 2. Classify Single Comment (POST)
# ============================================

@csrf_exempt
def classify_comment_view(request):

    if request.method == "POST":

        try:

            body = json.loads(request.body)

            text = body.get("text")

            if not text:

                return JsonResponse(
                    {"error": "text is required"},
                    status=400
                )

            result = predict_spam(text)

            return JsonResponse({

                "text": text,

                "label": result["label"],

                "confidence": result["confidence"]

            })

        except Exception as e:

            return JsonResponse({

                "error": str(e)

            }, status=500)


    return JsonResponse(
        {"error": "POST method required"},
        status=405
    )
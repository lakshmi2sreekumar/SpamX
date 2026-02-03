from django.urls import path
from .views import analyze_video

urlpatterns = [
    path("analyze/", analyze_video),
]


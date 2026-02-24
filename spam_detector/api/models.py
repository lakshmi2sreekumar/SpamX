import requests
from django.conf import settings


def predict_spam(text):
    headers = {
        "X-API-Key": settings.HF_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    response = requests.post(settings.HF_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return {
            "label": "error",
            "details": response.text
        }

    return response.json()


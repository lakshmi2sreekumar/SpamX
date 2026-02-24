from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "SpamX/SpamX"

print("Loading SpamX model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

print("SpamX model loaded")


def predict_spam(text):

    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    predicted_class = torch.argmax(probs, dim=1).item()

    labels = ["non-spam", "spam"]

    return {
        "label": labels[predicted_class],
        "confidence": probs[0][predicted_class].item()
    }
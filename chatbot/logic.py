import os
import base64
import google.generativeai as genai

# Configure Gemini with your API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Models for text and vision
_TEXT_MODEL = genai.GenerativeModel("gemini-pro")
_VISION_MODEL = genai.GenerativeModel("gemini-pro-vision")

def get_bot_response(user_message: str) -> str:
    """Return a text answer from Gemini."""
    try:
        response = _TEXT_MODEL.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API Gemini : {e}")
        return "D\u00e9sol\u00e9, une erreur technique est survenue. Veuillez r\u00e9essayer."


def get_bot_response_with_image(user_message: str, image_base64: str) -> str:
    """Return a Gemini answer using both text and an image."""
    try:
        image_bytes = base64.b64decode(image_base64)
        content = [
            user_message,
            {"mime_type": "image/jpeg", "data": image_bytes},
        ]
        response = _VISION_MODEL.generate_content(content)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel \u00e0 l'API Gemini (vision) : {e}")
        return (
            "D\u00e9sol\u00e9, une erreur technique est survenue lors de l'analyse de l'image. "
            "Veuillez r\u00e9essayer."
        )

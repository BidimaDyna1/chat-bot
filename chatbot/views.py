from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from .logic import get_bot_response
from .logic import get_bot_response_with_image # Nous allons créer cette fonction
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Vue pour la page d'accueil du site
def accueil_page(request):
    """
    Affiche la page d'accueil principale du site CARIMO.
    """
    return render(request, 'chatbot/accueil.html')

# Vue pour la fenêtre du chatbot (qui sera dans l'iframe)
@xframe_options_sameorigin
def chatbot_window(request):
    """
    Affiche la page contenant uniquement l'interface du chatbot.
    """
    return render(request, 'chatbot/chatbot_window.html')

# Vue pour l'API du chatbot (qui gère la logique de conversation)
# DANS VOTRE FICHIER chatbot/views.py

# ... (vos autres imports et vues restent les mêmes) ...

@csrf_exempt
def chat_api(request):
    """
    Reçoit les messages des utilisateurs (texte et/ou image) et renvoie
    la réponse du bot de manière logique.
    """
    # 1. On vérifie que la méthode est bien POST au tout début.
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        # 2. On récupère les données envoyées par FormData (pour le cas avec image)
        user_message = request.POST.get('message', '')
        image_file = request.FILES.get('image_file', None)

        # 3. Clause de secours : si c'est une requête sans image, elle est peut-être
        #    au format JSON (votre ancien système).
        if not image_file and not user_message and request.body:
            try:
                data = json.loads(request.body)
                user_message = data.get('message', '')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # 4. On vérifie qu'on a bien reçu quelque chose.
        if not user_message and not image_file:
            return JsonResponse({'error': 'Message or image is required'}, status=400)
        
        # 5. On choisit la bonne fonction logique à appeler.
        if image_file:
            # S'IL Y A UNE IMAGE : on la traite et on appelle la fonction pour les images.
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            bot_response = get_bot_response_with_image(user_message, image_base64)
        else:
            # S'IL N'Y A QUE DU TEXTE : on appelle la fonction pour le texte.
            bot_response = get_bot_response(user_message)
            
        # 6. On renvoie la réponse qui a été choisie.
        return JsonResponse({'response': bot_response})

    except Exception as e:
        # On capture toutes les autres erreurs pour un débogage facile.
        print(f"An unexpected error occurred in chat_api: {e}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)
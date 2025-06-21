# D:\gestion_ai\chatbot_projecy\chatbot\urls.py

from django.urls import path
from . import views  # Importe votre fichier views.py

app_name = 'chatbot'

urlpatterns = [
    # Route pour la page d'accueil.
    # URL : /chat/
    # Vue : accueil_page
    # Nom pour le template : 'accueil'
    path('', views.accueil_page, name='accueil'),

    # Route pour la fenêtre du chatbot.
    # URL : /chat/window/
    # Vue : chatbot_window
    # Nom pour le template : 'chatbot_window'
    path('window/', views.chatbot_window, name='chatbot_window'),
    
    # Route pour l'API qui traite les messages.
    # URL : /chat/api/
    # Vue : chat_api
    # Nom pour le template : 'process_message'  <-- C'EST LA CORRECTION !
    path('api/', views.chat_api, name='process_message'),
]
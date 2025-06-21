"""
URL configuration for service_client project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Vous n'avez plus besoin d'importer les vues ici si la racine '/' est gérée par chatbot.urls
# from chatbot import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Votre URL principale est maintenant gérée par chatbot.urls
    # Si la racine de votre site (http://127.0.0.1:8000/) doit pointer vers
    # la page d'accueil de chatbot, alors la configuration ci-dessous est correcte.
   # path('', include('chatbot.urls')), # <--- C'est ici que l'on va travailler
]

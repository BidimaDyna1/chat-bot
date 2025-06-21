import json
import os

# Chemin vers notre base de connaissances JSON
DATA_FILE = os.path.join(os.path.dirname(__file__), 'carimo_data.json')

# On charge les données une seule fois au démarrage
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    carimo_data = json.load(f)

def get_bot_response(user_message):
    """
    Fonction principale qui analyse le message de l'utilisateur et cherche une réponse.
    """
    message = user_message.lower().strip()

    # 1. On vérifie d'abord les questions générales et spécifiques
    if "horaires" in message:
        return carimo_data["entreprise"]["horaires"]
    
    if "contact" in message or "appeler" in message:
        return carimo_data["entreprise"]["contact"]

    # 2. On détecte ensuite la branche qui intéresse l'utilisateur
    branche_detectee = None
    for key, branche_info in carimo_data["branches"].items():
        if any(mot_cle in message for mot_cle in branche_info["mots_cles"]):
            branche_detectee = key
            break

    if branche_detectee:
        branche = carimo_data["branches"][branche_detectee]
        if branche_detectee == "cosmetics":
            for gamme in branche["gammes"]:
                if any(mot_cle in message for mot_cle in gamme["mots_cles"]):
                    for produit in gamme.get("produits", []):
                        if produit["nom"].lower() in message:
                            return f"Le produit '{produit['nom']}' de la gamme {gamme['nom']} coûte {produit['prix']}."
                    return gamme["description"]
            noms_des_gammes = [g["nom"] for g in branche["gammes"]]
            return f"Dans notre branche CARIMO Cosmetics, nous avons plusieurs gammes : {', '.join(noms_des_gammes)}. Laquelle vous intéresse ?"
        else:
            return branche["description"] + " Comment puis-je vous aider plus en détail ?"

    # 3. Enfin, si rien d'autre ne correspond, on gère les salutations
    if any(salutation in message for salutation in ["bonjour", "salut", "hello"]):
        return "Bonjour ! Bienvenue chez CARIMO EMPIRE. Comment puis-je vous aider concernant nos branches : Cosmétiques, Immobilier ou Haute Couture ?"

    # 4. Si on ne comprend toujours pas, on demande de clarifier
    return "Je ne suis pas sûr de comprendre. Votre demande concerne-t-elle CARIMO Cosmetics, CARIMO Immobilier ou CARIMO Haute Couture ?"
# DANS chatbot/logic.py

# ... (tout votre code existant au-dessus : DATA_FILE, carimo_data, get_bot_response) ...
# ...
# ...

# --- NOUVELLE SECTION POUR LA RECONNAISSANCE D'IMAGES ---

from openai import OpenAI

# ---------------------------------------------------------------------------------
# REMPLACEZ "sk-VOTRE_CLÉ_API_ICI" PAR VOTRE VRAIE CLÉ API OBTENUE SUR LE SITE D'OPENAI
# ---------------------------------------------------------------------------------
# Pour plus de sécurité, il est recommandé d'utiliser une variable d'environnement,
# mais pour commencer, ceci fonctionnera.
client = OpenAI(api_key="sk-VOTRE_CLÉ_API_ICI")


def get_bot_response_with_image(user_message, image_base64):
    """
    Fonction qui envoie un message texte ET une image à l'API d'OpenAI (GPT-4o)
    pour obtenir une réponse intelligente.
    """
    
    # 1. Préparer le message pour l'IA
    messages_pour_ia = [
        {
            "role": "system",
            "content": """
            Tu es un assistant expert pour la marque de luxe CARIMO EMPIRE.
            La marque a trois branches : Cosmétiques, Immobilier, Haute Couture.
            Si l'utilisateur envoie une photo de l'un de nos produits, identifie-le
            et donne son nom et sa description si possible. Si l'image n'est pas claire
            ou ne correspond à aucun produit, dis-le poliment.
            Sois toujours professionnel, concis et serviable.
            """
        }
    ]

    # 2. Construire le contenu de la requête de l'utilisateur
    contenu_utilisateur = []
    
    # Ajouter le texte s'il y en a
    if user_message:
        contenu_utilisateur.append({
            "type": "text",
            "text": user_message
        })

    # Ajouter l'image (obligatoire pour cette fonction)
    contenu_utilisateur.append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}"
        }
    })

    messages_pour_ia.append({
        "role": "user",
        "content": contenu_utilisateur
    })

    # 3. Envoyer la requête à l'API d'OpenAI
    try:
        response = client.chat.completions.create(
            # gpt-4o est le modèle le plus récent et performant pour la vision
            model="gpt-4o", 
            messages=messages_pour_ia,
            max_tokens=250  # Limite la longueur de la réponse
        )
        # 4. Renvoyer la réponse texte de l'IA
        return response.choices[0].message.content
        
    except Exception as e:
        # Gérer les erreurs (clé API incorrecte, problème de connexion, etc.)
        print(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return "Désolé, une erreur technique est survenue lors de l'analyse de l'image. Veuillez réessayer."
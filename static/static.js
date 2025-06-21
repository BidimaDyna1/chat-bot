// Attend que tout le contenu de la page soit chargé avant d'exécuter le script
document.addEventListener('DOMContentLoaded', function() {
    
    const carouselContainer = document.querySelector('.carousel-container');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    // DANS VOTRE FICHIER JS OU DANS LA BALISE <script>

const imageUploadInput = document.getElementById('image-upload-input');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeImageBtn = document.getElementById('remove-image-btn');

// Gère la sélection d'une image
imageUploadInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreviewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

// Gère la suppression de l'image prévisualisée
removeImageBtn.addEventListener('click', function() {
    imageUploadInput.value = ''; // Réinitialise l'input file
    imagePreviewContainer.style.display = 'none';
});


// FONCTION D'ENVOI DE MESSAGE MODIFIÉE
async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const imageFile = imageUploadInput.files[0];

    if (userInput.trim() === '' && !imageFile) {
        return; // Ne rien faire si tout est vide
    }

    // Utiliser FormData pour envoyer à la fois du texte et des fichiers
    const formData = new FormData();
    formData.append('message', userInput);
    if (imageFile) {
        formData.append('image_file', imageFile);
    }
    
    // Afficher le message de l'utilisateur (et l'image s'il y en a une)
    // ... (votre code existant pour ajouter le message au chat) ...

    try {
        const response = await fetch('/chat/api/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        // Afficher la réponse du bot
        // ... (votre code existant) ...
        // ex: addMessageToChat('bot', data.response);

    } catch (error) {
        console.error('Erreur:', error);
        // Gérer l'erreur d'affichage
    }
    
    // Vider les champs après l'envoi
    document.getElementById('user-input').value = '';
    removeImageBtn.click(); // Simule un clic pour cacher la preview
}
    // Vérifie si les éléments du carrousel existent avant de continuer
    if (!carouselContainer || slides.length === 0 || !prevBtn || !nextBtn) {
        return;
    }

    let currentIndex = 0;
    const totalSlides = slides.length;

    function showSlide(index) {
        // Déplace le conteneur horizontalement
        carouselContainer.style.transform = `translateX(-${index * 100}%)`;
    }

    // Gère le clic sur le bouton "Suivant"
    nextBtn.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % totalSlides; // Revient au début si on est à la fin
        showSlide(currentIndex);
    });

    // Gère le clic sur le bouton "Précédent"
    prevBtn.addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides; // Va à la fin si on est au début
        showSlide(currentIndex);
    });

    // Initialise le carrousel à la première image
    showSlide(currentIndex);
});
#######################################################################################################################################
## BIBLIOTHÈQUES NÉCESSAIRES POUR LE PROJET LSQ                                                                                      ##
#######################################################################################################################################

TOUCHE_QUITTER = 'q'
TOUCHE_TRADUCTION = '1'
TOUCHE_TUTORIEL = '2'
COULEUR_TEXTE = (0,255,0)
TAILLE_TITRE = 1.2
TAILLE_SOUS_TITRE = 0.5
TAILLE_IMAGE = (200, 200)
ATTENTE_TOUCHE = 5

# Inclusion du script d'autocomplétion
from autocompletion import autocompletion_mot

# Inclusion de la bibliothèque pour ignorer les warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Inclusion de la bibliothèque d'aléatoire
import random

# Inclusion de la bibliothèque pour les collections
from collections import deque

# Inclusion de la bibliothèque de temps
import time 
derniere_lecture = 0

# Inclusion de la bibliothèque de lecture de caméra
import cv2

# Inclusion de la bibliothèque MediaPipe pour le traitement d'images
import mediapipe as mp
# Dessiner les résultats de détection
mp_dessin = mp.solutions.drawing_utils 
# Ajouter des couleurs différentes selon le type d'articulation (paume, doigts, etc.)
mp_styles = mp.solutions.drawing_styles
# Module principal pour la détection des mains
mp_mains = mp.solutions.hands

# Inclusion de la bibliothèque pour lire à voix haute
import win32com.client
voix = win32com.client.Dispatch("SAPI.SpVoice")
lettre = ""
ancienne_lettre = ""
lettre_a_repeter = ""

# Inclusion de la bibliothèque pour les appels asynchrones
import threading

# Inclusion de la bibliothèque pour le modèle KNN ("Machine Learning" pour la classification)
import joblib
knn = joblib.load('ressources/modele_knn_lsq.pkl')

# Liste des chemins complets des images
import os

# Initialisation de la capture vidéo depuis la caméra
camera = cv2.VideoCapture(0)

# Mode choisi par l'utilisateur
mode = ""

# Images du tutoriel
dossier_images = os.path.join("ressources", "img_tutoriel")

# Extensions acceptées
extensions_images = ('.png', '.jpg', '.jpeg')

# Dictionnaire généré par ChatGPT (ChatGPT, 2025) pour associer une image à son nom
dictionnaire_images = {
    # Séparer l'extension du nom complet du fichier ("chat.png" -> "chat", "png") : 
    # joindre le nom complet du fichier à la route
    os.path.splitext(images)[0]: os.path.join(dossier_images, images)
    for images in os.listdir(dossier_images)
    if images.lower().endswith(extensions_images)
}

# Phrase ou mot généré(e) par l'utilisateur pour l'autocomplétion
phrase = deque([], maxlen=20) 

#######################################################################################################################################
## FONCTIONS NÉCESSAIRES POUR LE PROJET LSQ                                                                                          ##
#######################################################################################################################################

# Vérifications simples générées
# @author Olivier Godon-Vandal
def verification():
    print("OpenCV version :", cv2.__version__)
    print("MediaPipe version :", mp.__version__)
    print("Joblib version :", joblib.__version__)

# Fonction pour lire une lettre à voix haute
# @author Olivier Godon-Vandal
def lectureLettre(lettre):
    if isinstance(lettre, str) and lettre:
        voix.Speak(lettre)
    else :
        raise ValueError("Aucune lettre à lire")

# Fonction pour afficher une phrase
# @param image : image (frame) sur la quelle affichée le texte
# @author Olivier Godon-Vandal
def afficherPhrase(image):
    cv2.putText(image, f"Phrase : {''.join(phrase)}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)

# Fonction pour extraire des traits pour KNN
# @param reperes: Liste des repères de la main détectée
# @return: Liste des coordonnées x, y, z de chaque repère
# Code généré par : OpenAI. (2025). ChatGPT (version 29 juillet 2025)
def extraire_traits(reperes):
    resultat = []
    for repere in reperes:
        resultat.extend([repere.x, repere.y, repere.z])
    return resultat

# Fonction pour changer de mode en fonction des touches saisies
# @param touche : détection de la touche
# @author Olivier Godon-Vandal
def detection_touche(touche):
    global mode
    if touche == ord(TOUCHE_TRADUCTION):
        mode = "traduction"
    elif touche == ord(TOUCHE_TUTORIEL):
        mode = "tutoriel"
    elif touche == ord(TOUCHE_QUITTER):
        if mode == "":
            camera.release()
            cv2.destroyAllWindows()
            exit(0)
        else :
            mode = ""

# Fonction pour dessiner les traits et jointures sur la main détectée
# @param image : image sur laquelle dessiner
# @param main_reperes : repères de la main détectés
# Inspiré de : https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
def dessiner_traits_main(image, main_reperes):
    mp_dessin.draw_landmarks(
        image,
        main_reperes,
        mp_mains.HAND_CONNECTIONS,
        mp_styles.get_default_hand_landmarks_style(),
        mp_styles.get_default_hand_connections_style())
    
# Fonction pour lire les images de la caméra et afficher le tutoriel
# Inspiré de : https://medium.com/@odil.tokhirov/how-i-built-a-hand-gesture-recognition-model-in-python-part-1-db378cf196e6
# @author Olivier Godon-Vandal
def lectureMain():
    global lettre, mode

    with mp_mains.Hands(
        static_image_mode=False,  # False si vidéo, True si image statique
        max_num_hands=1,          # Nombre maximum de mains à détecter
        model_complexity=1,       # Complexité du modèle : 0 (léger), 1 (équilibré), 2 (précis)
        min_detection_confidence=0.5,  # Seuil de confiance pour la détection
        min_tracking_confidence=0.5   # Seuil de confiance pour le suivi
    ) as mains:
        while camera.isOpened():
            estOuverte, image = camera.read()
            if not estOuverte:
                # Doc : https://www.w3schools.com/python/gloss_python_raise.asp
                raise ValueError("Impossible d'ouvrir la caméra.") 
            
            # Améliorer les performances en marquant l'image comme non modifiable
            resultats = optimisation_image(mains, image)

            touche = cv2.waitKey(ATTENTE_TOUCHE) & 0xFF
            detection_touche(touche)
         
            # Afficher les indications à l'utilisateur
            if mode == "":
                # Gestion des touches
                affichage_indications(image)

            # Afficher le mode traduction
            elif mode == "traduction":
                afficher_traduction(image)

            # Afficher le mode tutoriel
            elif mode == "tutoriel":
                afficher_tutoriel(image)

            if resultats.multi_hand_landmarks:
                for main_reperes in resultats.multi_hand_landmarks:
                    dessiner_traits_main(image, main_reperes)
                    reconnaitre_geste(main_reperes.landmark)
            else:
                lettre = ""

            # Affichage des images en continu
            cv2.imshow('LSQ', image)

    camera.release()
    cv2.destroyAllWindows()

# Fonction pour lire une lettre à voix haute dans un fil (thread) séparé
# @param lettre : Lettre à lire
# @author Olivier Godon-Vandal
def lire_lettre(lettre):
    fil = threading.Thread(target=lectureLettre, args=(lettre,))
    fil.start()

# Fonction pour enregistrer une lettre dans la phrase à afficher à l'utilisateur 
# @author Olivier Godon-Vandal
def enregistrer_lettre():
    if lettre == "ESPACE":
        phrase.append(" ")
    elif lettre == "SUPPRIMER":
        if phrase:
            phrase[-1] = phrase[-1][:-1]
            if phrase[-1] == "":
                phrase.pop()
    elif lettre == "CONFIRMER":
        if phrase:
            mot_en_cours = ''
            while phrase and phrase[-1] != ' ': # si HELLO WORLD, retourne WORLD
                mot_en_cours = phrase.pop() + mot_en_cours

            mot_complet = autocompletion_mot(mot_en_cours)
            for i in mot_complet:
                phrase.append(i)
    else:
        phrase.append(lettre) 
        
# Fonction pour reconnaître les gestes basés sur les landmarks de la main
# @param reperes: Liste des landmarks de la main détectée
# @return: Lettre reconnue par le modèle KNN
# Code généré par : OpenAI. (2025). ChatGPT (version 29 juillet 2025)
def reconnaitre_geste(reperes):
    global lettre, ancienne_lettre, derniere_lecture, mode

    # Prédiction par modèle
    traits = extraire_traits(reperes)
    lettre = knn.predict([traits])[0]

    # Temps
    maintenant = time.time()

    # Lire une lettre qui est affichée depuis plus de 3 secondes
    if mode == "traduction":
        if lettre != ancienne_lettre:
            ancienne_lettre = lettre
            derniere_lecture = maintenant
        elif (maintenant - derniere_lecture >= 3):
            # Lance la lecture dans un thread séparé
            derniere_lecture = maintenant
            lire_lettre(lettre)
            enregistrer_lettre()
    elif mode == "tutoriel":
        if lettre == lettre_a_repeter:
            lettre_aleatoire()
            lire_lettre(lettre)

    return lettre

# Fonction pour choisir une lettre aléatoire à répéter dans le tutoriel
# @author Olivier Godon-Vandal
def lettre_aleatoire():
    global lettre_a_repeter
    lettre_a_repeter = random.choice(list(dictionnaire_images.keys())) 

# Fonction pour afficher une image en fonction de la lettre à répéter
# @param image: Image à afficher dans l'interface de tutoriel
# @author Olivier Godon-Vandal
def afficher_image(image):
    global lettre_a_repeter
    tuto_img = cv2.imread(dictionnaire_images.get(lettre_a_repeter)) 
    tuto_img = cv2.resize(tuto_img, TAILLE_IMAGE)
    # Code généré par : OpenAI. (2025). ChatGPT (version 29 juillet 2025)
    h, w, _ = tuto_img.shape 
    image[0:h, -w:] = tuto_img

# Fonction pour afficher les indications à l'utilisateur dans le menu principal
# @param image: "frame" de la caméra pour afficher les indications
# @author Olivier Godon-Vandal
def affichage_indications(image):
    cv2.putText(image, f"Bienvenue sur l'application pour apprendre la langue des signes!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_TITRE, COULEUR_TEXTE, 2)
    cv2.putText(image, f"Appuyez sur '1' pour commencer la traduction", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)
    cv2.putText(image, f"Appuyez sur '2' pour commencer le tutoriel", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)
    cv2.putText(image, f"Appuyez sur 'q' pour quitter l'application", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)

# Fonction pour afficher la traduction à l'utilisateur dans le mode traduction
# @param image: "frame" de la caméra pour afficher les indications
# @author Olivier Godon-Vandal
def afficher_traduction(image):
    global lettre, phrase
    cv2.putText(image, f"Lettre : {lettre}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_TITRE, COULEUR_TEXTE, 2)
    cv2.putText(image, f"Phrase : {''.join(phrase)}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)
    cv2.putText(image, f"Essayez-vous de de signer '{autocompletion_mot(''.join(phrase))}' ? Faites un pouce pour confirmer.", (10, 430), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)

# Fonction pour afficher le tutoriel à l'utilisateur dans le mode tutoriel
# @param image: "frame" de la caméra pour afficher les indications
# @author Olivier Godon-Vandal
def afficher_tutoriel(image):
        if lettre_a_repeter == "":
            lettre_aleatoire()
        else:
            afficher_image(image)
                
        cv2.putText(image, f"Lettre : {lettre_a_repeter}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_TITRE, COULEUR_TEXTE, 2)
        cv2.putText(image, "Veuillez imiter l'image sur la droite", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, TAILLE_SOUS_TITRE, COULEUR_TEXTE, 2)

# Fonction pour optimiser l'affichage de l'image
# @param mains: Instance de MediaPipe Hands pour le traitement d'image
# @param image: "frame" de la caméra pour afficher les indications
# @return: Résultats du traitement d'image par MediaPipe
# @author Olivier Godon-Vandal
def optimisation_image(mains, image):
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image.flags.writeable = True
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    resultats = mains.process(image_rgb)
    return resultats

#######################################################################################################################################
## COMPILATION POUR LE PROJET LSQ                                                                                                    ##
#######################################################################################################################################

if __name__ == "__main__":
    verification()
    lectureMain()

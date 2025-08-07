#######################################################################################################################################
## BIBLIOTHÈQUES NÉCESSAIRES POUR LE PROJET LSQ                                                                                      ##
#######################################################################################################################################

DIMENSION_FENETRE = 320 
NB_IMAGE_MAX = 3000

# Inclusion de la bibliothèque pour ignorer les warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Importation des bibliothèques nécessaires
import cv2
import mediapipe as mp
import os
import csv

# Initialisation de MediaPipe pour la détection de mains sur image
mp_mains = mp.solutions.hands
mains = mp_mains.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# Chemin vers le dossier contenant les images et la sortie du CSV
chemin_donnees = os.path.join("ressources","img_mains","ASL_Alphabet_Dataset","asl_alphabet_train")
sortie_csv = os.path.join("ressources","donnees_main.csv")

#######################################################################################################################################
## CRÉATION DU FICHIER CSV                                                                                                           ##
#######################################################################################################################################

# Création du CSV et ouverture avec les noms de colonnes
with open(sortie_csv, mode = 'w', newline = '') as fichier:
    writer = csv.writer(fichier, delimiter=';')
    # MediaPipe détecte 18 repères dans une main, sous des coordonnées X, Y et Z.
    header = [
                'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20',
                'y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y10', 'y11', 'y12', 'y13', 'y14', 'y15', 'y16', 'y17', 'y18', 'y19', 'y20',
                'z0', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9', 'z10', 'z11', 'z12', 'z13', 'z14', 'z15', 'z16', 'z17', 'z18', 'z19', 'z20',
                'label'
            ]
    writer.writerow(header)

    # Pour chaque sous-dossier (représente une lettre : A, B, C, ...)
    # Code partiellement généré par : OpenAI. (2025). ChatGPT (version 29 juillet 2025) [Modèle massif 
    # de langage]. https://chat.openai.com/chat
    liste_dossiers_tries = sorted(os.listdir(chemin_donnees))

    for nom in liste_dossiers_tries:
        #nom_dossier = f"{chemin_donnees}/{nom}" <-- Les barres obliques peuvent être problématiques. Elles changent d'orientation entre Linux et Windows.
        nom_dossier = os.path.join(chemin_donnees, nom) # <-- Beaucoup plus fiable

        print(f"\n▶ Traitement des images pour la classe '{nom}'...")
        liste_images = os.listdir(nom_dossier)
        
        # Parcours des premières X images de chaque dossier 
        #for i, nom_image in enumerate(liste_images[:NB_IMAGE_MAX]):  
        for i, nom_image in enumerate(liste_images):
            chemin_image = os.path.join(nom_dossier, nom_image)
            image = cv2.imread(chemin_image) # Lire l'image

            # Redimensionne l'image pour uniformiser les tailles (améliore performance/détection)
            image = cv2.resize(image, (DIMENSION_FENETRE, DIMENSION_FENETRE))
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            resultats = mains.process(image_rgb)

            # Si une main est détectée, extraire les landmarks
            if resultats.multi_hand_landmarks:
                main_reperes_coor = resultats.multi_hand_landmarks[0]
                rangee = []

                # Pour chaque repère de la main, sauver les coordonnées X, Y, Z
                for repere in main_reperes_coor.landmark:
                    rangee.extend([repere.x, repere.y, repere.z]) # Extend -> Ajouter un itérable la fin d'une liste
                rangee.append(nom) # Append -> Ajouter un élément à la fin d'une liste

                writer.writerow(rangee)
            else:
                print(f"❌ Pas de main détectée : {chemin_image}")

print("Reconnaissance terminée.")

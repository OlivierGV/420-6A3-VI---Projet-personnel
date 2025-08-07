# Autocomplétion des mots
# Inspiré de : https://www.youtube.com/watch?v=g5BdNoxwt2E&ab_channel=NeuralNine
import requests as requetes
import os

# Ouverture (une fois) du fichier fr.text
# Code généré par : OpenAI. (2025). ChatGPT (version 29 juillet 2025)
# Fichier fr.txt saisi de : https://raw.githubusercontent.com/lorenbrichter/Words/refs/heads/master/Words/fr.txt
with open(os.path.join("ressources", "dictionnaires", "fr.txt"), encoding="utf-8") as fichier:
    dictionnaire = [mot.strip().lower() for mot in fichier if mot.strip()] # ['a', 'b', 'c']

# Fonction pour obtenir les suggestions d'autocomplétion de mot
# @param sequence: la séquence de caractères à compléter
# @author Olivier Godon-Vandal
def autocompletion_mot(sequence):
    sequence = sequence.strip().lower()
    if not sequence:
        return ""  

    mots = sequence.split()
    if not mots:
        return ""  

    dernier_mot = mots[-1]

    # Filtrer les mots du dictionnaire commençant par le dernier mot
    suggestions = [mot for mot in dictionnaire if mot.startswith(dernier_mot)]
    return suggestions[0].upper() if suggestions else dernier_mot  

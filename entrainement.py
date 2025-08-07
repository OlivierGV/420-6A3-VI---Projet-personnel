# Script généré par ChatGPT (ChatGPT, 2025) pour entraîner un modèle KNN sur les données de la main
# Documentation : https://scikit-learn.org/stable/index.html
# Documentation : https://www.w3schools.com/python/python_ml_train_test.asp

#######################################################################################################################################
## BIBLIOTHÈQUES NÉCESSAIRES POUR LE PROJET LSQ                                                                                      ##
#######################################################################################################################################

# Inclusion de la bibliothèque pour ignorer les warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Importation des bibliothèques nécessaires
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

#######################################################################################################################################
## PRÉPARATION DES TESTS                                                                                                             ##
#######################################################################################################################################

# Chargement des données du fichier excel
donnees_csv = pd.read_csv('ressources/donnees_main.csv', sep=";")

X = donnees_csv.drop('label', axis=1)
y = donnees_csv['label']

# Entraîner et tester le modèle avec les images
# 20% des données utilisées pour le test, 80% pour l'entraînement
X_entrainement, X_test, Y_entrainement, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#######################################################################################################################################
## PRÉPARATION DU MODÈLE                                                                                                             ##
#######################################################################################################################################

# Créer et entraîner un modèle KNN selon les 5 voisins les plus proches (en terme de distance)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_entrainement, Y_entrainement)

#######################################################################################################################################
## RAPPORTS DES TESTS                                                                                                                ##
#######################################################################################################################################

# Prédiction sur les données
y_pred = knn.predict(X_test)
# Calculer le score de précision (bonnes réponses)
print("Précision :", accuracy_score(y_test, y_pred))
# Rapport détaillé pour chaque test et prédiction
print(classification_report(y_test, y_pred))

# Sauvegarder le modèle
joblib.dump(knn, 'ressources/modele_knn_lsq.pkl')

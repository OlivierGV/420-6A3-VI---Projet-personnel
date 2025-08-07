import unittest
import string
from unittest.mock import patch, MagicMock
from collections import namedtuple, deque
import lsq
from lsq import lettre, phrase, mode, lettre_a_repeter, lectureLettre, extraire_traits, enregistrer_lettre, detection_touche, lettre_aleatoire, TOUCHE_TRADUCTION, TOUCHE_TUTORIEL, TOUCHE_QUITTER

class TestLectureLettre(unittest.TestCase):
    # Vérifier si un paramètre valide est prononcé
    def test_lecture_lettre_valide(self):
        lettre_test = "A"
        mot_test = "ESPACE"
        lettre_special = "É"
        lectureLettre(lettre_test)
        lectureLettre(lettre_test.lower())
        lectureLettre(mot_test)
        lectureLettre(mot_test.lower())
        lectureLettre(lettre_special)
        lectureLettre(lettre_special.lower())

    def test_lecture_lettre_invalide(self):
        # Vérifier si un paramètre vide est perçu comme une erreur
        with self.assertRaises(ValueError):
            lectureLettre("")

        # Vérifier si un paramètre inexistant est perçu comme une erreur
        with self.assertRaises(ValueError):
            lectureLettre(None)
    
class TestExtraireTraits(unittest.TestCase):
    # Vérifier si les repères valides sont bien lus 
    # Code généré par : OpenAI. (2025). ChatGPT (version 6 août 2025)
    def test_extraire_traits_valides(self):
        Landmark = namedtuple('Landmark', ['x', 'y', 'z'])
        reperes = [Landmark(x=0.1 * i, y=0.2 * i, z=0.3 * i) for i in range(21)]
        traits = extraire_traits(reperes)
        self.assertEqual(len(traits), 63)
    
class TestEnregistrerLettre(unittest.TestCase):
    # Avant chaque test
    def setUp(self):
        phrase.clear()
        global lettre
        lettre = ""
    
    # Vérifier si une lettre valide est bien enregistrée
    def test_enregistrer_lettre(self):
        global lettre
        lsq.lettre = "A"
        enregistrer_lettre()
        self.assertEqual(list(lsq.phrase), ["A"])

    # Vérifier si un espace est bien enregistré
    def test_enregistrer_espace(self):
        global lettre
        lsq.lettre = "ESPACE"
        enregistrer_lettre()
        self.assertEqual(list(lsq.phrase), [" "])
    
    # Vérifier si la suppression supprime bien la dernière lettre
    def test_supprimer_lettre(self):
        global lettre
        lsq.phrase.extend(["H", "E", "L", "L", "O"])
        lsq.lettre = "SUPPRIMER"
        enregistrer_lettre()
        self.assertEqual(list(lsq.phrase), ["H", "E", "L", "L"])

class TestChangementMode(unittest.TestCase):
    # Avant chaque test
    def setUp(self):
        global mode
        lsq.mode = ""

    def test_touche_traduction(self):
        detection_touche(ord(TOUCHE_TRADUCTION))
        self.assertEqual(lsq.mode, "traduction")
    
    def test_touche_tutoriel(self):
        detection_touche(ord(TOUCHE_TUTORIEL))
        self.assertEqual(lsq.mode, "tutoriel")

    @patch("lsq.exit")
    def test_touche_quitter_traduction(self, mock_exit):
        global mode
        lsq.mode = "traduction"
        detection_touche(ord(TOUCHE_QUITTER))
        self.assertEqual(lsq.mode, "")
        mock_exit.assert_not_called()

    @patch("lsq.exit")
    def test_touche_quitter_tutoriel(self, mock_exit):
        global mode
        lsq.mode = "tutoriel"
        detection_touche(ord(TOUCHE_QUITTER))
        self.assertEqual(lsq.mode, "")
        mock_exit.assert_not_called()
    
class TestLettreAleatoire(unittest.TestCase):
    def test_lettre_aleatoire(self):
        
        lettre_aleatoire()

        # Vérifier si la lettre n'est pas vide
        self.assertTrue(lsq.lettre_a_repeter, "La lettre ne devrait pas être vide")

        # Vérifier si la lettre existe et est singulière
        self.assertEqual(len(lsq.lettre_a_repeter), 1, "La lettre doit être un seul caractère")

        # Vérifier que la lettre n'est pas un signe spécial
        self.assertTrue(lsq.lettre_a_repeter.isalpha(), "La lettre doit être alphabétique")

        # Vérifier que la lettre fait partie de l'alphabet
        self.assertIn(lsq.lettre_a_repeter.lower(), string.ascii_lowercase, "La lettre doit être dans l'alphabet")

if __name__ == '__main__':
    unittest.main()

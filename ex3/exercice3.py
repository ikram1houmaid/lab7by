
from datetime import datetime
import copy


# Mixin 1 : ValidationMixin
class ValidationMixin:

    def valider_titre(self):
        if not self.titre or not self.titre.strip():
            raise ValueError("Le titre est obligatoire et ne peut pas être vide.")

        return True


# Mixin 2 : HistoriqueMixin
class HistoriqueMixin:

    def __init__(self):
        self.historique = []

    def enregistrer_historique(self):
        ancienne_version = {
            "description": self.description,
            "date": datetime.now()
        }

        self.historique.append(copy.deepcopy(ancienne_version))

    def afficher_historique(self):
        if not self.historique:
            print("Aucun historique disponible.")
        else:
            print("\n--- Historique des modifications ---")

            for i, version in enumerate(self.historique, start=1):
                print(f"Version {i}")
                print(f"Description : {version['description']}")
                print(f"Date : {version['date']}")
                print("------------------------")


# Mixin 3 : JournalisationMixin
class JournalisationMixin:

    def journaliser(self, action):
        print(f"[Journal] {datetime.now()} : {action}")


# Classe principale Tache
class Tache(
    ValidationMixin,
    HistoriqueMixin,
    JournalisationMixin
):

    def __init__(self, titre, description):
        HistoriqueMixin.__init__(self)

        self.titre = titre
        self.description = description
        self.date_creation = datetime.now()

        self.valider_titre()

        self.journaliser(f"Création de la tâche '{self.titre}'")

    def mettre_a_jour(self, description):
        self.valider_titre()

        self.enregistrer_historique()

        self.description = description

        self.journaliser(f"Modification de la tâche '{self.titre}'")

    def afficher_tache(self):
        print("\n--- Informations de la tâche ---")
        print(f"Titre : {self.titre}")
        print(f"Description : {self.description}")
        print(f"Date de création : {self.date_creation}")


# -----------------------------
# EXEMPLE D'UTILISATION
# -----------------------------

# Création d'une tâche
tache = Tache(
    "Projet Python",
    "Préparer le premier exercice"
)

# Afficher la tâche
tache.afficher_tache()

# Première modification
tache.mettre_a_jour("Préparer les exercices Python")

# Deuxième modification
tache.mettre_a_jour("Terminer tous les exercices Python")

# Afficher les informations actuelles
tache.afficher_tache()

# Afficher l'historique
tache.afficher_historique()


from datetime import datetime
import json

# Mixin 1 : Horodatable
class Horodatable:
    def horodatage(self):
        print(f"[LOG] Action à {datetime.now()}")


# Mixin 2 : Validable
class Validable:
    def valider(self):
        if not getattr(self, "titre", None):
            raise ValueError("Titre manquant")

        print("Validation OK")


# Mixin 3 : Serializable
class Serializable:
    def to_json(self):
        donnees = {
            "titre": self.titre,
            "contenu": self.contenu
        }

        return json.dumps(donnees, ensure_ascii=False, indent=4)


# Mixin 4 : Historisable
class Historisable:
    def __init__(self):
        self.historique = []

    def ajouter_action(self, action):
        self.historique.append({
            "action": action,
            "date": str(datetime.now())
        })

    def afficher_historique(self):
        for element in self.historique:
            print(element)


# Classe principale Document
class Document(Horodatable, Validable, Serializable, Historisable):

    def __init__(self, titre, contenu):
        self.titre = titre
        self.contenu = contenu
        Historisable.__init__(self)

    def sauvegarder(self):
        self.horodatage()
        self.valider()
        self.ajouter_action("Sauvegarde du document")

        print(f"Document '{self.titre}' sauvegardé.")


# Exemple d'utilisation
doc = Document("Rapport", "Contenu important")

# Sauvegarder
doc.sauvegarder()

# Convertir en JSON
print("\n--- Conversion JSON ---")
print(doc.to_json())

# Afficher l'historique
print("\n--- Historique des actions ---")
doc.afficher_historique()

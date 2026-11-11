
import json
import csv
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring


# Mixin 1 : Serializable
class Serializable:

    def to_json(self):
        donnees = {
            key: value
            for key, value in self.__dict__.items()
            if key != "historique"
        }
        return json.dumps(donnees, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        donnees = json.loads(json_str)
        return cls(**donnees)


# Mixin 2 : Historisable
class Historisable:

    def __init__(self):
        self.historique = []

    def enregistrer_etat(self):
        etat = {
            key: value
            for key, value in self.__dict__.items()
            if key != "historique"
        }
        self.historique.append({
            "date": datetime.now().isoformat(),
            "etat": etat.copy()
        })


# Mixin 3 : Journalisable
class Journalisable:

    def journaliser(self, message):
        print(f"[Journal] {datetime.now()}: {message}")


# Mixin 4 : Horodatable
class Horodatable:

    def horodater(self):
        return datetime.now().isoformat()


# Mixin 5 : ExportCSV
class ExportCSV:

    def exporter_csv(self, nom_fichier):
        with open(nom_fichier, "w", newline="", encoding="utf-8") as fichier:
            champs = [
                key for key in self.__dict__
                if key != "historique"
            ]

            writer = csv.DictWriter(fichier, fieldnames=champs)
            writer.writeheader()

            donnees = {
                key: value for key, value in self.__dict__.items()
                if key != "historique"
            }

            writer.writerow(donnees)

        print("Export CSV effectué.")


# Mixin 6 : ExportXML
class ExportXML:

    def exporter_xml(self, nom_fichier):
        racine = Element(self.__class__.__name__)

        for key, value in self.__dict__.items():
            if key != "historique":
                element = SubElement(racine, key)
                element.text = str(value)

        contenu = tostring(racine, encoding="unicode")

        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write(contenu)

        print("Export XML effectué.")


# Classe métier Contrat
class Contrat(
    Serializable,
    Historisable,
    Journalisable,
    Horodatable,
    ExportCSV,
    ExportXML
):

    def __init__(self, id, description):
        Historisable.__init__(self)
        self.id = id
        self.description = description

    def modifier(self, nouvelle_desc):
        self.enregistrer_etat()
        self.journaliser(f"Modification du contrat {self.id}")
        self.description = nouvelle_desc
        print("Contrat modifié.")


# Classe métier Commande
class Commande(
    Serializable,
    Historisable,
    Journalisable,
    Horodatable,
    ExportCSV,
    ExportXML
):

    def __init__(self, id, montant):
        Historisable.__init__(self)
        self.id = id
        self.montant = montant

    def modifier(self, nouveau_montant):
        self.enregistrer_etat()
        self.journaliser(f"Modification de la commande {self.id}")
        self.montant = nouveau_montant
        print("Commande modifiée.")


# Classe métier Client
class Client(
    Serializable,
    Historisable,
    Journalisable,
    Horodatable,
    ExportCSV,
    ExportXML
):

    def __init__(self, id, nom):
        Historisable.__init__(self)
        self.id = id
        self.nom = nom

    def modifier(self, nouveau_nom):
        self.enregistrer_etat()
        self.journaliser(f"Modification du client {self.id}")
        self.nom = nouveau_nom
        print("Client modifié.")


# -----------------------------
# EXEMPLES D'UTILISATION
# -----------------------------

# Test Contrat
print("===== CONTRAT =====")

c = Contrat(1, "Initial")
c.modifier("Révisé")

print(c.to_json())

print("Historique :", c.historique)

print("Horodatage :", c.horodater())

# Test désérialisation
nouveau_contrat = Contrat.from_json(c.to_json())
print("Contrat restauré :", nouveau_contrat.to_json())

# Export CSV et XML
c.exporter_csv("contrat.csv")
c.exporter_xml("contrat.xml")


# Test Commande
print("\n===== COMMANDE =====")

commande = Commande(2, 1500)
commande.modifier(2000)
print(commande.to_json())


# Test Client
print("\n===== CLIENT =====")

client = Client(3, "Ikram")
client.modifier("Sara")
print(client.to_json())

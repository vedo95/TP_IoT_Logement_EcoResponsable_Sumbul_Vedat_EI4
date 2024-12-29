import sqlite3
from datetime import datetime, timedelta
import random

# =======================================================
# Configurer les adaptateurs pour gérer les datetime
# =======================================================
# Adaptateur pour transformer datetime en string
def adapt_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Convertisseur pour transformer string en datetime
def convert_datetime(s):
    return datetime.strptime(s.decode("utf-8"), "%Y-%m-%d %H:%M:%S")

# Enregistrer les adaptateurs ets convertisseurs
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)

# Connexion à la base de données avec détection des types
conn = sqlite3.connect(r'..\Database\TP1.db', detect_types=sqlite3.PARSE_DECLTYPES )

cursor = conn.cursor()
# =======================================================
# Fonction pour vider une table
# =======================================================
def vider_table(nom_table):
    print(f"Vidage de la table {nom_table}...")
    cursor.execute(f"DELETE FROM {nom_table};")
    conn.commit()
    print(f"Table {nom_table} vidée avec succès.")

# =======================================================
# Fonction pour insérer des logements
# =======================================================
def inserer_logements():
    print("Insertion des logements...")
    logements = [
        ('123 Rue Verte', '0123456789', '192.168.0.1'),
        ('456 Rue Bleue', '0987654321', '192.168.0.2')
    ]
    cursor.executemany(
        "INSERT INTO Logements (adresse, numero_telephone, adresse_ip) VALUES (?, ?, ?)",
        logements
    )
    conn.commit()
    print("Logements insérés avec succès.")

# =======================================================
# Fonction pour insérer des pièces
# =======================================================
def inserer_pieces():
    print("Insertion des pièces...")
    pieces = [
        ('Salon', 0, 0, 0, 1),
        ('Cuisine', 1, 0, 0, 1),
        ('Chambre', 0, 1, 0, 1),
        ('Salle de bain', 0, 0, 1, 1),
        ('Garage', 0, -1, 0, 2)
    ]
    cursor.executemany(
        "INSERT INTO Pieces (nom_piece, x_coord, y_coord, z_coord, id_logement) VALUES (?, ?, ?, ?, ?)",
        pieces
    )
    conn.commit()
    print("Pièces insérées avec succès.")

# =======================================================
# Fonction pour insérer des types de capteurs/actionneurs
# =======================================================
def inserer_types_capteurs_actionneurs():
    print("Insertion des types de capteurs/actionneurs...")
    types = [
        ('Température', '°C', '[-50, 50]'),
        ('Lumière', 'Lux', '[0, 1000]'),
        ('Humidité', '%', '[0, 100]'),
        ('Électricité', 'kWh', '[0, 10000]')
    ]
    cursor.executemany(
        "INSERT INTO Type_Capt_Actionneur (nom_type, unite_mesure, plage_precision) VALUES (?, ?, ?)",
        types
    )
    conn.commit()
    print("Types de capteurs/actionneurs insérés avec succès.")

# =======================================================
# Fonction pour insérer des capteurs/actionneurs
# =======================================================
def inserer_capteurs_actionneurs():
    print("Insertion des capteurs/actionneurs...")
    capteurs_actionneurs = [
        ('Température', 'Ref123', 'COM1', 1),
        ('Lumière', 'Ref456', 'COM2', 2),
        ('Humidité', 'Ref789', 'COM3', 3),
        ('Électricité', 'Ref321', 'COM4', 4)
    ]
    cursor.executemany(
        "INSERT INTO Capteurs_Actionneurs (type, reference_commerciale, port_communication, id_piece) VALUES (?, ?, ?, ?)",
        capteurs_actionneurs
    )
    conn.commit()
    print("Capteurs/actionneurs insérés avec succès.")

# =======================================================
# Fonction pour insérer des mesures
# =======================================================
def inserer_mesures():
    print("Insertion des mesures...")
    mesures = []
    for id_capt_act in range(1, 5):  # Suppose qu'il y a 4 capteurs
        for _ in range(2):  # Deux mesures par capteur
            valeur = round(random.uniform(10, 30), 2)  # Valeur entre 10 et 30
            date_insertion = datetime.now() - timedelta(days=random.randint(0, 30))
            mesures.append((id_capt_act, valeur, date_insertion))
    cursor.executemany(
        "INSERT INTO Mesures (id_capt_act, valeur, date_insertion) VALUES (?, ?, ?)",
        mesures
    )
    conn.commit()
    print("Mesures insérées avec succès.")

# =======================================================
# Fonction pour insérer des factures
# =======================================================
def inserer_factures():
    print("Insertion des factures...")
    factures = []
    for _ in range(4):  # Quatre factures
        type_facture = random.choice(['Électricité', 'Eau', 'Déchets'])
        date_facture = datetime.now() - timedelta(days=random.randint(30, 120))
        montant = round(random.uniform(20, 200), 2)  # Montant entre 20 et 200
        consommation = round(random.uniform(50, 500), 2)  # Consommation entre 50 et 500
        factures.append((1, type_facture, date_facture, montant, consommation))
    cursor.executemany(
        "INSERT INTO Factures (id_logement, type, date_facture, montant, consommation) VALUES (?, ?, ?, ?, ?)",
        factures
    )
    conn.commit()
    print("Factures insérées avec succès.")

# =======================================================
# Exécution des fonctions
# =======================================================
# Vidage des tables avant d'insérer de nouvelles données
vider_table("Mesures")
vider_table("Capteurs_Actionneurs")
vider_table("Type_Capt_Actionneur")
vider_table("Pieces")
vider_table("Factures")
vider_table("Logements")

# Insertion des données dans les tables
inserer_logements()
inserer_pieces()
inserer_types_capteurs_actionneurs()
inserer_capteurs_actionneurs()
inserer_mesures()
inserer_factures()

# Fermeture de la connexion
conn.close()
print("Remplissage terminé.")

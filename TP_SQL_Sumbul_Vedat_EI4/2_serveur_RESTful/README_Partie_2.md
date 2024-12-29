
# Serveur RESTful - TP IoT Logement Éco-Responsable

## Introduction
Cette partie du TP consiste à écrire le code correspondant à un serveur RESTful en Python. Le serveur gère la communication avec une base de données SQLite et permet de manipuler les entités liées au logement éco-responsable, telles que les **logements**, **pièces**, **capteurs/actionneurs**, **mesures**, et **factures**.

---

## Structure du Projet
### Fichiers Principaux :
- **`serveur.py`** : Contient l'implémentation du serveur RESTful en Python avec Flask.
- **`remplissage.py`** : Remplit la base de données SQLite avec des données initiales.
- **Base de données** : Le fichier `TP1.db` dans le répertoire `Database` contient toutes les tables nécessaires.

---

## Fonctionnalités Principales
### Exercices :
1. **Remplissage de la base de données** :
   - Utilisation de requêtes GET et POST pour ajouter ou lire des données.
   - Les données sont pré-remplies via le script Python `remplissage.py`.

2. **Camembert des Factures** :
   - Une route GET permet de générer dynamiquement une page HTML affichant un camembert (Google Charts) basé sur les données des factures.

3. **Prévisions Météo** :
   - Intégration d'une API météo pour afficher les prévisions à 5 jours sous forme de tableau HTML.

4. **Actions Basées sur les Capteurs** :
   - Simulations des capteurs et déclenchement d'actions si certaines conditions sont remplies (exemple : allumer une LED si la température dépasse un seuil).

---

## Lancer le Serveur

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Remplir la base de données** :
   Exécutez le script `remplissage.py` pour insérer des données initiales :
   ```bash
   python remplissage.py
   ```

3. **Démarrer le serveur** :
   Lancez le serveur Flask :
   ```bash
   python serveur.py
   ```

4. **Accéder à l'application** :
   Ouvrez un navigateur et visitez [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Routes REST Implémentées

### Logements :
- **Obtenir la liste des logements** :
  ```bash
  curl -X GET http://127.0.0.1:5000/logements
  ```
- **Ajouter un logement** :
  ```bash
  curl -X POST http://127.0.0.1:5000/logements   -H "Content-Type: application/json"   -d '{"adresse": "123 Rue Verte", "numero_telephone": "0123456789", "adresse_ip": "192.168.0.1"}'
  ```

### Pièces :
- **Obtenir la liste des pièces** :
  ```bash
  curl -X GET http://127.0.0.1:5000/pieces
  ```
- **Ajouter une pièce** :
  ```bash
  curl -X POST http://127.0.0.1:5000/pieces   -H "Content-Type: application/json"   -d '{"nom_piece": "Salon", "x_coord": 5, "y_coord": 3, "z_coord": 2, "id_logement": 1}'
  ```

### Mesures :
- **Obtenir la liste des mesures** :
  ```bash
  curl -X GET http://127.0.0.1:5000/mesures
  ```
- **Ajouter une mesure** :
  ```bash
  curl -X POST http://127.0.0.1:5000/mesures   -H "Content-Type: application/json"   -d '{"id_capt_act": 1, "valeur": 30.5}'
  ```
- **Afficher les mesures avec actions associées** :
  ```bash
  curl -X GET http://127.0.0.1:5000/mesures/actions
  ```

### Factures :
- **Afficher le graphique des factures sous forme de camembert** :
  ```bash
  curl -X GET http://127.0.0.1:5000/factures/piechart
  ```

### Prévisions Météo :
- **Afficher les prévisions météo d’une ville en tableau HTML** (exemple pour Paris) :
  ```bash
  curl -X GET http://127.0.0.1:5000/meteo/Paris
  ```

---

## Notes Importantes
- Les seuils de déclenchement pour les actions (exemple : température > 25°C) sont configurés dans `serveur.py` via la variable `TEMP_SEUIL`.
- Le fichier `remplissage.py` doit être exécuté pour insérer des données avant le démarrage du serveur.
- La clé API pour OpenWeather est incluse dans le code (`serveur.py`) mais peut être modifiée si nécessaire.

---
## Contact

Pour toute question ou suggestion :  
- **Nom** : Vedat Sumbul
- **Email** : vedat.sumbul@etu.sorbonne-universite.fr  
- **GitHub** : https://github.com/vedo95/TP_IoT_Logement_EcoResponsable_Sumbul_Vedat_EI4

Ce projet a été réalisé dans le cadre d'un travail pratique pour  Internet of Things (IoT) à Polytech Sorbonne.

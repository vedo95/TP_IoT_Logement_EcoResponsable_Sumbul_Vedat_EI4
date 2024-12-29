# TP IoT : Partie 1 - Construction et Remplissage de la Base de Données

---

## Contenu de la Partie 1

### 1. Modèle Relationnel
- **Question 1** : Le modèle relationnel validé est disponible dans le fichier suivant :
  - **Fichier** : `Q1_modele_relationnel.png`

### 2. Script SQL : `logement.sql`
Ce fichier contient les réponses aux **questions 2 à 8** :
- **Question 2** : Détruire toutes les tables existantes :  
  - Lignes **2 à 12**.
- **Question 3** : Création des tables :
  - Logements : Ligne **15 à 22**
  - Pièces : Ligne **25 à 34**
  - Capteurs/Actionneurs : Ligne **37 à 45**
  - Types de Capteurs/Actionneurs : Ligne **48 à 54**
  - Mesures : Ligne **57 à 63**
  - Factures : Ligne **66 à 73**
- **Questions 4 à 8** : Insertion des données :
  - Non inclus directement dans ce fichier SQL, mais gérées par le script Python `remplissage.py`.

### 3. Script Python : `remplissage.py`
- Ce script insère automatiquement les données pour les **questions 4 à 8**.
  - **Ligne 37 à 45** : Fonction `inserer_logements` pour insérer 2 logements.
  - **Ligne 48 à 56** : Fonction `inserer_pieces` pour insérer 5 pièces associées aux logements.
  - **Ligne 59 à 67** : Fonction `inserer_types_capteurs_actionneurs` pour insérer 4 types de capteurs/actionneurs.
  - **Ligne 70 à 78** : Fonction `inserer_capteurs_actionneurs` pour insérer 4 capteurs/actionneurs.
  - **Ligne 81 à 92** : Fonction `inserer_mesures` pour insérer 2 mesures par capteur.
  - **Ligne 95 à 105** : Fonction `inserer_factures` pour insérer 4 factures.
- **Vidage des tables** : Ligne **30 à 35** avec la fonction `vider_table`.

---

## Comment cela fonctionne

### Étape 1 : Modèle Relationnel
- Le fichier `Q1_modele_relationnel.png` représente la structure validée des tables et relations.

### Étape 2 : Création de la Base de Données
1. Charger le fichier SQL dans SQLite :
   ```bash
   sqlite3 database.db
   .read logement.sql
   ```
   Cela crée les tables décrites dans le fichier `logement.sql`.

### Étape 3 : Remplissage Automatique des Données
1. Exécuter le script Python pour insérer les données automatiquement :
   ```bash
   python remplissage.py
   ```
   Le script insère des logements, des pièces, des capteurs/actionneurs, des mesures et des factures dans la base de données `database.db`.

---

## Résumé des Localisations

| Question | Localisation                                    |
|----------|------------------------------------------------|
| Q1       | `Q1_modele_relationnel.png`                   |
| Q2       | `logement.sql`, lignes 2-12                   |
| Q3       | `logement.sql`, lignes 15-73                 |
| Q4 à Q8  | `remplissage.py`, lignes 37-105              |

---

## Contact

Pour toute question ou suggestion :  
- **Nom** : Vedat Sumbul
- **Email** : vedat.sumbul@etu.sorbonne-universite.fr  
- **GitHub** : https://github.com/vedo95/TP_IoT_Logement_EcoResponsable_Sumbul_Vedat_EI4

Ce projet a été réalisé dans le cadre d'un travail pratique pour  Internet of Things (IoT) à Polytech Sorbonne.

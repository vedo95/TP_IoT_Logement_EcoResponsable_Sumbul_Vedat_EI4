
# HarmonieVerte

![HarmonieVerte Logo](static/img/logo.png)

**HarmonieVerte** est une application web conçue pour gérer les logements, capteurs et actionneurs au sein d'un environnement intelligent. Cette application offre une interface conviviale pour permettre aux utilisateurs de configurer leurs paramètres, ajouter/supprimer des logements, ainsi que des capteurs/actionneurs.

---

## Table des Matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
   - [Cloner le Dépôt](#1-cloner-le-dépôt)
   - [Créer un Environnement Virtuel](#2-créer-un-environnement-virtuel-recommandé)
   - [Installer les Dépendances](#3-installer-les-dépendances)
3. [Lancer le Serveur](#lancer-le-serveur)
4. [Structure du Projet](#structure-du-projet)
5. [Fonctionnalités](#fonctionnalités)
6. [Dépannage](#dépannage)
7. [Licence](#licence)
8. [Contact](#contact)

---

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.7 ou supérieur**  
  [Télécharger Python](https://www.python.org/downloads/)
- **pip** (gestionnaire de paquets Python)  
  Vérifiez son installation avec :  
  ```bash
  pip --version
  ```

---

## Installation

### 1. Cloner le Dépôt

Si vous avez **Git** installé, vous pouvez cloner le dépôt. Sinon, téléchargez le code source en tant que fichier ZIP et extrayez-le.

```bash
git clone https://github.com/votre-utilisateur/harmonieverte.git
```

### 2. Créer un Environnement Virtuel (Recommandé)

Pour isoler les dépendances du projet, créez un environnement virtuel :

```bash
python -m venv venv
```

Activez l'environnement virtuel :  

- **Sur Windows** :  
  ```bash
  venv\Scripts\activate
  ```
- **Sur macOS et Linux** :  
  ```bash
  source venv/bin/activate
  ```

### 3. Installer les Dépendances

Les dépendances nécessaires sont listées dans le fichier `requirements.txt`. Installez-les en utilisant `pip` :

```bash
pip install -r requirements.txt
```

---

## Lancer le Serveur

Une fois que l'environnement est configuré et les dépendances installées, lancez le serveur Flask :

```bash
python serveur.py
```

**Accéder à l'Application :**  
Ouvrez votre navigateur et accédez à l'adresse suivante :  
```bash
http://localhost:5000/
```

---

## Structure du Projet

Voici la structure des fichiers et des dossiers principaux du projet :

```plaintext
harmonieverte/
├── Database/
│   └── TP1.db
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── capteurs.js
│   │   ├── configuration.js
│   │   ├── economies.js
│   │   ├── consommation.js
│   │   ├── main.js
│   │   └── meteo.js
│   └── img/
│       └── capteur-icon.png
│       └── consommation-icon.png
│       └── eco-house.png
│       └── economies-icon.png
│       └── meteo-icon.png
├── templates/
│   ├── index.html
│   ├── capteurs.html
│   ├── configuration.html
│   ├── economies.html
│   ├── consommation.html
├── serveur.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Description des Dossiers et Fichiers

- **`Database/`** : Contient le fichier de base de données SQLite (`TP1.db`).
- **`static/`** : Contient les fichiers statiques tels que CSS, JavaScript et images.
  - **`css/styles.css`** : Feuille de style principale.
  - **`js/`** : Scripts JavaScript pour les différentes fonctionnalités de l'application.
    - `capteurs.js` : Gestion des capteurs/actionneurs.
    - `configuration.js` : Configuration des logements et utilisateurs.
    - `economies.js` : Gestion des économies réalisées.
    - `consommation.js` : Gestion de la consommation.
    - `main.js` : Script principal.
    - `meteo.js` : Gestion des prévisions météo.
- **`templates/`** : Contient les fichiers HTML pour les différentes pages de l'application :
  - `index.html` : Page d'accueil.
  - `capteurs.html` : Gestion des capteurs/actionneurs.
  - `configuration.html` : Page de configuration.
  - `economies.html` : Page des économies réalisées.
  - `consommation.html` : Gestion de la consommation.
- **`serveur.py`** : Script principal du serveur Flask.
- **`requirements.txt`** : Liste des dépendances Python nécessaires.
- **`README.md`** : Documentation du projet.
- **`.gitignore`** : Exclusion de certains fichiers/dossiers dans Git.

---

## Fonctionnalités

1. **Paramètres Utilisateur**  
   Configurez votre nom et votre email via la section Paramètres Utilisateur. Remplissez le formulaire et cliquez sur "Enregistrer".
2. **Gestion des Capteurs/Actionneurs**  
   - **Affichage** : Liste des capteurs/actionneurs existants.  
   - **Ajout** : Ajoutez un capteur/actionneur via le formulaire dédié.  
   - **Suppression** : Supprimez un capteur/actionneur existant via un bouton dédié.
3. **Gestion des Logements**  
   - **Affichage** : Liste des logements existants.  
   - **Ajout** : Ajoutez un logement via le formulaire dédié.  
   - **Suppression** : Supprimez un logement via un bouton dédié.
4. **Mesures et Actions**  
   Consultez les mesures récentes des capteurs et les actions associées via `/mesures/actions`.
5. **Graphiques et Factures**  
   - Visualisez les montants des factures par type sous forme de graphiques via `/factures/piechart`.
6. **Météo**  
   Consultez les prévisions météo d'une ville via `/meteo/`.  
   Exemple :  
   ```bash
   http://localhost:5000/meteo/
   ```

---

## Dépannage

### Problèmes fréquents et solutions :

1. **Erreur `IndexError: No item with that key`**  
   - Vérifiez que les colonnes utilisées dans le code Flask correspondent aux tables de la base de données.  
   - Assurez-vous que `TP1.db` est bien dans le dossier `Database`.

2. **Problèmes de Connexion à la Base de Données**  
   - Vérifiez que `TP1.db` existe et a les bonnes permissions.  
   - Assurez-vous que le chemin est correct dans `serveur.py`.

3. **Le Serveur Flask Ne Démarre Pas**  
   - Vérifiez qu'aucun autre processus n'utilise le port 5000.  
   - Installez les dépendances via `pip install -r requirements.txt`.

4. **Fichiers Statiques Non Chargés (CSS/JS)**  
   - Vérifiez les chemins des fichiers statiques dans les templates HTML.

5. **Erreur CORS**  
   - Installez et configurez correctement Flask-Cors.

6. **Clé API OpenWeather Invalide**  
   - Vérifiez ou régénérez la clé API OpenWeather utilisée.


---

## Contact

Pour toute question ou suggestion :  
- **Nom** : Vedat Sumbul
- **Email** : vedat.sumbul@etu.sorbonne-universite.fr  
- **GitHub** : https://github.com/vedo95/TP_IoT_Logement_EcoResponsable_Sumbul_Vedat_EI4

Ce projet a été réalisé dans le cadre d'un travail pratique pour  Internet of Things (IoT) à Polytech Sorbonne.

from flask import Flask, jsonify, request  # Flask pour gérer les requêtes HTTP
import sqlite3  # SQLite pour la gestion de la base de données
import logging  # Pour le logging des informations et des erreurs
import requests  # Pour effectuer les requêtes HTTP (ex. API météo)
import random  # Pour générer des valeurs simulées
from threading import Timer  # Pour simuler des actions périodiques

# Température seuil pour déclencher l'action (par exemple, allumer une LED)
TEMP_SEUIL = 25.0


# =======================================================
# Configurer les logs
# =======================================================
# Initialise les logs pour suivre les exécutions avec des niveaux de gravité (INFO, DEBUG, ERROR).
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialisation de l'application Flask
app = Flask(__name__)

# =======================================================
# Fonction utilitaire : Connexion à SQLite
# =======================================================
def get_db_connection():
    """
    Initialise et retourne une connexion à la base de données SQLite.
    Les lignes retournées par les requêtes peuvent être accédées par clé.
    """
    logging.info("Connexion à la base de données SQLite")
    conn = sqlite3.connect(r'..\Database\TP1.db')
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

# =======================================================
# Route : Page d'accueil
# =======================================================
@app.route('/')
def index():
    """
    Fournit un message de bienvenue à la racine de l'application.
    """
    logging.info("Route '/' appelée")
    return jsonify({'message': 'Bienvenue sur le serveur RESTful du TP IOT. Consultez la documentation pour utiliser les endpoints.'})

# =======================================================
# Gestion des Logements
# =======================================================

@app.route('/logements', methods=['GET'])
def get_logements_html():
    """
    Affiche tous les logements sous forme de tableau HTML structuré.
    """
    logging.info("Route '/logements' appelée (GET)")
    conn = get_db_connection()
    logements = conn.execute('SELECT * FROM Logements').fetchall()
    conn.close()

    # Génération du tableau HTML à partir des données des logements
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liste des Logements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            h1 {
                text-align: center;
                margin: 20px 0;
                color: #333;
            }
            table {
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #fff;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 12px;
                text-align: center;
            }
            th {
                background-color: #f9f9f9;
                font-weight: bold;
                color: #555;
            }
            tr:nth-child(even) {
                background-color: #f3f3f3;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            caption {
                font-size: 1.2em;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Liste des Logements</h1>
        <table>
            <caption>Informations sur les logements</caption>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Adresse</th>
                    <th>Numéro de Téléphone</th>
                    <th>Adresse IP</th>
                    <th>Date d'Insertion</th>
                </tr>
            </thead>
            <tbody>
    """

    # Ajout des lignes du tableau pour chaque logement
    for logement in logements:
        html_content += f"""
            <tr>
                <td>{logement['id_logement']}</td>
                <td>{logement['adresse']}</td>
                <td>{logement['numero_telephone']}</td>
                <td>{logement['adresse_ip']}</td>
                <td>{logement['date_insertion']}</td>
            </tr>
        """

    # Fermeture du tableau et du HTML
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    logging.info("Page HTML des logements générée avec succès.")
    return html_content

@app.route('/logements', methods=['POST'])
def add_logement():
    """
    Ajoute un nouveau logement dans la base de données.
    Champs requis : adresse, numero_telephone, adresse_ip.
    """
    logging.info("Route '/logements' appelée (POST)")
    new_logement = request.get_json()
    logging.debug(f"Données reçues : {new_logement}")

    # Vérification des champs obligatoires
    if not new_logement or 'adresse' not in new_logement or 'numero_telephone' not in new_logement or 'adresse_ip' not in new_logement:
        logging.error("Champs manquants dans les données reçues")
        return jsonify({'error': 'Champs requis : adresse, numero_telephone, adresse_ip'}), 400

    # Insertion dans la base
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Logements (adresse, numero_telephone, adresse_ip) VALUES (?, ?, ?)',
        (new_logement['adresse'], new_logement['numero_telephone'], new_logement['adresse_ip'])
    )
    conn.commit()
    conn.close()
    logging.info("Logement ajouté avec succès")
    return jsonify({'message': 'Logement ajouté avec succès!'}), 201


# =======================================================
# Gestion des Pièces
# =======================================================
@app.route('/pieces', methods=['GET'])
def get_pieces_html():
    """
    Affiche toutes les pièces sous forme de tableau HTML structuré.
    """
    logging.info("Route '/pieces' appelée (GET)")
    conn = get_db_connection()
    pieces = conn.execute('SELECT * FROM Pieces').fetchall()
    conn.close()

    # Génération du tableau HTML à partir des données des pièces
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liste des Pièces</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            h1 {
                text-align: center;
                margin: 20px 0;
                color: #333;
            }
            table {
                width: 90%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #fff;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 12px;
                text-align: center;
            }
            th {
                background-color: #f9f9f9;
                font-weight: bold;
                color: #555;
            }
            tr:nth-child(even) {
                background-color: #f3f3f3;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            caption {
                font-size: 1.2em;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Liste des Pièces</h1>
        <table>
            <caption>Informations sur les pièces</caption>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Coordonnée X</th>
                    <th>Coordonnée Y</th>
                    <th>Coordonnée Z</th>
                    <th>ID Logement</th>
                </tr>
            </thead>
            <tbody>
    """

    # Ajout des lignes du tableau pour chaque pièce
    for piece in pieces:
        html_content += f"""
            <tr>
                <td>{piece['id_piece']}</td>
                <td>{piece['nom_piece']}</td>
                <td>{piece['x_coord']}</td>
                <td>{piece['y_coord']}</td>
                <td>{piece['z_coord']}</td>
                <td>{piece['id_logement']}</td>
            </tr>
        """

    # Fermeture du tableau et du HTML
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    logging.info("Page HTML des pièces générée avec succès.")
    return html_content

@app.route('/pieces', methods=['POST'])
def add_piece():
    """
    Ajoute une pièce à un logement existant.
    Champs requis : nom_piece, x_coord, y_coord, z_coord, id_logement.
    """
    logging.info("Route '/pieces' appelée (POST)")
    new_piece = request.get_json()
    logging.debug(f"Données reçues : {new_piece}")

    if not new_piece or 'nom_piece' not in new_piece or 'x_coord' not in new_piece or 'y_coord' not in new_piece or 'z_coord' not in new_piece or 'id_logement' not in new_piece:
        logging.error("Champs manquants dans les données reçues")
        return jsonify({'error': 'Champs requis : nom_piece, x_coord, y_coord, z_coord, id_logement'}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Pieces (nom_piece, x_coord, y_coord, z_coord, id_logement) VALUES (?, ?, ?, ?, ?)',
        (new_piece['nom_piece'], new_piece['x_coord'], new_piece['y_coord'], new_piece['z_coord'], new_piece['id_logement'])
    )
    conn.commit()
    conn.close()
    logging.info("Pièce ajoutée avec succès")
    return jsonify({'message': 'Pièce ajoutée avec succès!'}), 201


# =======================================================
# Gestion des Mesures
# =======================================================
@app.route('/mesures', methods=['GET'])
def get_mesures_html():
    """
    Affiche toutes les mesures sous forme de tableau HTML structuré.
    """
    logging.info("Route '/mesures' appelée (GET)")
    conn = get_db_connection()
    mesures = conn.execute('SELECT * FROM Mesures').fetchall()
    conn.close()

    # Génération du tableau HTML à partir des données des mesures
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liste des Mesures</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            h1 {
                text-align: center;
                margin: 20px 0;
                color: #333;
            }
            table {
                width: 90%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #fff;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 12px;
                text-align: center;
            }
            th {
                background-color: #f9f9f9;
                font-weight: bold;
                color: #555;
            }
            tr:nth-child(even) {
                background-color: #f3f3f3;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            caption {
                font-size: 1.2em;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Liste des Mesures</h1>
        <table>
            <caption>Informations sur les mesures enregistrées</caption>
            <thead>
                <tr>
                    <th>ID Mesure</th>
                    <th>ID Capteur/Actionneur</th>
                    <th>Valeur</th>
                    <th>Date d'Insertion</th>
                </tr>
            </thead>
            <tbody>
    """

    # Ajout des lignes du tableau pour chaque mesure
    for mesure in mesures:
        html_content += f"""
            <tr>
                <td>{mesure['id_mesure']}</td>
                <td>{mesure['id_capt_act']}</td>
                <td>{mesure['valeur']}</td>
                <td>{mesure['date_insertion']}</td>
            </tr>
        """

    # Fermeture du tableau et du HTML
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    logging.info("Page HTML des mesures générée avec succès.")
    return html_content

@app.route('/mesures', methods=['POST'])
def add_mesure():
    """
    Ajoute une mesure pour un capteur/actionneur spécifique.
    Champs requis : id_capt_act, valeur.
    """
    logging.info("Route '/mesures' appelée (POST)")
    new_mesure = request.get_json()
    logging.debug(f"Données reçues : {new_mesure}")

    if not new_mesure or 'id_capt_act' not in new_mesure or 'valeur' not in new_mesure:
        logging.error("Champs manquants dans les données reçues")
        return jsonify({'error': 'Champs requis : id_capt_act, valeur'}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Mesures (id_capt_act, valeur, date_insertion) VALUES (?, ?, datetime("now"))',
        (new_mesure['id_capt_act'], new_mesure['valeur'])
    )
    conn.commit()
    conn.close()
    logging.info("Mesure ajoutée avec succès")
    return jsonify({'message': 'Mesure ajoutée avec succès!'}), 201

# =======================================================
# Gestion des Factures et des Graphiques
# =======================================================
@app.route('/factures/piechart', methods=['GET'])
def factures_piechart():
    """
    Génère une page HTML affichant un camembert des montants des factures à l'aide de Google Charts.
    Affiche les montants en pourcentage.
    """
    logging.info("Route '/factures/piechart' appelée (GET)")

    # Connexion à la base de données
    conn = get_db_connection()
    factures = conn.execute('SELECT type, SUM(montant) as total FROM Factures GROUP BY type').fetchall()
    conn.close()

    # Vérification si des factures existent dans la base de données
    if not factures:
        logging.warning("Aucune facture trouvée dans la base de données")
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Répartition des Factures</title>
        </head>
        <body>
            <h1>Aucune facture disponible</h1>
            <p>Veuillez insérer des factures dans la base de données pour voir le graphique.</p>
        </body>
        </html>
        """

    # Préparer les données pour Google Charts
    facture_data = [['Type de facture', 'Montant total']]  # En-tête pour Google Charts
    facture_data += [[facture['type'], facture['total']] for facture in factures]

    logging.debug(f"Données des factures pour graphique : {facture_data}")

    # Générer le contenu HTML avec Google Charts
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Répartition des Factures</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {{'packages':['corechart']}});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {{
                var data = google.visualization.arrayToDataTable({facture_data});

                var options = {{
                    title: 'Répartition des Montants des Factures',
                    is3D: true,
                    width: 800,
                    height: 600,
                    pieSliceText: 'percentage',  // Affiche les pourcentages
                    legend: {{ position: 'right', alignment: 'center' }},
                    sliceVisibilityThreshold: 0.02  // Affiche les tranches > 2%
                }};

                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }}
        </script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            #piechart {{
                margin: 20px auto;
                display: block;
            }}
        </style>
    </head>
    <body>
        <h1>Répartition des Montants des Factures</h1>
        <div id="piechart"></div>
    </body>
    </html>
    """
    return html_content

# =======================================================
# Prévisions météo (Route pour récupérer la météo à 5 jours)
# =======================================================
OPENWEATHER_API_KEY = "b2d6603b64a6f81f2e328dda41ce2666"  #
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.route('/meteo/<city>', methods=['GET'])
def get_weather_forecast_as_table_in_french(city):
    """
    Récupère les prévisions météo pour les 5 prochains jours et affiche les résultats dans un tableau HTML en français.
    """
    logging.info(f"Route '/meteo/{city}' appelée (GET)")

    # Préparer les paramètres pour la requête API
    params = {
        'q': city,  # Nom de la ville
        'appid': OPENWEATHER_API_KEY,  # Clé API OpenWeatherMap
        'units': 'metric',  # Température en degrés Celsius
        'cnt': 40  # Maximum de prévisions (8 par jour pour 5 jours)
    }

    try:
        # Effectuer la requête à l'API OpenWeatherMap
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status()  # Vérifie si la requête a réussi

        # Extraire les données JSON de la réponse
        weather_data = response.json()

        # Traduction des descriptions météo en français
        translation = {
            "clear sky": "ciel dégagé",
            "few clouds": "quelques nuages",
            "scattered clouds": "nuages épars",
            "broken clouds": "nuages fragmentés",
            "shower rain": "averse",
            "rain": "pluie",
            "thunderstorm": "orage",
            "snow": "neige",
            "mist": "brume",
            "overcast clouds": "nuages couverts",
            "moderate rain": "pluie modérée",
            "heavy intensity rain": "pluie intense",
            "light rain": "pluie légère",
            "light snow": "neige légère"
        }

        # Regrouper les prévisions par jour
        daily_forecast = {}
        for entry in weather_data['list']:
            date = entry['dt_txt'].split(' ')[0]  # Extraire la date (YYYY-MM-DD)
            if date not in daily_forecast:
                daily_forecast[date] = []

            # Ajouter les détails de la prévision au jour correspondant
            description = translation.get(entry['weather'][0]['description'], entry['weather'][0]['description'])
            daily_forecast[date].append({
                'time': entry['dt_txt'].split(' ')[1],  # Heure de la prévision
                'temperature': entry['main']['temp'],  # Température en degrés Celsius
                'description': description,  # Description météo traduite
                'humidity': entry['main']['humidity']  # Humidité (optionnel)
            })

        # Générer la page HTML avec le tableau des prévisions
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prévisions météo pour {city}</title>
            <style>
                table {{
                    width: 80%;
                    border-collapse: collapse;
                    margin: 20px auto;
                    font-family: Arial, sans-serif;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background-color: #f4f4f4;
                }}
                h1 {{
                    text-align: center;
                    font-family: Arial, sans-serif;
                }}
            </style>
        </head>
        <body>
            <h1>Prévisions météo pour {city}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Heure</th>
                        <th>Température (°C)</th>
                        <th>Description</th>
                        <th>Humidité (%)</th>
                    </tr>
                </thead>
                <tbody>
        """.format(city=city.capitalize())

        # Ajouter les données des prévisions dans le tableau
        for date, details in daily_forecast.items():
            for detail in details:
                html_content += f"""
                    <tr>
                        <td>{date}</td>
                        <td>{detail['time']}</td>
                        <td>{detail['temperature']}</td>
                        <td>{detail['description']}</td>
                        <td>{detail['humidity']}</td>
                    </tr>
                """

        # Fermer les balises HTML
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        return html_content

    # Gestion des erreurs possibles pendant la requête
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            logging.error("Clé API invalide ou permissions manquantes.")
            return jsonify({'error': 'Clé API invalide ou permissions manquantes. Veuillez vérifier votre clé API.'}), 401
        elif response.status_code == 404:
            logging.error(f"Ville non trouvée : {city}")
            return jsonify({'error': f"Ville '{city}' introuvable. Veuillez vérifier le nom de la ville."}), 404
        else:
            logging.error(f"Erreur HTTP lors de la requête API : {e}")
            return jsonify({'error': 'Erreur lors de la récupération des données météo.'}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête API : {e}")
        return jsonify({'error': 'Impossible de récupérer les données météo.'}), 500


from flask import render_template_string

# =======================================================
# Simuler les données des capteurs et exécuter des actions
# =======================================================
def simuler_capteurs_et_actions():
    """
    Simule les mesures des capteurs en insérant des données dans la base de données
    et vérifie si une action doit être effectuée (par exemple, allumer une LED).
    """
    logging.info("Simulation des données des capteurs et vérification des actions")

    # Connexion à la base de données
    conn = get_db_connection()

    # Simuler une mesure de température aléatoire pour un capteur spécifique
    id_capt_act = 1  # Exemple : Capteur 1 (vous pouvez le rendre dynamique)
    valeur_simulee = random.uniform(20.0, 35.0)  # Générer une température entre 20 et 35 degrés
    conn.execute(
        'INSERT INTO Mesures (id_capt_act, valeur, date_insertion) VALUES (?, ?, datetime("now"))',
        (id_capt_act, valeur_simulee)
    )
    conn.commit()

    logging.info(f"Mesure simulée insérée : Capteur {id_capt_act}, Température = {valeur_simulee} °C")

    # Vérifier si la température dépasse le seuil
    if valeur_simulee > TEMP_SEUIL:
        logging.info(
            f"Température {valeur_simulee} °C dépasse le seuil de {TEMP_SEUIL} °C. Action déclenchée : LED ALLUMÉE.")
    else:
        logging.info(
            f"Température {valeur_simulee} °C est inférieure ou égale au seuil de {TEMP_SEUIL} °C. LED ETEINTE.")

    conn.close()

    # Relancer la simulation après un délai (ex. 10 secondes)
    Timer(10, simuler_capteurs_et_actions).start()


# =======================================================
# Route pour afficher les données sous forme de tableau
# =======================================================
@app.route('/mesures/actions', methods=['GET'])
def afficher_mesures_et_actions():
    """
    Affiche les mesures et les actions associées sous forme de tableau.
    """
    logging.info("Route '/mesures/actions' appelée (GET)")

    # Connexion à la base de données
    conn = get_db_connection()

    # Récupérer les mesures récentes
    mesures = conn.execute(
        '''
        SELECT 
            m.id_mesure, 
            m.id_capt_act, 
            m.valeur, 
            m.date_insertion,
            CASE
                WHEN m.valeur > ? THEN 'LED allumée'
                ELSE 'LED éteinte'
            END AS action
        FROM Mesures m
        ORDER BY m.date_insertion DESC
        ''',
        (TEMP_SEUIL,)  # Seuil de température
    ).fetchall()
    conn.close()

    # Générer le tableau HTML
    html_table = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mesures et Actions</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            table {
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                background: #fff;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 10px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>Mesures et Actions Associées</h1>
        <table>
            <thead>
                <tr>
                    <th>ID Mesure</th>
                    <th>ID Capteur</th>
                    <th>Température (°C)</th>
                    <th>Date d'Insertion</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
    """

    for mesure in mesures:
        html_table += f"""
        <tr>
            <td>{mesure['id_mesure']}</td>
            <td>{mesure['id_capt_act']}</td>
            <td>{mesure['valeur']:.2f}</td>
            <td>{mesure['date_insertion']}</td>
            <td>{mesure['action']}</td>
        </tr>
        """

    html_table += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html_table


# =======================================================
# Démarrage de la simulation des capteurs
# =======================================================
if __name__ == '__main__':
    logging.info("Démarrage du serveur Flask et simulation des capteurs")

    # Lancer la simulation des capteurs et des actions
    simuler_capteurs_et_actions()

    # Démarrer le serveur Flask
    app.run(debug=True)

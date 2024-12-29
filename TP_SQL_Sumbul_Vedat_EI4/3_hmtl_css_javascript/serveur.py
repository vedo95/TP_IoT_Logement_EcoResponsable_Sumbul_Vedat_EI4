from flask import Flask, jsonify, request, render_template
import sqlite3
import logging
import requests
import random
from threading import Timer
from flask_cors import CORS

# =======================================================
# Configuration globale
# =======================================================
TEMP_SEUIL = 25.0  # Seuil de température
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Clé API OpenWeather
OPENWEATHER_API_KEY = "b2d6603b64a6f81f2e328dda41ce2666"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# =======================================================
# Connexion à la base de données SQLite
# =======================================================
def get_db_connection():
    """
    Initialise et retourne une connexion à la base de données SQLite.
    Active le mode WAL et autorise plusieurs threads (check_same_thread=False)
    pour limiter les erreurs "database is locked".
    """
    logging.info("Connexion à la base de données SQLite")
    # IMPORTANT : on utilise check_same_thread=False pour permettre
    # l'accès depuis plusieurs threads, et on active WAL.
    conn = sqlite3.connect(r'Database\TP1.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Activer le mode WAL pour réduire les verrous
    conn.execute("PRAGMA journal_mode=WAL;")

    return conn

# =======================================================
# Routes HTML principales (5 pages)
# =======================================================
@app.route('/', endpoint='index')
def route_index():
    """
    Page d'accueil (templates/index.html)
    Endpoint nommé 'index' => url_for('index')
    """
    logging.info("Route '/' appelée (page d'accueil)")
    return render_template('index.html')

@app.route('/capteurs', endpoint='capteurs')
def route_capteurs():
    """
    Page des capteurs/actionneurs (templates/capteurs.html)
    Endpoint nommé 'capteurs' => url_for('capteurs')
    """
    logging.info("Route '/capteurs' appelée (page capteurs)")
    return render_template('capteurs.html')

@app.route('/configuration', endpoint='configuration')
def route_configuration():
    """
    Page de configuration (templates/configuration.html)
    Endpoint nommé 'configuration' => url_for('configuration')
    """
    logging.info("Route '/configuration' appelée (page configuration)")
    return render_template('configuration.html')

@app.route('/economies', endpoint='economies')
def route_economies():
    """
    Page des économies réalisées (templates/economies.html)
    Endpoint nommé 'economies' => url_for('economies')
    """
    logging.info("Route '/economies' appelée (page économies)")
    return render_template('economies.html')

@app.route('/consommation', endpoint='consommation')
def route_consommation():
    """
    Page de consommation (templates/consommation.html)
    Endpoint nommé 'consommation' => url_for('consommation')
    """
    logging.info("Route '/consommation' appelée (page consommation)")
    return render_template('consommation.html')

# =======================================================
# Exemple d'endpoint pour un éventuel /api/user/config
# =======================================================
@app.route('/api/user/config', methods=['POST'], endpoint='user_config')
def user_config():
    """
    Reçoit {username, email} pour configurer un utilisateur (exemple).
    """
    logging.info("Route '/api/user/config' appelée (POST)")
    data = request.get_json()
    if not data:
        return jsonify({"error": "Aucune donnée transmise"}), 400

    username = data.get('username')
    email = data.get('email')
    logging.debug(f"Données reçues user config : {data}")

    # Exemple minimal (pas de stockage en BDD)
    return jsonify({"message": f"Paramètres utilisateur reçus : {username} / {email}"}), 200

# =======================================================
# Routes HTML "existant" : Logements, Pièces, Mesures...
# =======================================================
# Route API pour obtenir tous les logements (JSON)
@app.route('/api/logements', methods=['GET'])
def get_logements():
    logging.info("Route '/api/logements' (GET) - Récupération des logements en JSON")
    conn = get_db_connection()
    logements = conn.execute('SELECT * FROM Logements').fetchall()
    conn.close()

    logements_list = []
    for logement in logements:
        logements_list.append({
            'id_logement': logement['id_logement'],
            'adresse': logement['adresse'],
            'numero_telephone': logement['numero_telephone'],
            'adresse_ip': logement['adresse_ip'],
            'date_insertion': logement['date_insertion']
        })

    return jsonify(logements_list), 200

# Route API pour ajouter un logement (JSON)
@app.route('/api/logements', methods=['POST'])
def add_logement():
    """
    Ajoute un nouveau logement dans la base de données, format JSON.
    """
    logging.info("Route '/api/logements' (POST) - Ajout d'un nouveau logement")
    new_logement = request.get_json()
    logging.debug(f"Données reçues : {new_logement}")

    # Validation des données
    required_fields = ['adresse', 'numero_telephone', 'adresse_ip']
    if not new_logement or not all(field in new_logement for field in required_fields):
        logging.error("Champs manquants dans les données reçues")
        return jsonify({'error': 'Champs requis : adresse, numero_telephone, adresse_ip'}), 400

    adresse = new_logement['adresse']
    numero_telephone = new_logement['numero_telephone']
    adresse_ip = new_logement['adresse_ip']

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Logements (adresse, numero_telephone, adresse_ip) VALUES (?, ?, ?)',
            (adresse, numero_telephone, adresse_ip)
        )
        conn.commit()
        conn.close()
        logging.info("Logement ajouté avec succès")
        return jsonify({'message': 'Logement ajouté avec succès!'}), 201
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout du logement : {e}")
        return jsonify({'error': 'Erreur lors de l\'ajout du logement.'}), 500

# Route API pour supprimer un logement (JSON)
@app.route('/api/logements/<int:logement_id>', methods=['DELETE'])
def delete_logement(logement_id):
    """
    Supprime un logement de la base de données.
    """
    logging.info(f"Route '/api/logements/{logement_id}' (DELETE) - Suppression du logement")

    conn = get_db_connection()
    logement = conn.execute('SELECT * FROM Logements WHERE id_logement = ?', (logement_id,)).fetchone()

    if logement is None:
        conn.close()
        logging.error("Logement non trouvé")
        return jsonify({'error': 'Logement non trouvé.'}), 404

    try:
        conn.execute('DELETE FROM Logements WHERE id_logement = ?', (logement_id,))
        conn.commit()
        conn.close()
        logging.info("Logement supprimé avec succès")
        return jsonify({'message': 'Logement supprimé avec succès!'}), 200
    except Exception as e:
        conn.close()
        logging.error(f"Erreur lors de la suppression du logement : {e}")
        return jsonify({'error': 'Erreur lors de la suppression du logement.'}), 500

# Route existante pour afficher les logements en HTML (peut être conservée)
@app.route('/logements', methods=['GET'])
def get_logements_html():
    """
    Affiche tous les logements sous forme de tableau HTML.
    """
    logging.info("Route '/logements' (GET) - génération HTML directe")
    conn = get_db_connection()
    logements = conn.execute('SELECT * FROM Logements').fetchall()
    conn.close()

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liste des Logements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0; padding: 0;
                background-color: #f4f4f9;
            }
            h1 {
                text-align: center; margin: 20px 0; color: #333;
            }
            table {
                width: 80%; margin: 20px auto; border-collapse: collapse;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #fff;
            }
            th, td {
                border: 1px solid #ccc; padding: 12px; text-align: center;
            }
            th {
                background-color: #f9f9f9; font-weight: bold; color: #555;
            }
            tr:nth-child(even) { background-color: #f3f3f3; }
            tr:hover { background-color: #f1f1f1; }
            caption { font-size: 1.2em; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>Liste des Logements</h1>
        <table>
            <caption>Informations sur les logements</caption>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Adresse</th>
                    <th>Nombre de Pièces</th>
                    <th>Propriétaire</th>
                    <th>Date d'Insertion</th>
                </tr>
            </thead>
            <tbody>
    """

    for logement in logements:
        html_content += f"""
            <tr>
                <td>{logement['id_logement']}</td>
                <td>{logement['nom']}</td>
                <td>{logement['adresse']}</td>
                <td>{logement['nombre_de_pieces']}</td>
                <td>{logement['proprietaire']}</td>
                <td>{logement['date_insertion']}</td>
            </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    return html_content
@app.route('/pieces', methods=['GET'])
def get_pieces_html():
    """
    Affiche toutes les pièces sous forme de tableau HTML.
    """
    logging.info("Route '/pieces' (GET)")
    conn = get_db_connection()
    pieces = conn.execute('SELECT * FROM Pieces').fetchall()
    conn.close()

    html_content = """<!DOCTYPE html><html><head><title>Liste des Pièces</title> ..."""
    # ...
    return html_content

@app.route('/pieces', methods=['POST'])
def add_piece():
    """
    Ajoute une pièce à un logement existant (JSON).
    """
    logging.info("Route '/pieces' (POST)")
    new_piece = request.get_json()
    logging.debug(f"Données reçues : {new_piece}")

    if not new_piece or 'nom_piece' not in new_piece or 'x_coord' not in new_piece or 'y_coord' not in new_piece or 'z_coord' not in new_piece or 'id_logement' not in new_piece:
        logging.error("Champs manquants dans les données reçues")
        return jsonify({'error': 'Champs requis : nom_piece, x_coord, y_coord, z_coord, id_logement'}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Pieces (nom_piece, x_coord, y_coord, z_coord, id_logement) VALUES (?, ?, ?, ?, ?)',
        (new_piece['nom_piece'], new_piece['x_coord'], new_piece['y_coord'],
         new_piece['z_coord'], new_piece['id_logement'])
    )
    conn.commit()
    conn.close()
    logging.info("Pièce ajoutée avec succès")
    return jsonify({'message': 'Pièce ajoutée avec succès!'}), 201

@app.route('/api/mesures/actions', methods=['GET'])
def get_mesures_actions():
    """
    Retourne toutes les mesures ET l'action LED (allumée/éteinte) pour chaque mesure.
    """
    conn = get_db_connection()
    mesures = conn.execute('''
        SELECT 
            m.id_mesure,
            m.id_capt_act,
            m.valeur,
            m.date_insertion,
            CASE
                WHEN m.valeur > 25 THEN 'LED allumée'
                ELSE 'LED éteinte'
            END AS action
        FROM Mesures m
        ORDER BY m.date_insertion DESC
    ''').fetchall()
    conn.close()

    result = []
    for row in mesures:
        result.append({
            "id_mesure": row["id_mesure"],
            "id_capt_act": row["id_capt_act"],
            "valeur": row["valeur"],
            "date_insertion": row["date_insertion"],
            "action": row["action"]
        })
    return jsonify(result), 200

@app.route('/mesures', methods=['POST'])
def add_mesure():
    """
    Ajoute une mesure pour un capteur/actionneur spécifique (JSON).
    """
    logging.info("Route '/mesures' (POST)")
    new_mesure = request.get_json()
    logging.debug(f"Données reçues : {new_mesure}")

    if not new_mesure or 'id_capt_act' not in new_mesure or 'valeur' not in new_mesure:
        logging.error("Champs manquants")
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
# Factures + Graphique PieChart (HTML)
# =======================================================
@app.route('/factures/piechart', methods=['GET'])
def factures_piechart():
    """
    Génère une page HTML affichant un camembert Google Charts (montants des factures).
    """
    logging.info("Route '/factures/piechart' (GET)")

    conn = get_db_connection()
    factures = conn.execute('SELECT type, SUM(montant) as total FROM Factures GROUP BY type').fetchall()
    conn.close()

    if not factures:
        return """
        <!DOCTYPE html>
        <html><head><title>Répartition des Factures</title></head>
        <body>
            <h1>Aucune facture disponible</h1>
            <p>Veuillez insérer des factures dans la base.</p>
        </body>
        </html>
        """

    facture_data = [['Type de facture', 'Montant total']]
    facture_data += [[f['type'], f['total']] for f in factures]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Répartition des Factures</title>
        <script src="https://www.gstatic.com/charts/loader.js"></script>
        <script>
            google.charts.load('current', {{'packages':['corechart']}});
            google.charts.setOnLoadCallback(drawChart);
            function drawChart() {{
                var data = google.visualization.arrayToDataTable({facture_data});
                var options = {{
                    title: 'Répartition des Montants des Factures',
                    is3D: true,
                    width: 800,
                    height: 600,
                    pieSliceText: 'percentage',
                    legend: {{ position: 'right' }}
                }};
                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }}
        </script>
    </head>
    <body>
        <h1>Répartition des Montants des Factures</h1>
        <div id="piechart"></div>
    </body>
    </html>
    """
    return html_content

# =======================================================
# Météo (HTML)
# =======================================================
@app.route('/meteo/<city>', methods=['GET'])
def get_weather_forecast_as_table_in_french(city):
    """
    Récupère les prévisions météo (5 jours) et affiche un tableau HTML en français.
    """
    logging.info(f"Route '/meteo/{city}' appelée (GET)")

    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'cnt': 40
    }

    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

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

        daily_forecast = {}
        for entry in weather_data['list']:
            date = entry['dt_txt'].split(' ')[0]
            if date not in daily_forecast:
                daily_forecast[date] = []
            descr = translation.get(entry['weather'][0]['description'], entry['weather'][0]['description'])
            daily_forecast[date].append({
                'time': entry['dt_txt'].split(' ')[1],
                'temperature': entry['main']['temp'],
                'description': descr,
                'humidity': entry['main']['humidity']
            })

        html_content = f"""
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
            <h1>Prévisions météo pour {city.capitalize()}</h1>
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
        """

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

        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        return html_content

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            logging.error("Clé API invalide ou permissions manquantes.")
            return jsonify({'error': 'Clé API invalide ou permissions manquantes.'}), 401
        elif response.status_code == 404:
            logging.error(f"Ville non trouvée : {city}")
            return jsonify({'error': f"Ville '{city}' introuvable."}), 404
        else:
            logging.error(f"Erreur HTTP lors de la requête API : {e}")
            return jsonify({'error': 'Erreur lors de la récupération des données météo.'}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête API : {e}")
        return jsonify({'error': 'Impossible de récupérer les données météo.'}), 500

# =======================================================
# Simulation des données capteurs & actions
# =======================================================
def simuler_capteurs_et_actions():
    """
    Insère régulièrement des mesures simulées (température).
    Vérifie si la température dépasse TEMP_SEUIL.
    """
    logging.info("Simulation des données des capteurs et vérification des actions")
    conn = get_db_connection()

    id_capt_act = 1
    valeur_simulee = random.uniform(20.0, 35.0)
    conn.execute(
        'INSERT INTO Mesures (id_capt_act, valeur, date_insertion) VALUES (?, ?, datetime("now"))',
        (id_capt_act, valeur_simulee)
    )
    conn.commit()
    logging.info(f"Mesure simulée insérée : Capteur {id_capt_act}, Température = {valeur_simulee:.2f} °C")

    if valeur_simulee > TEMP_SEUIL:
        logging.info(f"Température {valeur_simulee:.2f} °C > seuil {TEMP_SEUIL} °C => LED ALLUMÉE.")
    else:
        logging.info(f"Température {valeur_simulee:.2f} °C <= seuil {TEMP_SEUIL} °C => LED ÉTEINTE.")

    conn.close()
    # Relance la simulation après 10 secondes
    Timer(10, simuler_capteurs_et_actions).start()

@app.route('/mesures/actions', methods=['GET'])
def afficher_mesures_et_actions():
    """
    Affiche les mesures récentes + action LED sous forme HTML
    (limitées aux 20 dernières lignes).
    """
    logging.info("Route '/mesures/actions' (GET)")
    conn = get_db_connection()

    # On ajoute "LIMIT 20" pour n'afficher que 20 mesures
    mesures = conn.execute('''
        SELECT
            m.id_mesure,
            m.id_capt_act,
            m.valeur,
            m.date_insertion,
            CASE WHEN m.valeur > ? THEN 'LED allumée' ELSE 'LED éteinte' END AS action
        FROM Mesures m
        ORDER BY m.date_insertion DESC
        LIMIT 20
    ''', (TEMP_SEUIL,)).fetchall()

    conn.close()

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
      <h1>Mesures et Actions (20 dernières)</h1>
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
# API Consommation (JSON) : /api/consommation
# =======================================================
@app.route('/api/consommation', methods=['GET'])
def get_consommation():
    """
    Retourne les consommations (ex. électricité, eau, déchets) en JSON.
    """
    logging.info("Route '/api/consommation' (GET)")
    try:
        conn = get_db_connection()
        consommations = conn.execute('''
            SELECT type, SUM(consommation) as total
            FROM Factures
            GROUP BY type
        ''').fetchall()
        conn.close()

        # Ex. [{"type": "electricite", "total": 2500}, {"type": "eau", "total": 800}, ...]
        consommation_data = [{'type': row['type'], 'total': row['total']} for row in consommations]
        logging.debug(f"Données consommation renvoyées : {consommation_data}")
        return jsonify(consommation_data)

    except sqlite3.Error as e:
        logging.error(f"Erreur SQLite : {e}")
        return jsonify({'error': 'Erreur lors de la récupération des données de consommation.'}), 500

# =======================================================
# API Capteurs (JSON) : /api/capteurs
# =======================================================
@app.route('/api/capteurs', methods=['GET'])
def get_capteurs():
    """
    20 derniers capteurs : ORDER BY id DESC LIMIT 20
    """
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT *
        FROM Capteurs_Actionneurs
        ORDER BY id_capt_act DESC
        LIMIT 20
    ''').fetchall()
    conn.close()

    capteurs_list = []
    for row in rows:
        capteurs_list.append({
            "id": row["id_capt_act"],
            "type": row["type"],
            "port_communication": row["port_communication"],
            "reference_commerciale": row["reference_commerciale"]
        })
    return jsonify(capteurs_list), 200
@app.route('/api/capteurs', methods=['POST'])
def add_capteur():
    new_capteur = request.get_json()
    # On inclut "id_piece" dans la liste des champs obligatoires
    required = ["type", "port_communication", "reference_commerciale", "id_piece"]
    if not new_capteur or not all(k in new_capteur for k in required):
        return jsonify({'error': f"Champs requis : {required}"}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Capteurs_Actionneurs
        (type, port_communication, reference_commerciale, id_piece)
        VALUES (?, ?, ?, ?)
    ''', (
        new_capteur["type"],
        new_capteur["port_communication"],
        new_capteur["reference_commerciale"],
        new_capteur["id_piece"]
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Capteur ajouté avec succès!'}), 201

@app.route('/api/capteurs/<int:id>', methods=['DELETE'])
def delete_capteur(id):
    conn = get_db_connection()
    result = conn.execute('DELETE FROM Capteurs_Actionneurs WHERE id_capt_act = ?', (id,))
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({'error': 'Capteur non trouvé'}), 404
    return jsonify({'message': 'Capteur supprimé avec succès!'}), 200


# =======================================================
# API Économies : /api/economies
# =======================================================
@app.route('/api/economies', methods=['GET'])
def get_economies():
    """
    Retourne les économies selon l'échelle de temps (mensuel, annuel...).
    """
    scale = request.args.get('scale', 'monthly')
    conn = get_db_connection()

    if scale == 'monthly':
        query = """
        SELECT 
            strftime('%Y-%m', date_facture) as type,
            SUM(montant) as economie
        FROM Factures
        GROUP BY strftime('%Y-%m', date_facture)
        ORDER BY strftime('%Y-%m', date_facture)
        """
    elif scale == 'yearly':
        query = """
        SELECT
            strftime('%Y', date_facture) as type,
            SUM(montant) as economie
        FROM Factures
        GROUP BY strftime('%Y', date_facture)
        ORDER BY strftime('%Y', date_facture)
        """
    else:
        query = """
        SELECT
            type,
            SUM(montant) as economie
        FROM Factures
        GROUP BY type
        """

    rows = conn.execute(query).fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "type": r["type"],
            "economie": r["economie"]
        })
    return jsonify(data)

@app.route('/meteo', endpoint='meteo')
def route_meteo():
    """
    Page météo (templates/meteo.html).
    L'utilisateur pourra taper une ville, faire un fetch ou
    un simple <form> pour aller sur /meteo/<city>.
    """
    logging.info("Route '/meteo' appelée (page meteo)")
    return render_template('meteo.html')


# =======================================================
# Lancement de l’application
# =======================================================
if __name__ == '__main__':
    logging.info("Démarrage du serveur Flask et simulation des capteurs")
    simuler_capteurs_et_actions()  # Lance la boucle de simulation
    app.run(debug=True)

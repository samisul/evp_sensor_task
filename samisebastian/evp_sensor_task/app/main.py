# coding=utf-8
# Importieren der benötigten Module: Flask, jsonify, render_template, mysql.connector, signal, sys und CORS
from flask import Flask, jsonify, render_template
import mysql.connector
import signal
import sys
from flask_cors import CORS

# Definitieren einer Funktion zum Schließen der MySQL-Verbindung bei Programmende
def close_connection(signal, frame):
    # Schließe die MySQL-Verbindung
    db.close()
    print("MySQL connection closed.")
    sys.exit(0)

# Registrieren des Signalhandlers für das Beenden des Programms
signal.signal(signal.SIGINT, close_connection)
signal.signal(signal.SIGTERM, close_connection)

# Definieren einer Datenklasse DataObject zur Strukturierung der Daten
class DataObject:
    def __init__(self, id, temperature, humidity, co2, dust):
        self.id = id
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.dust = dust

# Instanziieren der Flask-Anwendung
app = Flask(__name__)
# Aktivieren von CORS (Cross-Origin Resource Sharing) für die Flask-Anwendung
CORS(app)

# Herstellen einer Verbindung zur MySQL-Datenbank
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ItTakesDedication_0915",
    database="sensor_data"
)

# Erstellen eines Cursor-Objekts für die Datenbankverbindung
cursor = db.cursor()

# Definieren des ersten API-Endpunkts: '/api/data'
# Zugriffsmethode: GET
@app.route('/api/data', methods=['GET'])
# Ausführen der Funktion get_data()
def get_data():
    # Festlegen der SQL-Abfrage
    query = "SELECT color FROM data ORDER BY timeIndex LIMIT 1"
    # Ausführen der SQL-Abfrage
    cursor.execute(query)
    # Abrufen aller zurückgegebenen Zeilen
    rows = cursor.fetchall()
    # Erstellen einer Liste von DataObject-Instanzen
    data_objects = []
    # Über die zurückgegebenen Zeilen iterieren und Erstellen von DataObject-Instanzen
    for row in rows:
        data_objects.append(row)
    # Ausgebeben der ersten DataObject-Instanz
    print(data_objects[0])
    # Rückgabe der Daten im JSON-Format
    return jsonify(data_objects)

# Definieren des zweiten API-Endpunkts: '/'
# Zugriffsmethode: GET
@app.route('/')
# Ausführen der Funktion index()
def index():
    # Rückgabe einer HTML-Vorlage
    return render_template('index.html')

# Starten der Flask-Anwendung
if __name__ == '__main__':
    app.run()

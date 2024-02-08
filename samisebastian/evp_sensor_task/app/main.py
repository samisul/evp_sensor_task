# coding=utf-8
# Hier importieren wir das Flask-Framework 'flask', sowie 'jsonify' und 'render_template'
from flask import Flask, jsonify, render_template
import mysql.connector
import signal
import sys
from flask_cors import CORS


def close_connection(signal, frame):
    # Close MySQL connection
    db.close()
    print("MySQL connection closed.")
    sys.exit(0)


# Register signal handler for shutdown
signal.signal(signal.SIGINT, close_connection)
signal.signal(signal.SIGTERM, close_connection)


class DataObject:
    def __init__(self, id, temperature, humidity, co2, dust):
        self.id = id
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.dust = dust


# Hier wird die Flask-Anwendung instanziiert
app = Flask(__name__)
CORS(app)

# Creating a connection object
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ItTakesDedication_0915",
    database="sensor_data"
)

cursor = db.cursor()

# Definiere ersten API-Endpunkt:
# Wenn per GET Methode aufgerufen


@app.route('/api/data', methods=['GET'])
# Wird get_data() ausgeführt
def get_data():
    # Hier werden die zurückgegebenen Daten festgelegt
    query = "SELECT color FROM data ORDER BY timeIndex LIMIT 1"
    # Execute the query
    cursor.execute(query)

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()

    # Create a list of DataObject instances
    data_objects = []

    # Iterate over the rows and create DataObject instances
    for row in rows:
        data_objects.append(row)

    print(data_objects[0])
    return jsonify(data_objects)

# Definiere zweiten API-Endpunkt, die 'Hauptseite'


@app.route('/')
# Wird index() ausgeführt
def index():
    # Gibt eine HTML-Vorlage zurück
    return render_template('index.html')


# Starten der Anwendung
if __name__ == '__main__':
    app.run()

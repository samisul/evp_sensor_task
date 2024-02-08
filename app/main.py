# Hier importieren wir das Flask-Framework 'flask', sowie 'jsonify' und 'render_template'
from flask import Flask, jsonify, render_template

# Hier wird die Flask-Anwendung instanziiert
app = Flask(__name__)

# Definiere ersten API-Endpunkt:
# Wenn per GET Methode aufgerufen


@app.route('/api/data', methods=['GET'])
# Wird get_data() ausgeführt
def get_data():
    # Hier werden die zurückgegebenen Daten festgelegt
    data = {'message': 'Hello, World!'}

    # Alles wird als JSON-Datei zurückgegeben
    return jsonify(data)

# Definiere zweiten API-Endpunkt, die 'Hauptseite'


@app.route('/')
# Wird index() ausgeführt
def index():
    # Gibt eine HTML-Vorlage zurück
    return render_template('index.html')


# Starten der Anwendung
if __name__ == '__main__':
    app.run()

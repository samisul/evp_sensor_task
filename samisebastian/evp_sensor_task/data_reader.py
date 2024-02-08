# Hier werden sämtliche Bibliotheken und Frameworks importiert, die für den Code benötigt werden; zum Beispiel Serial für die serielle Verbindung, GPIO für die Pinsteuerung, MySQL für die Datenbankverbindung...
import serial
import bme680
import time
import mysql.connector
import ast
import RPi.GPIO as GPIO
import subprocess


# Hier wird die Pinnummerierung festgelegt 
GPIO.setmode(GPIO.BCM)
# Aufsetzen der GPIO Pins 5, 6 und 13 des PIs 
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


# Erstellen einer Funktion zur Reduktion von Redundanz
def switch_lights(red, yellow, green):
    # Übergeben des Parameters als Befehl an den jeweiligen Pin
    GPIO.output(13, red)
    GPIO.output(5, yellow)
    GPIO.output(6, green)

# Hier wird die Funktion definiert, welche die physische Ampel mit den Sensorwerten synchronisiert
def sync_lights_with_sensor_values():
    if dust >= 91 or obj.co2 >= 1501:
        # Rote LED leuchtet: PM 91-250+ und CO2 1501-30k+
        switch_lights(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
        return 'red'
    elif dust >= 31 or obj.co2 >= 451:
        # Gelbe LED leuchtet: PM 31-90 und CO2 451-1500
        switch_lights(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        return 'yellow'
    elif dust <= 30 or obj.co2 <= 450:
        # Grüne LED leuchtet: PM 0-30 und CO2 350-450
        switch_lights(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        return 'green'


# Erzeugen des MySQL-Verbindungsobjektes
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ItTakesDedication_0915",
    database="sensor_data"
)

# Erzeugen des Cursor-Objektes
cursor = db.cursor()


# Öffnen der Seriellen Kommunikation, um Daten vom Arduino abrufen zu können
arduino = serial.Serial('/dev/ttyUSB0', 9600)


# Dieser Codeabschnitt initialisiert einen Sensor (BME680) und führt dann einige Konfigurationsschritte aus.
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
# Iteriere über die Eigenschaften des Kalibrierungsdatenobjekts des Sensors.
for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))


# Konfigurieren der Einstellungen des Sensors.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


# Deklarieren einer Variablen
command = "sudo python -m mh_z19"


# Dieser Codeausschnitt erfasst kontinuierlich Sensordaten und speichert diese in einer Datenbank
try:
    while True:
         # Überprüft, ob Sensor-Daten verfügbar sind
        if sensor.get_sensor_data():
            # Daten werden vom Arduino abgerufen und verarbeitet
            dust = float(arduino.readline().decode().strip())
            # Führt ein Shell-Kommando aus und speichert dessen Ausgabe 
            output = subprocess.check_output(command, shell=True)
            # Dekodiert die Ausgabe und entfernt Leerzeichen
            output = output.decode()
            string = output.strip("'")
            # Wandle den String in ein Python-Dictionary um
            dictionary = ast.literal_eval(string)
            # Erstellt ein Objekt aus dem Python-Dictionary
            obj = type('Object', (object,), dictionary)()
            # Synchronisiert Lichtfarben mit den Sensorwerten und erhalte die Farbwerte
            colorValue = sync_lights_with_sensor_values()
            # Diese SQL-Query lädt die gesammelten Daten in die Datenbank
            cursor.execute(f"""
                            INSERT INTO data (temperature, humidity, dust, co2, color)
                            VALUES ({sensor.data.temperature}, {sensor.data.humidity}, {dust}, {obj.co2}, '{colorValue}');""")
            # Übermitteln der SQL-Query
            db.commit()
            # Wartet zehn Sekunden
            time.sleep(10)

# Falls per Tastatureingabe "STRG + C" gedrückt wird  
except KeyboardInterrupt:
    # Werden die GPIO Zuweisungen bereinigt
    GPIO.cleanup()
    pass
# Die Arduino Verbindung wird genau wie die Datenbankverbindung geschlossen 
arduino.close()
db.close()

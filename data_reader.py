# Hier werden sämtliche Bibliotheken und Frameworks importiert, die für den Code benötigt werden. 
# Zum Beispiel Serial für die serielle Verbindung, 'bme680' um  das entsprechende Bauteil verwenden zu können, 'ast' zur Auswertung von Zeichenketten in Python Objekte,
# GPIO für die Pinsteuerung...
import serial
import bme680
import time
import mysql.connector
import ast
import RPi.GPIO as GPIO
import subprocess

# Hier wird die Ampelsteuerungsfunktion erschaffen
def switch_lights(red, yellow, green):
    GPIO.output(13, red)
    GPIO.output(5, yellow)
    GPIO.output(6, green)

# Ampelkontrollstruktur
def sync_lights_with_sensor_values():
    # Wenn der Feinstaubwert zwischen 91-250µg/m³ der Co2-Wert zwischen 1501-30kppm sowie darüber liegt, leuchtet sie rot
    if dust >= 91 or obj.co2 >= 1501: 
        switch_lights(GPIO.HIGH, GPIO.LOW, GPIO.LOW) 
        print('ROT')
    # Bei 31-90µg/m³ und 451-1500ppm leuchtet die Ampel gelb
    elif dust >= 31 or obj.co2 >= 451: 
        switch_lights(GPIO.LOW, GPIO.HIGH, GPIO.LOW) 
        print('GELB')
    # Bei 0-30µg/m³ und 350-450ppm leuchtet die Ampel grün
    elif dust <= 30 or obj.co2 <= 450: 
        switch_lights(GPIO.LOW, GPIO.LOW, GPIO.HIGH) 
        print('GRÜN')

#Hier wird der GPIO-Modus sowie die einzelnen benutzten GPIO-Pins festgelegt
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
  
# Hier wird die SQL Verbindung als Objekt instanziiert
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="samisebastian",
    database="sensor_data"
)

# Erstellen eines Cursor-Objektes für SQL-Abfragen
cursor = db.cursor()

# Aufbauen der seriellen Verbindung zum Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your Arduino's serial port

# Initialisieren des BME680 Sensors
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):	
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Auslesen und Ausgeben der Kalibrierungsdaten
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# Konfigurieren des BME680 Sensors
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)          
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Command to be executed
command = "sudo python -m mh_z19"

# Hier befindet sich nun die Hauptschleife des Programms, in welcher kontinuierlich in einem zehnsekündigen Rythmus an die Datenbank sendet
try:
    while True:
        if sensor.get_sensor_data():
            dust = float(arduino.readline().decode().strip())
            output = subprocess.check_output(command, shell=True)
            output = output.decode()
            string = output.strip("'")
            dictionary = ast.literal_eval(string)
            obj = type('Object', (object,), dictionary)()
            # Die Lichter werden mit den Daten synchronisiert
            sync_lights_with_sensor_values()
            # Der Loop wird auf zehn Sekunden getimed 
            time.sleep(10)

            # Sendet sämtliche wichtigen Sensordaten an die Datenbank 
            cursor.execute(f"""
                            INSERT INTO data (temperature, humidity, dust, co2)
                            VALUES ({sensor.data.temperature}, {sensor.data.humidity}, {dust}, {obj.co2});""")
            db.commit()

# Sobald STRG + C gedrückt wird, bricht das Programm ab
except KeyboardInterrupt:
    GPIO.cleanup()
    pass

# Schließen der Arduino- und Datenbankverbindung
arduino.close()
db.close()
    

# Hier werden sämtliche Bibliotheken und Frameworks importiert, die für den Code benötigt werden. Zum Beispiel Serial für die serielle Verbindung, [...] des Sensors 'bme680'
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


# Green: PM 0-30 und CO2 350-450
# Yellow: PM 31-90 und CO2 451-1500
# Red: PM 91-250+ und CO2 1501-30k+

def sync_lights_with_sensor_values():
    if dust >= 91 or obj.co2 >= 1501:
        switch_lights(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
        print('ROT')
        return 'red'
    elif dust >= 31 or obj.co2 >= 451:
        switch_lights(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        print('GELB')
        return 'yellow'
    elif dust <= 30 or obj.co2 <= 450:
        switch_lights(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        print('GRÜN')
        return 'green'


GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


# Creating a connection object
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ItTakesDedication_0915",
    database="sensor_data"
)

cursor = db.cursor()

# Open the serial port connection
# Replace '/dev/ttyUSB0' with your Arduino's serial port
arduino = serial.Serial('/dev/ttyUSB0', 9600)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

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

try:
    while True:
        if sensor.get_sensor_data():
            dust = float(arduino.readline().decode().strip())
            output = subprocess.check_output(command, shell=True)
            output = output.decode()
            string = output.strip("'")
            dictionary = ast.literal_eval(string)
            obj = type('Object', (object,), dictionary)()

            print(obj.co2)

            colorValue = sync_lights_with_sensor_values()
            print(colorValue)
            cursor.execute(f"""
                            INSERT INTO data (temperature, humidity, dust, co2, color)
                            VALUES ({sensor.data.temperature}, {sensor.data.humidity}, {dust}, {obj.co2}, '{colorValue}');""")
            db.commit()

            time.sleep(10)

except KeyboardInterrupt:
    GPIO.cleanup()
    pass

arduino.close()
db.close()

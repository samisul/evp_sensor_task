// Bei diesem Code handelt es sich um das Codebeispiel vom Hersteller, zu finden im herunterladbaren Datenblatt unter: "https://joy-it.net/de/products/SEN-GP2Y1014AU", stand 30.01.2024.
// Bis auf eine Wertumrechnung  von mg in µg ist dieses Codebeispiel unverändert.

int ledPower = 2;
double dustDensity;
int sensorValue;
double voltage;

// the setup routine runs once when you press reset:
void setup() {
    // initialize serial communication at 9600 bits per second:
    Serial.begin(9600);
    // set LED pin as output
    pinMode(ledPower,OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
    // set the LED pin low
    digitalWrite(ledPower,LOW);

    delayMicroseconds(180); // delay about 180us
    // read the analog pin
    sensorValue = analogRead(A1); // needs about 100 us
    delayMicroseconds(30);    //delay about 30 us

    // set the LED pin high
    digitalWrite(ledPower,HIGH);
    delayMicroseconds(9680);  // filling out the rest of the pulse cycle

    // Convert analog value to voltage
    voltage = sensorValue * (5.0 / 1023.0);
  
    // calculate dust density
    if (voltage <= 0.9) dustDensity = 0.0;
    if (voltage < 3.5 && voltage > 0.9) dustDensity = -0.0127*pow(voltage, 2.0) + 0.2225*voltage - 0.1819;
    if (voltage >= 3.5) dustDensity = 40.0*pow(voltage, 2.0) - 280.8*voltage + 493.28;
    if (dustDensity >= 0.8) dustDensity = 0.8;

    // print the measured and calculated data
    // Hier findet die Umrechnung mg in µg statt
    Serial.println(dustDensity * 1000);

    delay(1000);
}

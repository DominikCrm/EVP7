import time, adafruit_dht, board, RPi.GPIO as gpio, paho.mqtt.client as mqtt

# GPIO Initialisierung
gpio.setmode(gpio.BCM)  # Setze den Modus des GPIO-Pins auf BCM
gpio.setup(22, gpio.OUT)  # Konfiguriere Pin 22 als Ausgang für den Servo

# Initialisiere Servo
servo = gpio.PWM(22, 350)  # Erstelle ein PWM-Objekt für Pin 22 mit einer Frequenz von 350 Hz
servo.start(0)  # Starte den Servo mit einer Anfangsposition von 0

# Initialisiere den DHT22-Sensor
dht_device = adafruit_dht.DHT22(board.D5, use_pulseio=False)  # Erstelle ein DHT22-Objekt an Pin D5

# MQTT-Parameter
TOPIC = "home/pi/14/sensordata"  # Das MQTT-Thema, unter dem die Sensorwerte veröffentlicht werden
BROKER_ADRESS = "localhost"  # Die IP-Adresse des MQTT-Brokers (hier lokal, kann sich ändern)
PORT = 1883  # Der Port des MQTT-Brokers

# Callback-Funktion, die aufgerufen wird, wenn eine Nachricht vom Broker empfangen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))  # Nachricht von Bytes in String umwandeln
    print(f"Nachricht empfangen: {msg}")
    # Hier fehlt eine Bedingung oder eine Aktion, die bei Empfang einer Nachricht ausgeführt werden soll

# Callback-Funktion, die aufgerufen wird, wenn eine Verbindung zum Broker hergestellt wird
def on_connect(client, userdata, flags, rc):
    print(f"Mit Broker ({BROKER_ADRESS}) verbunden")
    client.subscribe(TOPIC)  # Abonnement für das angegebene Thema

# Hauptfunktionsdefinition
def main():
    if __name__ == "__main__":
        client = mqtt.Client()  # Erstelle ein MQTT-Client-Objekt
        client.on_connect = on_connect  # Setze die Verbindungsrückruffunktion
        client.on_message = on_message  # Setze die Nachrichtenrückruffunktion
        client.connect(BROKER_ADRESS, PORT)  # Verbinde mit dem MQTT-Broker
        client.loop_forever()  # Starte die Schleife zur kontinuierlichen Nachrichtenverarbeitung

# Hauptfunktionsaufruf
main()

import time, adafruit_dht, board, RPi.GPIO as gpio, paho.mqtt.client as mqtt, sys

# GPIO Initialisierung
gpio.setmode(gpio.BCM)  # Setze den Modus des GPIO-Pins auf BCM
gpio.setup(22, gpio.OUT)  # Konfiguriere Pin 22 als Ausgang für den Servo

# Initialisiere Servo
servo = gpio.PWM(22, 350)  # Erstelle ein PWM-Objekt für Pin 22 mit einer Frequenz von 350 Hz
servo.start(0)  # Starte den Servo mit einer Anfangsposition von 0

# Initialisiere den DHT22-Sensor
dht_device = adafruit_dht.DHT22(board.D5, use_pulseio=False)  # Erstelle ein DHT22-Objekt an Pin D5

# Konfiguriere MQTT-Parameter
TOPIC = "home/pi/14/sensordata"  # Das MQTT-Thema, unter dem die Sensorwerte veröffentlicht werden
BROKER_ADRESS = "172.17.0.102"  # Die IP-Adresse des MQTT-Brokers
PORT = 1883  # Der Port des MQTT-Brokers
QOS = 1  # Die Qualität des Dienstes für die MQTT-Nachrichten

def main():
    if __name__ == "__main__":
        # Verbindung zum MQTT-Broker herstellen
        client = mqtt.Client()  # Erstelle ein MQTT-Client-Objekt
        client.connect(BROKER_ADRESS, PORT)  # Verbinde mit dem MQTT-Broker
        print(f"Mit MQTT Broker ({BROKER_ADRESS}) verbunden")
        
        # Hauptprogrammschleife
        while True:
            try:
                # Sensorwerte abrufen
                temperature_c = dht_device.temperature  # Temperaturwert in Celsius
                humidity = dht_device.humidity  # Luftfeuchtigkeitswert in Prozent
                
                # Sensorwerte auf der Konsole anzeigen
                print("Temp:{:.1f} C    Luftfeuchtigkeit: {}%".format(temperature_c, humidity))
                
                # Sensorwerte über MQTT veröffentlichen
                client.publish(TOPIC, humidity, qos=QOS)  # Veröffentliche die Luftfeuchtigkeit unter dem angegebenen Topic (variable)
                
                # Kurze Pause, bevor die nächsten Sensorwerte abgerufen werden
                time.sleep(2)
            
            # Fehlerbehandlung
            except Exception as e:
                print("Fehler:", e)
                time.sleep(0.1)  # Kurze Pause, bevor der nächste Versuch unternommen wird

# Hauptfunktionsaufruf
main()

# GPIO aufräumen, nachdem das Hauptprogramm beendet wurde
gpio.cleanup()

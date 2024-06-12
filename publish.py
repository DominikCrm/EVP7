# Importieren verschiedener Bibliotheken zu Sicherung der Funktionalität
import time, adafruit_dht, board, RPi.GPIO as gpio, paho.mqtt.client as mqtt

# Festlegung der Pin Nummerierung / Hier: logische Nummerierung anhand der Namen auf dem Board (bspw GPIO24 für PIN 24)
gpio.setmode(gpio.BCM)
# Setup der Pinbelegung auf dem GPIO-Board (Für In- und Output) 
gpio.setup(22, gpio.OUT)

# Initialisierung des Motors und dessen Frequenz
servo = gpio.PWM(22, 350)
servo.start(0)

dht_device = adafruit_dht.DHT22(board.D5, use_pulseio=False)

TOPIC = "home/server/sensor2"
BROKER_ADRESS = "172.17.0.104"
PORT = 1883
QOS = 1

def main():
    if __name__ == "__main__":
        client = mqtt.Client()
        client.connect(BROKER_ADRESS, PORT)
        print(f"Mit MQTT Broker ({BROKER_ADRESS}) verbunden")
        while True:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            print("Temp:{:.1f} C    Luftfeuchtigkeit: {}%".format(temperature_c, humidity))
            client.publish(TOPIC, temperature_c, qos=QOS)
            time.sleep(2)

# Aufruf der main-Funktion   
main()

# Freigabe der GPIO Pins nach Programmende
gpio.cleanup()
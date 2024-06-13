import time, RPi.GPIO as gpio, paho.mqtt.client as mqtt

gpio.setmode(gpio.BCM)

pins = {
    "knopf": [23, "in", 0],
    "LED_ROT": [12, "out", "low"],
    "LED_GRUEN": [16, "out", "low"]
}

lampenstatus = {}
timediff = 0
max_timediff = 10
lampenstatus = "aus"

for pin in pins:
    if pins[pin][1].upper() == "OUT":
        gpio.setup(pins[pin][0], gpio.OUT)
        if pins[pin][2].upper() == "HIGH":
            gpio.output(pins[pin][0], gpio.HIGH)
        else:
            gpio.output(pins[pin][0], gpio.LOW)
    elif pins[pin][1].upper() == "IN":
        gpio.setup(pins[pin][0], gpio.IN)
    

TOPIC = "home/pi/14/sensordata"
BROKER_ADRESS = "localhost"
PORT = 1883

max_value = 20.0
start_value_button = gpio.input(pins["knopf"][0])
print(start_value_button)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print(f"Nachricht empfangen: {msg}")   
    
def on_connect(client, userdata, flag, rc):
    print(f"Mit Broker ({BROKER_ADRESS}) verbunden")
    client.subscribe(TOPIC)
    
def lampe_an(LED_PORT):
    global lampenstatus
    gpio.output(pins[LED_PORT][0], gpio.HIGH)
    print(f"{pins[LED_PORT][0]} ist an")
        
    
def lampe_aus(LED_PORT):
    global lampenstatus
    gpio.output(pins[LED_PORT][0], gpio.LOW)
    


def main():
    global lampenstatus, timediff, lampenstatus
    while True:
        __localtime = time.time()
        time.sleep(.01)
        if lampenstatus == "an":
            timediff += time.time() - __localtime
            if doorstatus == "offen":
                lampe_aus("LED_GRUEN")
                lampenstatus = "aus"
                lampe_an("LED_ROT")
        if gpio.input(pins["knopf"][0]) != start_value_button:
            lampe_an("LED_GRUEN")
            lampenstatus = "an"
        if timediff > 10:
            lampe_aus("LED_GRUEN")
            lampenstatus = "aus"

try:
    main()  
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    gpio.cleanup()
except Exception as error:
    print(error)
    gpio.cleanup()
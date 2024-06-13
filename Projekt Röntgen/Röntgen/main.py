import time, RPi.GPIO as gpio, paho.mqtt.client as mqtt, paho.mqtt.subscribe as subscribe, paho.mqtt.publish as publish

TOPIC = "bkgut/gruppe14/lampe"
HOST = "localhost"

pins = {
    "Knopf": [16, "IN", 0],
    "LED_ROT": [32, "OUT", "HIGH"],
    "LED_GRUEN": [36, "OUT", "LOW"],
}

door_status = "zu"
roentgen_timer = 10 #Sekunden

gpio.setmode(gpio.BOARD)

for pin in pins:
    if pins[pin][1] == "OUT":
        gpio.setup(pins[pin][0], gpio.OUT)
        if pins[pin][2] == "HIGH":
            gpio.output(pins[pin][0], True)
        else:
            gpio.output(pins[pin][0], False)
    else:
        gpio.setup(pins[pin][0], gpio.IN)
        

def input_status(input_number):
    return gpio.input(input_number) == 1
    
def main():
    while True:
        __starttime = time.time()
        time.sleep(.1)
        print(input_status(pins["Knopf"][0]))
        if input_status(pins["Knopf"][0]):
            publish.single(topic=TOPIC, payload="ON", hostname=HOST)
            gpio.output(pins["LED_ROT"][0], False)
            gpio.output(pins["LED_GRUEN"][0], True)
            while time.time() - __starttime < roentgen_timer and door_status == "zu":
                print(time.time() - __starttime)
            publish.single(topic=TOPIC, payload="OFF", hostname=HOST)
            gpio.output(pins["LED_ROT"][0], True)
            gpio.output(pins["LED_GRUEN"][0], False)
    print("Code ende")

main()
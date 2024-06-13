""" Skript für Projekt der Automatisierung der Sicherung der Tür
    Lehrer: Hr. Seibert
    Berufsschule: BK GuT
    Name, Organisation:         Anatolii Liebiediev, Regio iT 
                                Dominik Cremer, CANCOM
    Erstellt, Letzte Änderung:  01.02.2024
    """

import time, sys, RPi.GPIO as gpio

# Variablendeklaration für den Startzustand und den Cleanup am Ende des Programmes
cleanedup = False
is_day = True
day_night_time = 10 #Sekunden
timeraktiv = False
alarmaktiv = False
doorlocked = False
led_status = "gruen"

# Pin Belegung des GPIO Boards für leichtere Verwendung der PINs
Sensor = 17
Motor = 18
Button = 22
Buzzer = 23
LED_Gruen = 24
LED_Rot = 25

# Festlegung der Pin Nummerierung / Hier: logische Nummerierung anhand der Namen auf dem Board (bspw GPIO24 für PIN 24)
gpio.setmode(gpio.BCM) 

# Setup der Pinbelegung auf dem GPIO-Board (Für In- und Output)
gpio.setup(Sensor, gpio.IN)
gpio.setup(Motor, gpio.OUT)
gpio.setup(Button, gpio.IN, pull_up_down=gpio.PUD_UP) # Definierung eines Pull_Up Widerstandes für den input des Knopfes
gpio.setup(Buzzer, gpio.OUT)
gpio.setup(LED_Gruen, gpio.OUT)
gpio.setup(LED_Rot, gpio.OUT)

# Initialisierung des Motors und dessen Frequenz
servo = gpio.PWM(Motor, 350)
servo.start(0)

# Startwerte für Sensoren und Aktoren
reedstartnumber = 0 # Statischer Startwert des Sensors, dass keine Komplikationen oder Vertauschungen entstehen   
knopfstartnumber = gpio.input(Button) # Startwert des Knopfes dynamisch in einer Variable speichern

# Funktion, welche Prüft, ob der Knopf gedrückt wird
def knopf_gedrueckt(): 
    return gpio.input(Button) != knopfstartnumber

#True = Auf, False = Zu
def set_schlossstatus(status):
    global doorlocked # import der festgelegten Variable für den Zustand der Dachluke
    servo.ChangeDutyCycle(not status and 65 or 23) # Schließmechanismus für den Motor
    time.sleep(1) #Sicherheitsfenster
    servo.ChangeDutyCycle(0) # Verhindert Zucken des Motors nach einer Aktion
    doorlocked = status # Status der Variable "doorlocked" aktualisieren 

# Funktion für den Alarm
def alarm(alarmstatus):
    #print(f"Alarm: {alarmstatus}")
    global alarmaktiv, Buzzer # import der beiden relevanten globalen Variablen
    alarmaktiv = alarmstatus 
    if alarmstatus: # Prüfung des Alarmstatus (True oder False) und aktivierung des Buzzers je nach Fall
        gpio.output(Buzzer, gpio.HIGH) # Buzzer an
    else:
        gpio.output(Buzzer, gpio.LOW) # Buzzer aus

# Hauptfunktion für die Implementierung alles Funktionen 
def main():
    if __name__ == "__main__":
        global is_day, timeraktiv, led_status # import der relevanten globalen Variablen
        __localtimer = time.time() # Vergleich der Zeit für den Schließmechanismus
        set_schlossstatus(is_day) # Setzen des Schlossstatus auf Tag
        while True: #Endlosschleife bis Beendigung des Programmes
            time.sleep(.1) # Sicherheitsfenster
            if is_day: # Unterscheidung der ausgeführten Aktionen von Tag und Nacht
                if knopf_gedrueckt(): # Prüfung auf Knopfdruck, damit dies am Tag jederzeit möglich ist
                    #print("Knopf gedrückt")
                    timeraktiv = True # Änderung der Variable um Alarm Zeitweise auszuschalten
                    time.sleep(5) # 5 Sekunden Alarm deaktiviert 
                    timeraktiv = False # Alarm nach angegebener Zeit wieder einschalten
                if gpio.input(Sensor) == reedstartnumber: # Vergleich der Sensorwerte vom Start und aktuell (Hier: bei Übereinstimmung)
                    gpio.output(LED_Rot, gpio.HIGH) # Aktivierung der Roten LED, wenn Luke geöffnet ist 
                    gpio.output(LED_Gruen, gpio.LOW) # Deaktivierung der Grünen LED, wenn die Luke geöffnet ist
                    led_status = "gruen" # LED-Status ändern, um Funktion zu gewährleisten
                    alarm(False) # Änderung der Variable für den Alarm, zur Aktivierung bei Öffnung der Luke
                elif gpio.input(Sensor) != reedstartnumber: # Vergleich der Sensorwerte vom Start und aktuell (Hier: bei Unterscheidung)
                    gpio.output(LED_Rot, gpio.LOW) # Deaktivierung der Roten LED, wenn Luke geschlossen ist
                    gpio.output(LED_Gruen, gpio.HIGH) # Aktivierung der Grünen LED, wenn Luke geschlossen ist
                    led_status = "rot" # LED-Status ändern, um Funktion zu gewährleisten
                    if not timeraktiv: # Wenn der Knopf und somit auch der Timer nicht aktiviert ist
                        alarm(True) # Variable für Alarm auf True setzen, um Alarm zu aktivieren
            else: # anderer Fall, wenn es Nacht sein sollte
                if gpio.input(Sensor) == reedstartnumber: # Vergleich der Sensorwerte vom Start und aktuell (Hier: bei Übereinstimmung)
                    alarm(False) # Änderung der Variable für den Alarm, zur Aktivierung bei Öffnung der Luke (Alarm auch bei Nacht aktiv)
                elif gpio.input(Sensor) != reedstartnumber: # Vergleich der Sensorwerte vom Start und aktuell (Hier: bei Unterscheidung)
                    alarm(True) # Änderung der Variable für den Alarm, zur Deaktivierung bei Öffnung der Luke (Alarm auch bei Nacht aktiv)
            if (time.time() - __localtimer) > day_night_time: # 
                __localtimer = time.time() # Lokaler Timer mit Echtzeit abgleichen
                is_day = not is_day # Vergleich, ob Tag oder Nacht ist
                while gpio.input(Sensor) == reedstartnumber: # Vergleich der Sensorwerte vom Start und aktuell (Hier: bei Übereinstimmung)
                    time.sleep(.1) # Sicherheitsfenster
                set_schlossstatus(is_day) # Setzen des Schlossstatus auf Tag
                gpio.output(LED_Rot, gpio.LOW) # Deaktivierung der Roten LED, wärhend es Nacht ist (Alarm bleibt aktiv)
                gpio.output(LED_Gruen, gpio.LOW) # Deaktivierung der Roten LED, wärhend es Nacht ist (Alarm bleibt aktiv)
                print(is_day and "Es ist Tag" or "Es ist Nacht") # Konsolenausgabe zur Überprüfung (kann weggelassen werden)
                
                
# Aufruf der Main-Funktion, sowie Einbindung einer Funktion, um das Programm sicher zu beenden         
try:
    main() # Aufruf der main Funktion
except KeyboardInterrupt: # erwartet eine Unterbrechung durch Tastatureingabe (STRG + C)
    if not cleanedup: # Prüfung, ob die Pin-Belegung noch nicht freigegeben ist 
        cleanedup = True # Variable für den Zustand der Pin-Belegung ändern
        print("Keyboardinterruption") # Konsolenausgabe, wenn eine Unterbrechung durch die Tastatureingabe getätigt wird (kann weggelassen werden
        gpio.cleanup() # Cleanup der Pin-Belegung
finally: # erneute Prüfung der Pin-Belegung
    if not cleanedup: 
        cleanedup = True # Variable für den Zustand der Pin-Belegung ändern
        gpio.cleanup() # Cleanup der Pin-Belegung
    sys.exit() # Sciherstellen, dass das Programm beendet wird

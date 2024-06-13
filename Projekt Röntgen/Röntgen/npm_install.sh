#!/bin/bash

# Lokalisieren der Position des ConBee-Adapters
ls -l /dev/serial/by-id

# Nodesource-Repositories hinzugefügen und Node.js sowie andere benötigte Pakete installieren
sudo curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs git make g++ gcc libsystemd-dev make

# Überprüfung der Installierten Version von "NodeJS und "NPM", um spätere Komplikationen zu vermeiden
node --version  
npm --version

# Verzeichnis für ZigBee2MQTT erstellen und den aktuellen User als Besitzer berechtigen
sudo mkdir /opt/zigbee2mqtt
sudo chown -R ${USER}: /opt/zigbee2mqtt

# Das ZigBee2MQTT-Repository wird herunterladen
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt

# Hier wird in das ZigBee2MQTT-Verzeichnis gewechselt und die Abhängigkeiten installiert
cd /opt/zigbee2mqtt
npm ci

# Aufbauen der NPM-App
npm run build

# Konfigurationsdatei in zuvor erstelltes Verzeichnis für ZigBee2MQTT kopieren
cp /opt/zigbee2mqtt/data/configuration.example.yaml /opt/zigbee2mqtt/data/configuration.yaml
# Konfigurationsdatei auf das Netzwerk und den verwendeten Adapter abändern (falls nötig)
nano /opt/zigbee2mqtt/data/configuration.yaml

# In das korrekte Verzeichnis wechseln, sodass diese Daten verwendet werden können
cd /opt/zigbee2mqtt
# NPM starten (kann über den Brower mit dem Port 8080 zugegriffen werden)
npm start

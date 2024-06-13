#!/bin/bash

# Überprüfe, ob die Datei 'docker-compose.yml' vorhanden ist
if [ -f docker-compose.yaml ]; then
    echo "Docker-Compose-Datei gefunden."
else
    echo "Fehler: Docker-Compose-Datei nicht gefunden."
    exit 1
fi

# Starte die Container
echo "Starte die Container..."
docker-compose up -d

# Überprüfe die Logs
echo "Überprüfe die Logs..."
docker-compose logs -f

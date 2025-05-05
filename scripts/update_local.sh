#!/bin/bash

# Script zur Synchronisierung des lokalen Projektstands mit GitHub
# Erstellt: 05.05.2025

# Stellt sicher, dass lokale Änderungen und GitHub-Repository synchronisiert sind
cd "$(dirname "$0")/.."
echo "Aktualisiere lokalen Stand mit GitHub-Repository..."

# Hole aktuelle Änderungen vom Remote-Repository
git pull origin main

# Starte die Container mit den aktualisierten Konfigurationen neu
echo "Starte Docker-Container neu..."
docker-compose down
docker-compose up -d

echo "Überprüfe Status der Docker-Container..."
docker-compose ps

echo "Synchronisierung abgeschlossen. Du kannst jetzt auf das ERPNext-System unter http://bikedoctor.localhost zugreifen."
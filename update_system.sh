#!/bin/bash

# Update-Skript für bike.doctor ERP-System
# Erstellt: 05.05.2025
# Änderungen:
# - Initialer Script zur Synchronisierung lokaler Änderungen mit GitHub

# Stellt sicher, dass lokale Änderungen und GitHub-Repository synchronisiert sind
echo "Aktualisiere lokalen Stand mit GitHub-Repository..."

# Commit lokale Änderungen, falls vorhanden
if [ -n "$(git status --porcelain)" ]; then
  echo "Lokale Änderungen gefunden, führe Commit aus..."
  git add -A
  git commit -m "Lokale Änderungen: $(date +"%d.%m.%Y %H:%M")"
  git push origin main
fi

# Hole aktuelle Änderungen vom Remote-Repository
git pull origin main

# Starte die Container mit den aktualisierten Konfigurationen neu
echo "Starte Docker-Container neu..."
docker-compose down
docker-compose up -d

echo "Überprüfe Status der Docker-Container..."
docker-compose ps

echo "Synchronisierung abgeschlossen. Du kannst jetzt auf das ERPNext-System unter http://bikedoctor.localhost zugreifen."
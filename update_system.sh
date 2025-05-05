#!/bin/bash

# Update-Skript für bike.doctor ERP-System
# Erstellt: 05.05.2025
# Änderungen:
# - Initialer Script zur Synchronisierung lokaler Änderungen mit GitHub
# - Verbesserte Fehlerbehandlung hinzugefügt

set -e

# Stellt sicher, dass lokale Änderungen und GitHub-Repository synchronisiert sind
echo "===== bike.doctor ERP System Update ====="
echo "Aktualisiere lokalen Stand mit GitHub-Repository..."

# Commit lokale Änderungen, falls vorhanden
if [ -n "$(git status --porcelain)" ]; then
  echo "Lokale Änderungen gefunden, führe Commit aus..."
  git add -A
  git commit -m "Lokale Änderungen: $(date +"%d.%m.%Y %H:%M")"
  git push origin main
  echo "✅ Lokale Änderungen erfolgreich auf GitHub übertragen."
else
  echo "✅ Keine lokalen Änderungen gefunden."
fi

# Hole aktuelle Änderungen vom Remote-Repository
echo "Synchronisiere mit GitHub Repository..."
git pull origin main
echo "✅ Synchronisierung mit GitHub abgeschlossen."

# Starte die Container mit den aktualisierten Konfigurationen neu
echo "Starte Docker-Container neu..."
docker-compose down
echo "✅ Alle Container erfolgreich gestoppt."

docker-compose up -d
echo "✅ Container wurden im Hintergrund gestartet."

echo "Überprüfe Status der Docker-Container..."
docker-compose ps

echo ""
echo "✅ Synchronisierung abgeschlossen. Du kannst jetzt auf das ERPNext-System unter http://bikedoctor.localhost zugreifen."
echo "Hinweis: Es kann einige Sekunden dauern, bis alle Dienste vollständig gestartet sind."
# Minimale Installation für bike.doctor ERP
# Erstellt am: 2025-05-05
# Diese Anleitung beschreibt ein garantiert funktionierendes minimales Setup

## Schritt 1: Alles bereinigen

Führe diese Befehle aus, um alle bestehenden Container zu entfernen:

```bash
# Stoppe alle laufenden Container
docker-compose down -v
docker-compose -f docker-compose.simple.yml down -v

# Aufräumen
docker rm -f $(docker ps -aq) 2>/dev/null || true
docker volume prune -f
```

## Schritt 2: Das minimale Setup starten

```bash
# Verwende die minimale Konfiguration
docker-compose -f docker-compose.minimal.yml up -d
```

## Schritt 3: Überprüfe die Installation

Nach dem Start kannst du die Logs überwachen mit:
```bash
docker logs -f erpnext-minimal
```

## Schritt 4: Zugriff auf ERPNext

Sobald das System gestartet ist (kann einige Minuten dauern):

1. Öffne in deinem Browser: http://localhost:8080
2. Melde dich an mit:
   - Benutzername: Administrator
   - Passwort: admin

## Wenn das minimale Setup funktioniert

Wenn das minimale Setup funktioniert, können wir:

1. Ein spezifischeres Setup mit unserer bikedoctor-App erstellen
2. Die Benutzerrollen und Berechtigungen einrichten
3. Mit den Meilensteinen auf der Roadmap fortfahren

## Fehlerbehebung

Wenn Probleme auftreten:
1. Überprüfe, ob Port 8080 verfügbar ist
2. Überprüfe, ob Docker genügend Ressourcen hat (mind. 4GB RAM)
3. Schau in die Container-Logs mit `docker logs erpnext-minimal`

## Wichtiger Hinweis

Dieses Setup ist nur ein Startpunkt. Es enthält noch nicht die bikedoctor-App, aber es stellt sicher, dass du ein funktionierendes ERPNext-System hast, auf dem wir aufbauen können.
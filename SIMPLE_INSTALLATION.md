# Vereinfachte Installation für bike.doctor ERP
# Erstellt am: 2025-05-05
# Letzte Änderung: Anleitung für die vereinfachte Docker-Installation und Konfiguration

Diese Anleitung beschreibt eine vereinfachte Installation des bike.doctor ERP-Systems mit Docker, die weniger fehleranfällig ist als die komplexere Multi-Container-Konfiguration.

## Voraussetzungen

- Docker und Docker Compose sind installiert
- Git ist installiert
- Mindestens 4GB RAM und 2 CPU-Kerne
- 10GB freier Festplattenspeicher

## Schritt 1: Bestehende Container bereinigen

Um sauber zu starten, sollten alle bestehenden Container und Volumes entfernt werden:

```bash
# Stoppe und entferne alle bestehenden Container und deren Volumes
docker-compose down -v

# Entferne manuell alle Container, falls noch vorhanden
docker rm -f bd-erpnext bd-mariadb bd-redis-cache bd-redis-queue bd-redis-socketio

# Entferne ungenutzte Volumes
docker volume prune -f
```

## Schritt 2: Docker-Container mit vereinfachtem Setup starten

Die vereinfachte Konfiguration nutzt das offizielle ERPNext-Worker-Image und montiert die bikedoctor-App direkt ein:

```bash
# Starte das vereinfachte Setup
docker-compose -f docker-compose.simple.yml up -d
```

Die folgenden Container werden gestartet:
- bd-erpnext: Hauptanwendungsserver mit ERPNext
- bd-mariadb: Datenbank für ERPNext
- bd-redis-cache, bd-redis-queue, bd-redis-socketio: Redis-Instanzen für verschiedene Funktionen

## Schritt 3: Installation überwachen

Die erste Installation dauert einige Minuten. Du kannst den Fortschritt überwachen mit:

```bash
docker logs -f bd-erpnext
```

Warte, bis du Meldungen siehst, die anzeigen, dass der Server bereit ist (z.B. "ERPNext server started").

## Schritt 4: ERPNext zugänglich machen

1. Öffne einen Webbrowser und gehe zu: [http://localhost:8000](http://localhost:8000)
2. Falls die Domain nicht auflösbar ist, füge folgenden Eintrag zu deiner `/etc/hosts`-Datei hinzu:
   ```
   127.0.0.1 bikedoctor.localhost
   ```
3. Melde dich mit folgenden Anmeldedaten an:
   - Benutzername: `Administrator`
   - Passwort: `admin`

## Schritt 5: Überprüfung der Bikedoctor-App

Nach der Anmeldung solltest du die bikedoctor-App im System sehen. Du kannst dies in der ERPNext-Oberfläche überprüfen unter:

```
Einstellungen > Integrierte Apps
```

Die bikedoctor-App sollte in der Liste erscheinen.

## Fehlerbehebung

### Container starten nicht
- Überprüfe die Docker-Logs mit `docker logs bd-erpnext`
- Stelle sicher, dass keine anderen Dienste die Ports 8000 und 9000 belegen

### BikeDoctor-App ist nicht installiert
Wenn die App nicht in der Liste der installierten Apps erscheint, kannst du sie manuell installieren:
```bash
docker exec -it bd-erpnext bash -c "cd /home/frappe/frappe-bench && bench --site bikedoctor.localhost install-app bikedoctor"
```

### Website nicht erreichbar
- Überprüfe, ob der ERPNext-Container läuft mit `docker ps`
- Prüfe, ob du bikedoctor.localhost in deiner /etc/hosts-Datei hinzugefügt hast

### Neustart bei Problemen
```bash
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d
```

### Vollständiger Reset
```bash
docker-compose -f docker-compose.simple.yml down -v
docker-compose -f docker-compose.simple.yml up -d
```
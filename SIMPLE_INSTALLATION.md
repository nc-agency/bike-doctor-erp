# Vereinfachte Installation für bike.doctor ERP
# Erstellt am 2025-05-05
# Diese Anleitung beschreibt die vereinfachte Installation des bike.doctor ERP-Systems

# Vereinfachte Installation für bike.doctor ERP

Diese Anleitung beschreibt eine vereinfachte Installation des bike.doctor ERP-Systems mit Docker, die weniger fehleranfällig ist als die komplexere Multi-Container-Konfiguration.

## Voraussetzungen

- Docker und Docker Compose sind installiert
- Git ist installiert
- Mindestens 4GB RAM und 2 CPU-Kerne
- 10GB freier Festplattenspeicher

## Schritt 1: Repository klonen (falls noch nicht geschehen)

```bash
git clone https://github.com/nc-agency/bike-doctor-erp.git
cd bike-doctor-erp
```

## Schritt 2: Docker-Container starten

```bash
docker-compose -f docker-compose.simple.yml up -d
```

Die folgenden Container werden gestartet:
- erpnext: Hauptanwendungsserver mit ERPNext
- mariadb: Datenbank für ERPNext
- redis-cache, redis-queue, redis-socketio: Redis-Instanzen für verschiedene Funktionen

## Schritt 3: Auf die Installation warten

Die erste Installation dauert einige Minuten. Sie können den Fortschritt überwachen mit:

```bash
docker logs -f erpnext
```

Warten Sie, bis Sie Meldungen sehen, die anzeigen, dass der Server bereit ist (z.B. "ERPNext server started").

## Schritt 4: Auf das System zugreifen

1. Öffnen Sie einen Webbrowser und gehen Sie zu: [http://localhost:8000](http://localhost:8000)
2. Falls die Domain nicht auflösbar ist, fügen Sie folgenden Eintrag zu Ihrer `/etc/hosts`-Datei hinzu:
   ```
   127.0.0.1 bikedoctor.localhost
   ```
3. Melden Sie sich mit folgenden Anmeldedaten an:
   - Benutzername: `Administrator`
   - Passwort: `admin`

## Schritt 5: bike.doctor App installieren

Sobald ERPNext läuft, können Sie die bike.doctor App installieren:

```bash
docker exec -it erpnext bench --site bikedoctor.localhost get-app bikedoctor /home/frappe/frappe-bench/apps/bikedoctor
docker exec -it erpnext bench --site bikedoctor.localhost install-app bikedoctor
docker exec -it erpnext bench --site bikedoctor.localhost clear-cache
```

## Fehlerbehebung

### Container starten nicht
- Überprüfen Sie die Docker-Logs mit `docker logs erpnext`
- Stellen Sie sicher, dass keine anderen Dienste die Ports belegen

### Website nicht erreichbar
- Überprüfen Sie, ob der ERPNext-Container läuft mit `docker ps`
- Prüfen Sie, ob Sie bikedoctor.localhost in Ihrer /etc/hosts-Datei hinzugefügt haben

### Um alle Container neu zu starten
```bash
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d
```

### Um alle Daten zu löschen und neu zu beginnen
```bash
docker-compose -f docker-compose.simple.yml down -v
docker-compose -f docker-compose.simple.yml up -d
```

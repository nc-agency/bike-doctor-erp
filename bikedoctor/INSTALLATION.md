# Installation der BikeDoctor ERPNext-App
# Erstellt am 2025-05-05
# Anleitung zur Installation der BikeDoctor-App in ERPNext

# BikeDoctor Workshop Management Installation

Diese Anleitung beschreibt, wie du die BikeDoctor Workshop Management App in deine ERPNext-Installation integrierst.

## Voraussetzungen

* Eine funktionierende ERPNext-Installation (Version 15)
* Ausreichende Berechtigungen auf dem Server
* Git

## Installation mit dem Bench-Tool

1. Wechsle in dein Bench-Verzeichnis:
   ```bash
   cd /path/to/your/bench
   ```

2. Hole den Code aus dem GitHub-Repository:
   ```bash
   bench get-app https://github.com/nc-agency/bike-doctor-erp.git
   ```
   oder wenn du das Repository bereits lokal hast:
   ```bash
   bench add-app /local/path/to/bikedoctor
   ```

3. Installiere die App in deiner Site:
   ```bash
   bench --site yoursite.local install-app bikedoctor
   ```

4. Starte den Bench-Server neu:
   ```bash
   bench restart
   ```

## Installation in Docker-Umgebung

1. Kopiere das Verzeichnis `bikedoctor` in dein custom_apps-Verzeichnis deiner frappe_docker-Installation.

2. Füge "bikedoctor" zur Liste der Apps in deiner .env-Datei hinzu:
   ```
   APPS_LIST=frappe,erpnext,bikedoctor
   ```

3. Baue und starte die Container neu:
   ```bash
   docker-compose up -d --build
   ```

## Nach der Installation

1. Melde dich in ERPNext an.

2. Die BikeDoctor Workshop Management App sollte nun in der App-Liste und im Desk-Menü sichtbar sein.

3. Konfiguriere die App unter "BikeDoctor Workshop Management Settings".

4. Erstelle die grundlegenden Datensätze:
   - Bike Brands
   - Service Types
   - Workshop Settings

## Fehlerbehebung

1. Falls die App nach der Installation nicht angezeigt wird:
   ```bash
   bench --site yoursite.local clear-cache
   bench restart
   ```

2. Falls DocTypes fehlen:
   ```bash
   bench --site yoursite.local migrate
   bench restart
   ```

3. Bei anderen Problemen überprüfe die Logs:
   ```bash
   bench --site yoursite.local show-logs
   ```

## Support

Bei Fragen oder Problemen wende dich an support@bike.doctor oder eröffne ein Issue auf GitHub.

# bike.doctor ERP - Installationsanleitung

Erstellt: 05.05.2025  
Änderungen:
- Initiale Erstellung der Installationsanleitung für das bike.doctor ERP-System

## Voraussetzungen

- Docker und Docker Compose installiert
- Git installiert
- Mindestens 4GB RAM und 2 CPU-Kerne
- 10GB freier Festplattenspeicher

## Schritt 1: Repository klonen

```bash
git clone https://github.com/nc-agency/bike-doctor-erp.git
cd bike-doctor-erp
```

## Schritt 2: Docker-Container starten

```bash
docker-compose up -d
```

Die folgenden Container werden gestartet:
- traefik: Reverse Proxy für den Webzugriff
- mariadb: Datenbank für ERPNext
- redis: Cache und Message-Broker
- erpnext-app: Hauptanwendungsserver
- erpnext-worker: Hintergrundprozesse
- erpnext-socketio: Echtzeit-Kommunikation
- erpnext-web: Frontend-Server

## Schritt 3: ERPNext-Initialisierung und Site-Erstellung

Verbinden Sie sich mit dem erpnext-app Container und führen Sie die folgende Befehle aus:

```bash
# Verbindung zum Container herstellen
docker-compose exec erpnext-app bash

# Im Container: Bench-Umgebung initialisieren
cd /home/frappe/frappe-bench
bench init-bench

# Eine neue Site erstellen
bench new-site bikedoctor.localhost --admin-password=admin --db-name=bikedoctor --db-password=bikedoctor --db-user=bikedoctor

# ERPNext für diese Site installieren
bench --site bikedoctor.localhost install-app erpnext

# Unsere benutzerdefinierte App installieren
bench --site bikedoctor.localhost install-app bikedoctor

# Site aktivieren
bench --site bikedoctor.localhost enable-scheduler
bench --site bikedoctor.localhost set-config developer_mode 1
bench --site bikedoctor.localhost clear-cache
```

## Schritt 4: ERPNext-Grundkonfiguration

Nach der Installation können Sie die ERPNext-Weboberfläche unter http://bikedoctor.localhost aufrufen und sich mit dem Benutzernamen "Administrator" und dem Passwort "admin" anmelden.

Folgende Grundkonfigurationen sind durchzuführen:

1. **Unternehmensdaten einrichten**:
   - Navigieren Sie zu "Einstellungen > Unternehmen > Neues Unternehmen"
   - Legen Sie "bike.doctor" als Firmenname fest
   - Fügen Sie Logo, Adresse und Kontaktdaten hinzu

2. **Währung konfigurieren**:
   - Navigieren Sie zu "Einstellungen > Währungen"
   - Stellen Sie sicher, dass "EUR" als Hauptwährung eingerichtet ist

3. **Steuersätze konfigurieren**:
   - Navigieren Sie zu "Buchhaltung > Steuern > Steuersatz"
   - Erstellen Sie die notwendigen Steuersätze (z.B. 19% MwSt für Teile, 7% für Reparaturen)

4. **Lager einrichten**:
   - Navigieren Sie zu "Lager > Lager"
   - Erstellen Sie ein Hauptlager für "bike.doctor"
   - Fügen Sie Lagerbereiche für "Neuteile", "Gebrauchtteile" und "Werkzeuge" hinzu

## Schritt 5: Benutzer und Berechtigungen einrichten

Erstellen Sie Benutzerrollen über das Terminal und anschließend Benutzer über die Weboberfläche:

```bash
# Verbindung zum erpnext-app Container herstellen
docker-compose exec erpnext-app bash

# Im Container: Rollen erstellen
bench --site bikedoctor.localhost execute "frappe.core.doctype.role.role.create_custom_role('Werkstattleiter')"
bench --site bikedoctor.localhost execute "frappe.core.doctype.role.role.create_custom_role('Techniker')"
bench --site bikedoctor.localhost execute "frappe.core.doctype.role.role.create_custom_role('Kassierer')"
```

Anschließend können Sie über die Weboberfläche Benutzer erstellen und ihnen die entsprechenden Rollen zuweisen.

## Schritt 6: DocTypes registrieren

Die benutzerdefinierten DocTypes können entweder automatisch über das Installationsskript oder manuell über das Terminal registriert werden:

```bash
# Verbindung zum erpnext-app Container herstellen
docker-compose exec erpnext-app bash

# DocTypes registrieren
bench --site bikedoctor.localhost migrate
```

## Fehlerbehebung

### Container starten nicht
- Überprüfen Sie, ob die Ports 80, 3306, 8000, 9000 bereits verwendet werden
- Prüfen Sie die Docker-Logs mit `docker-compose logs -f`

### Datenbank-Fehler
- Stellen Sie sicher, dass die Datenbank korrekt initialisiert wurde
- Überprüfen Sie die Datenbankverbindung mit `docker-compose exec mariadb mysql -u bikedoctor -pbikedoctor -D bikedoctor`

### Website nicht erreichbar
- Überprüfen Sie, ob alle Container laufen mit `docker-compose ps`
- Prüfen Sie die DNS-Einstellungen und Host-Datei
- Stellen Sie sicher, dass bikedoctor.localhost auf 127.0.0.1 zeigt

## Nützliche Befehle

```bash
# Alle Container stoppen
docker-compose down

# Alle Container und Volumes löschen (Achtung: Datenverlust!)
docker-compose down -v

# Logs anzeigen
docker-compose logs -f

# In einen Container einsteigen
docker-compose exec [service-name] bash
```

## Kontakt und Support

Bei Fragen oder Problemen wenden Sie sich an:
- E-Mail: support@bike.doctor
- Telefon: +49-123-4567890
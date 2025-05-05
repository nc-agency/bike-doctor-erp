# Testanleitung für die bike.doctor ERPNext-App
# Erstellt am 2025-05-05
# Diese Anleitung beschreibt, wie die bike.doctor-App nach der Installation getestet werden kann

# bike.doctor App Testanleitung

Diese Anleitung beschreibt, wie du die bike.doctor Workshop Management App in deiner Docker-Umgebung testen kannst, nachdem du die Installation abgeschlossen hast.

## Voraussetzungen

- Docker und Docker Compose sind installiert
- Das bike-doctor-erp Repository wurde geklont
- Die Docker-Container wurden mit `docker-compose up -d` gestartet
- ERPNext und die bike.doctor App wurden erfolgreich installiert

## Schritt 1: Zugriff auf die ERPNext-Weboberfläche

1. Öffne deinen Browser und gehe zu: [http://bikedoctor.localhost](http://bikedoctor.localhost)
2. Falls die Domain nicht auflösbar ist, füge folgenden Eintrag zu deiner `/etc/hosts`-Datei hinzu:
   ```
   127.0.0.1 bikedoctor.localhost
   ```
3. Melde dich mit folgenden Anmeldedaten an:
   - Benutzername: `Administrator`
   - Passwort: `admin`

## Schritt 2: Überprüfen der installierten bike.doctor-App

1. Nach der Anmeldung solltest du im Hauptmenü einen Eintrag "Bike Workshop" sehen.
2. Klicke auf diesen Eintrag, um zum Bike Workshop Management-Bereich zu gelangen.

### Falls der Eintrag nicht sichtbar ist:

1. Gehe zum ERPNext-Terminal mit:
   ```bash
   docker-compose exec backend bench console
   ```
2. Überprüfe die installierten Apps:
   ```python
   frappe.get_installed_apps()
   ```
3. Falls "bikedoctor" nicht in der Liste erscheint, installiere die App manuell:
   ```bash
   docker-compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site bikedoctor.localhost install-app bikedoctor"
   ```
4. Aktualisiere den Cache:
   ```bash
   docker-compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site bikedoctor.localhost clear-cache"
   ```

## Schritt 3: Grundlegende DocTypes testen

### Bike Brand

1. Gehe zu "Bike Workshop" > "Setup" > "Bike Brands"
2. Klicke auf "Neu", um eine neue Fahrradmarke anzulegen
3. Fülle die erforderlichen Felder aus:
   - Brand Name: "Trek"
   - Website: "https://www.trekbikes.com"
   - Land: "USA"
4. Speichere den Eintrag mit "Speichern"

### Service Type

1. Gehe zu "Bike Workshop" > "Setup" > "Service Types" 
2. Klicke auf "Neu", um einen neuen Servicetyp zu erstellen
3. Fülle die Felder aus:
   - Service Name: "Standard Inspektion"
   - Kategorie: "Basic Service"
   - Standard-Rate: 49.90
   - Geschätzte Stunden: 1.0
   - Beschreibung: "Standardinspektion inkl. Bremsen, Schaltung, Laufräder und Verschleißteile"
4. Füge einige Checklistenpunkte hinzu:
   - "Bremsen prüfen" (Erforderlich)
   - "Schaltung einstellen" (Erforderlich)
   - "Luftdruck prüfen" (Erforderlich)
   - "Kette ölen" (Erforderlich)
5. Speichere den Eintrag

### Bike Details

1. Gehe zu "Bike Workshop" > "Bike Details"
2. Klicke auf "Neu", um ein neues Fahrrad anzulegen
3. Fülle die erforderlichen Felder aus:
   - Fahrradmarke: "Trek" (die zuvor erstellte Marke)
   - Modell: "Domane SL 6"
   - Jahr: 2023
   - Rahmennummer: "WTU123456789"
   - Besitzer-Typ: "Customer"
4. Da noch kein Kunde angelegt ist, erstelle zuerst einen Kunden:
   - Gehe zu "Verkauf" > "Kunden"
   - Erstelle einen neuen Kunden
   - Kehre zum Bike Details-Formular zurück und wähle den Kunden aus
5. Speichere das Fahrrad

### Workshop Order

1. Gehe zu "Bike Workshop" > "Workshop Operations" > "Workshop Order"
2. Klicke auf "Neu", um einen neuen Werkstattauftrag zu erstellen
3. Wähle den zuvor erstellten Kunden aus
4. Wähle das zuvor erstellte Fahrrad aus
5. Füge im Tab "Services" den zuvor erstellten Service "Standard Inspektion" hinzu
6. Füge eine Problembeschreibung im Tab "Notes" hinzu
7. Speichere den Auftrag und reiche ihn ein
8. Überprüfe, ob eine Job Card automatisch erstellt wurde

## Schritt 4: Workflow testen

1. Gehe zu "Bike Workshop" > "Workshop Operations" > "Job Card"
2. Öffne die automatisch erstellte Job Card
3. Klicke auf "Start Job" und überprüfe, ob die Startzeit gesetzt wird
4. Füge ein paar Teile hinzu:
   - Gehe zum Tab "Parts Used"
   - Füge ein neues Teil hinzu (falls nötig, erstelle vorher ein Teil unter "Lager" > "Items")
5. Klicke auf "Complete Job" und überprüfe, ob die Endzeit gesetzt wird
6. Gehe zurück zum Workshop Order und überprüfe, ob der Status aktualisiert wurde

## Fehlerbehebung

### Problem: DocType nicht gefunden

Falls ein DocType-Fehler auftritt:

```bash
docker-compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site bikedoctor.localhost migrate"
docker-compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site bikedoctor.localhost clear-cache"
```

### Problem: Import-Fehler oder fehlende Module

Falls Python-Import-Fehler auftreten:

```bash
docker-compose exec backend bash -c "cd /home/frappe/frappe-bench && pip install qrcode Pillow"
docker-compose restart backend
```

### Problem: Fehlende Berechtigungen

Stelle sicher, dass die Workshop-Rollen korrekt erstellt wurden:
1. Gehe zu "Einstellungen" > "Rolle"
2. Überprüfe, ob "Workshop Manager" und "Workshop Technician" existieren
3. Falls nicht, erstelle sie manuell und weise sie dem Administrator-Benutzer zu

## Nächste Schritte

Nach erfolgreichem Test kannst du:

1. Weitere Benutzer mit verschiedenen Rollen anlegen
2. Benutzerdefinierten Arbeitsabläufe definieren
3. Berichte erstellen und testen
4. Dein Feedback und gefundene Probleme melden

## Support

Bei Fragen oder Problemen wende dich an:
- GitHub Issues: https://github.com/nc-agency/bike-doctor-erp/issues

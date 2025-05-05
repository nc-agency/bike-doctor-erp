# Meilenstein 5: Benutzer und Berechtigungen Einrichtung
# Erstellt am: 2025-05-05
# Diese Anleitung beschreibt die Einrichtung von Benutzern und Berechtigungen gemäß Meilenstein 5 der Roadmap

## Übersicht

Diese Anleitung hilft dir dabei, die folgenden Punkte aus Meilenstein 5 umzusetzen:
- Administrator-Benutzer konfigurieren
- Werkstatt-Mitarbeiter mit entsprechenden Rollen definieren
- Berechtigungssystem für verschiedene Benutzergruppen konfigurieren
- Test der Benutzerzugänge und Berechtigungen

## Voraussetzungen

- ERPNext und bikedoctor sind installiert und laufen (gemäß SIMPLE_INSTALLATION.md)
- Du hast Administratorzugriff auf das System

## Schritt 1: Ausführen des Setup-Skripts

Das vorgefertigte Setup-Skript richtet automatisch alle notwendigen Rollen, Berechtigungen und Beispielbenutzer ein:

```bash
# Kopiere das Skript in den Container
docker cp setup_roles_and_permissions.py bd-erpnext:/home/frappe/frappe-bench/

# Führe das Skript im Container aus
docker exec -it bd-erpnext bench --site bikedoctor.localhost execute setup_roles_and_permissions.execute
```

## Schritt 2: Erstellte Benutzerrollen

Das Skript erstellt die folgenden Benutzerrollen:

1. **Workshop Manager**
   - Vollständige Kontrolle über alle Workshop-Dokumente
   - Zuständig für Werkstattplanung und Überwachung

2. **Workshop Technician**
   - Bearbeitet Workshop Job Cards (Arbeitsaufträge)
   - Zuständig für technische Aufgaben und Reparaturen

3. **Workshop Reception**
   - Erstellt und bearbeitet Workshop Orders (Werkstattaufträge)
   - Verwaltet Kunden- und Fahrradinformationen

## Schritt 3: Demo-Benutzer und Passwörter

Das Skript erstellt folgende Demo-Benutzer:

| Benutzer                        | Rolle               | Passwort         |
|---------------------------------|---------------------|------------------|
| workshop.manager@bikedoctor.test| Workshop Manager    | BikeManager@123  |
| technician@bikedoctor.test      | Workshop Technician | BikeTech@123     |
| reception@bikedoctor.test       | Workshop Reception  | BikeRec@123      |

## Schritt 4: Test der Benutzerrollen

Um die verschiedenen Rollen zu testen:

1. Melde dich als einer der Demo-Benutzer an
2. Überprüfe die verfügbaren Module und Dokumente
3. Teste die Erstellung und Bearbeitung von Dokumenten je nach Berechtigungsstufe

### Workshop Manager Test:
- Sollte alle Dokumente erstellen, bearbeiten und löschen können
- Sollte Zugriff auf Reports und Dashboards haben

### Workshop Technician Test:
- Sollte Arbeitsaufträge sehen und bearbeiten können
- Sollte keine Werkstattaufträge anlegen können
- Sollte Fahrraddetails einsehen können

### Workshop Reception Test:
- Sollte Werkstattaufträge anlegen und bearbeiten können
- Sollte Kundendaten und Fahrradinformationen verwalten können
- Sollte keine Jobkarten abschließen können

## Schritt 5: Anpassung der Berechtigungen

Falls du die Berechtigungen anpassen möchtest, kannst du dies in der ERPNext-Oberfläche tun:

1. Gehe zu Einstellungen > Benutzer und Berechtigungen > Rollenberechtigungen verwalten
2. Wähle die Rolle aus, die du anpassen möchtest
3. Passe die Berechtigungen für die verschiedenen DocTypes an

## Fehlerbehebung

### Skript führt zu Fehlern
- Überprüfe, ob alle DocTypes vorhanden sind (Workshop Order, Workshop Job Card, etc.)
- Stelle sicher, dass das System als Administrator ausgeführt wird

### Benutzer können sich nicht anmelden
- Überprüfe, ob die E-Mail-Domain richtig konfiguriert ist
- Setze die Passwörter manuell in der ERPNext-Benutzeroberfläche zurück

### Berechtigungsprobleme
- Überprüfe die Rollenberechtigungen in ERPNext
- Stelle sicher, dass die Benutzer die richtigen Rollen zugewiesen bekommen haben
# bike.doctor ERP

Ein ERPNext-basiertes Managementsystem für die Fahrradwerkstatt bike.doctor.

## Beschreibung

Diese Anwendung basiert auf ERPNext und bietet spezialisierte Funktionen für die Fahrradwerkstatt bike.doctor, darunter:

- Fahrrad- und Kundenverwaltung
- Werkstattmanagement und Reparaturverfolgung
- Inventarmanagement für Fahrradteile
- Terminplanung und Kalenderfunktionen
- Rechnungsstellung und Finanzen
- Mitarbeiterverwaltung und Technikerplanung

## Installation

### Voraussetzungen

- Docker und Docker Compose
- Git

### Installation

1. Repository klonen:
   ```
   git clone https://github.com/nc-agency/bike-doctor-erp.git
   cd bike-doctor-erp
   ```

2. Docker-Container starten:
   ```
   docker-compose up -d
   ```

3. ERPNext-Setup über den Browser ausführen:
   ```
   http://bikedoctor.localhost
   ```

## Spezielle Funktionen für bike.doctor

### Fahrradmanagement
- Detaillierte Fahrraderfassung mit technischen Daten
- Komponentenverwaltung mit Austausch- und Reparaturhistorie
- QR-Code-Generation für schnelle Fahrradidentifikation

### Werkstattverwaltung
- Werkstattstationen und Arbeitsplätze
- Technikerzuweisung und Skill-Management
- Automatische Statusaktualisierung

### Kundenverwaltung
- Kundenstammdaten mit Fahrradverknüpfung
- Kommunikationshistorie
- Automatische Benachrichtigungen bei Reparaturstatus-Änderungen

## Implementierungsplan

Eine detaillierte Implementierungs-Roadmap findest du in der [ROADMAP.md](ROADMAP.md)-Datei. Diese enthält einen umfassenden Plan mit klaren Meilensteinen, Zeitvorgaben und Ressourcenanforderungen.

## Benutzerdefinierte Datenmodelle

- **Bicycle**: Verwaltung aller Fahrräder mit detaillierten technischen Informationen
- **Bicycle Component**: Komponenten der Fahrräder mit Zustand und Historie
- **Bicycle Repair**: Reparatur- und Wartungsaufträge mit Status und Kosten
- **Bicycle Repair Part**: Verwendete Teile bei Reparaturen

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
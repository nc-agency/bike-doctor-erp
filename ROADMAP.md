# ROADMAP für bike.doctor ERP-System
# Erstellt: April 2025
# Letzte Aktualisierung: 05.05.2025
# Änderungen:
# - Meilenstein 1 erreicht: ERPNext v15 Installation abgeschlossen
# - Meilenstein 2 erreicht: Custom App bikedoctor integriert
# - Redis-Konfigurationsproblem behoben
# - Synchronisierungs-Tooling hinzugefügt

## Einleitung

Diese Roadmap skizziert die geplanten Entwicklungsphasen für das bike.doctor ERP-System. Das Ziel ist es, eine vollständige ERPNext-basierte Lösung für die Fahrradwerkstatt zu implementieren.

## Phasen und Meilensteine

### Phase 1: Grundinstallation und Setup (✅ ABGESCHLOSSEN)

- ✅ ERPNext v15 in Docker-Umgebung installieren
- ✅ Konfiguration der Datenbank, Redis und anderer Services
- ✅ Einrichtung der Domain bikedoctor.localhost
- ✅ Erstellung der grundlegenden Admin-Accounts
- ✅ Initialisierung des Projekts mit Versionskontrolle

### Phase 2: Integration der bikedoctor-App (✅ ABGESCHLOSSEN)

- ✅ Erstellung der bikedoctor Custom App
- ✅ Integration in das ERPNext-System
- ✅ Konfiguration der Berechtigungen
- ✅ Konfiguration des PYTHONPATH für die App
- ✅ Behebung von Redis-Verbindungsproblemen
- ✅ Erstellung des Update- und Synchronisierungsskripts

### Phase 3: Datenmodellierung für die Fahrradwerkstatt (🔄 IN BEARBEITUNG)

- ⬜ Definition der DocTypes für die Werkstatt:
  - ⬜ Fahrrad (Bicycle)
  - ⬜ Fahrradkomponenten (Bicycle Components)
  - ⬜ Reparaturauftrag (Repair Order)
  - ⬜ Werkzeuge (Tools)
  - ⬜ Lagerbestand (Inventory)
- ⬜ Einrichtung der Beziehungen zwischen den DocTypes
- ⬜ Implementierung der Validierungslogik
- ⬜ Erstellung der Suchfunktionen

### Phase 4: Geschäftsprozessmodellierung

- ⬜ Modellierung des Reparaturprozesses
  - ⬜ Auftragsannahme
  - ⬜ Diagnose
  - ⬜ Kostenvoranschlag
  - ⬜ Reparatur
  - ⬜ Qualitätskontrolle
  - ⬜ Übergabe
- ⬜ Modellierung des Verkaufsprozesses
  - ⬜ Beratung
  - ⬜ Konfiguration
  - ⬜ Bestellung
  - ⬜ Montage
  - ⬜ Übergabe
- ⬜ Modellierung des Bestellprozesses
  - ⬜ Bestandsüberwachung
  - ⬜ Lieferantenauswahl
  - ⬜ Bestellung
  - ⬜ Wareneingangskontrolle

### Phase 5: Berichts- und Dashboards-Implementierung

- ⬜ Werkstattauslastungsbericht
- ⬜ Umsatzbericht nach Kategorien
- ⬜ Lagerbericht
- ⬜ Kundenstatistiken
- ⬜ Mitarbeiterproduktivität

### Phase 6: Benutzeroberfläche und UX

- ⬜ Anpassung der Benutzeroberfläche an CI von bike.doctor
- ⬜ Optimierung der Benutzerführung
- ⬜ Implementierung von Schnellerfassungsformularen
- ⬜ Responsive Design für Tablet-Nutzung in der Werkstatt

### Phase 7: Integration und Schnittstellen

- ⬜ E-Mail-Integration für Kundenkommunikation
- ⬜ SMS-Benachrichtigungen für Auftragsstatus
- ⬜ Anbindung an Online-Terminbuchungssystem
- ⬜ Integration mit Kassensystem
- ⬜ Schnittstelle zu Lieferanten-Bestellsystemen

### Phase 8: Schulung und Dokumentation

- ⬜ Erstellung von Benutzerhandbüchern
- ⬜ Schulung der Mitarbeiter
- ⬜ Dokumentation der technischen Implementierung
- ⬜ Erstellung von Wartungs- und Supportprozessen

### Phase 9: Go-Live und Support

- ⬜ Abnahmetests
- ⬜ Datenmigration aus Altsystemen
- ⬜ Go-Live
- ⬜ Post-Go-Live Support
- ⬜ Feedback und kontinuierliche Verbesserung

## Aktueller Stand

- **Abgeschlossen:** Phase 1 und 2
- **In Bearbeitung:** Phase 3
- **Nächster Schritt:** Definition und Implementierung der DocTypes für Fahrrad und Komponenten

## Offene Probleme

- Redis-Verbindungsproblem wurde mit `BENCH_LOCAL_REDIS=0` in der Docker-Compose-Konfiguration behoben
- Docker-Container synchronisierbar über das erstellte Update-Skript

## System-Informationen

- **ERPNext-Version:** v15
- **Docker Images:** frappe/erpnext:v15
- **Datenbank:** MariaDB 10.6
- **Web-Server:** Nginx
- **Host-System:** macOS
- **Domain:** bikedoctor.localhost
# bike.doctor ERP

## Projektübersicht
Dieses Repository enthält die Docker-basierte ERPNext-Implementierung für die Fahrradwerkstatt bike.doctor, mit einer kundenspezifischen bikedoctor-App.

## Status
- ERPNext v15 wurde erfolgreich installiert und läuft stabil
- Die bikedoctor-App wurde erfolgreich ins System integriert
- Die Datenbankstruktur ist konfiguriert
- Docker-Volumes und PYTHONPATH-Einstellungen sind korrekt konfiguriert

## Installation und Einrichtung

### Voraussetzungen
- Docker und Docker Compose
- Git

### Einrichtung
1. Repository klonen:
   ```bash
   git clone https://github.com/nc-agency/bike-doctor-erp.git
   cd bike-doctor-erp
   ```

2. System starten:
   ```bash
   docker-compose up -d
   ```

3. Zugriff auf das System:
   - Die ERPNext-Web-Oberfläche ist unter http://bikedoctor.localhost erreichbar
   - Anmeldedaten: Administrator / admin

## System-Update und Wartung

Wir haben ein praktisches Skript erstellt, um die lokale Umgebung mit GitHub zu synchronisieren und das System zu aktualisieren. Um es zu verwenden:

1. Mache das Skript ausführbar (einmalig):
   ```bash
   chmod +x update_system.sh
   ```

2. Führe das Update-Skript aus:
   ```bash
   ./update_system.sh
   ```

Das Skript führt automatisch folgende Aktionen aus:
- Überprüft, ob lokale Änderungen vorhanden sind und committet diese
- Synchronisiert mit dem GitHub-Repository
- Startet die Docker-Container neu, um Änderungen zu übernehmen

## Projektstruktur
- `docker-compose.yml`: Hauptkonfigurationsdatei für Docker
- `.env`: Umgebungsvariablen für die Docker-Container
- `custom_apps/bikedoctor/`: Die benutzerdefinierte App für die Fahrradwerkstatt
- `ROADMAP.md`: Detaillierte Implementierungs-Roadmap mit Meilensteinen

## Fehlerbehebung

### Redis-Verbindungsfehler
Falls ein Redis-Verbindungsfehler auftritt, stellt das Update-Skript sicher, dass die korrekten Redis-Einstellungen verwendet werden.

### Datenbank-Zugangsprobleme
Bei Datenbankzugriffsproblemen können die Berechtigungen wiederhergestellt werden:
```bash
docker-compose exec mariadb mysql -uroot -pfrappe -e "GRANT ALL PRIVILEGES ON \`_18fac39732df0c89\`.* TO '_18fac39732df0c89'@'%' IDENTIFIED BY 'vwkLXvMY6Kifh83X' WITH GRANT OPTION; FLUSH PRIVILEGES;"
```

## Nächste Schritte
Siehe die detaillierte Roadmap in `ROADMAP.md` für die geplanten nächsten Schritte und Meilensteine.

---
Erstellt für bike.doctor Fahrradwerkstatt - Mai 2025
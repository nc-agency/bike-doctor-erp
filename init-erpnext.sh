#!/bin/bash
# init-erpnext.sh - Initialisierungsscript für ERPNext
# 
# Dieses Script initialisiert eine neue ERPNext-Installation für bike.doctor
# und wird als Entrypoint für den erpnext-app Container verwendet.
# Erstellt am: 2025-05-05
# Änderungen:
# - Initiale Erstellung des Scripts zur Verbesserung der Initialisierungssequenz von ERPNext
# - Aufgeteilt in besser nachvollziehbare Schritte mit detaillierter Ausgabe für Debugging

set -e  # Beendet das Script bei Fehlern
echo "Start der ERPNext-Initialisierung"
echo "Warte 15 Sekunden auf Datenbankstart"
sleep 15

cd /home/frappe/frappe-bench

# Konfiguration einrichten
echo "Konfiguriere Frappe Bench Settings..."
bench set-config -g db_host mariadb
bench set-config -g redis_cache "redis://redis:6379/0"
bench set-config -g redis_queue "redis://redis:6379/1"
bench set-config -g redis_socketio "redis://redis:6379/2"
bench set-config -g socketio_port 9000

# Prüfe Frappe bench Status
echo "Führe Bench Doctor aus..."
bench doctor || true

# Erstelle neue Site
echo "Erstelle neue Site bikedoctor.localhost..."
bench new-site bikedoctor.localhost \
  --db-name frappe \
  --admin-password admin \
  --mariadb-root-password frappe \
  --db-root-username root \
  --db-password frappe \
  --install-app erpnext

# Migration durchführen
echo "Führe Datenbankmigration durch..."
bench --site bikedoctor.localhost migrate

# Scheduler aktivieren
echo "Aktiviere Scheduler..."
bench --site bikedoctor.localhost enable-scheduler

# Site als Standard setzen
echo "Füge Site zu hosts hinzu und setze als Standard..."
bench --site bikedoctor.localhost add-to-hosts
bench use bikedoctor.localhost

# Führe Bench Doctor erneut aus
echo "Überprüfe finalen Status..."
bench doctor || true

# Starte Gunicorn
echo "Starte Gunicorn Server..."
exec /home/frappe/frappe-bench/env/bin/gunicorn -b 0.0.0.0:8000 --threads=4 -w 2 frappe.app:application --timeout 120
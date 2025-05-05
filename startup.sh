#!/bin/bash
# Startup-Skript für bike.doctor ERPNext Backend
# Erstellt am: 2025-05-05
# Verbessert die Initialisierung von ERPNext mit Fehlerbehandlung und Statusberichten

set -e
echo "=== bike.doctor ERPNext Startskript ==="
echo "$(date): Starte Backend-Dienst..."

# Container-Status-Check
function check_redis_connection() {
  echo "Prüfe Redis-Verbindung..."
  local redis_host=${REDIS_CACHE:-redis}
  local redis_port=${REDIS_PORT:-6379}
  if timeout 5 bash -c "echo PING | nc $redis_host $redis_port" | grep -q PONG; then
    echo "✓ Redis-Verbindung erfolgreich ($redis_host:$redis_port)"
    return 0
  else
    echo "✗ Keine Verbindung zu Redis ($redis_host:$redis_port)"
    return 1
  fi
}

function check_mariadb_connection() {
  echo "Prüfe MariaDB-Verbindung..."
  local db_host=${DB_HOST:-mariadb}
  local db_port=${DB_PORT:-3306}
  if timeout 5 bash -c "</dev/tcp/$db_host/$db_port"; then
    echo "✓ MariaDB-Verbindung erfolgreich ($db_host:$db_port)"
    return 0
  else
    echo "✗ Keine Verbindung zu MariaDB ($db_host:$db_port)"
    return 1
  fi
}

function apply_fixes() {
  # Stellt sicher, dass Redis nicht lokal verwendet wird
  echo "Stellt sicher, dass Redis-Konfiguration korrekt ist..."
  if grep -q "localhost" /home/frappe/frappe-bench/sites/common_site_config.json 2>/dev/null; then
    echo "Korrigiere Redis-Host-Einstellungen in common_site_config.json"
    sed -i 's/"localhost"/"redis"/g' /home/frappe/frappe-bench/sites/common_site_config.json
  fi
  
  # Prüfe und korrigiere site_config.json
  for site in /home/frappe/frappe-bench/sites/*; do
    if [ -d "$site" ] && [ -f "$site/site_config.json" ]; then
      site_name=$(basename "$site")
      echo "Prüfe Site-Konfiguration für: $site_name"
      
      if grep -q "localhost" "$site/site_config.json"; then
        echo "Korrigiere Redis-Host-Einstellungen in $site/site_config.json"
        sed -i 's/"localhost"/"redis"/g' "$site/site_config.json"
      fi
    fi
  done
}

# Hauptprozess
echo "Prüfe Systemvoraussetzungen..."
for i in {1..5}; do
  if check_redis_connection && check_mariadb_connection; then
    break
  else
    echo "Warte auf Datenbankservices (Versuch $i/5)..."
    sleep 3
  fi
done

# Wendet Konfigurationskorrekturen an
apply_fixes

# Startet den angeforderten Dienst
case "$1" in
  start)
    echo "Starte Frappe Backend mit Gunicorn..."
    cd /home/frappe/frappe-bench
    bench start
    ;;
  worker)
    echo "Starte Worker für Queue: $2"
    cd /home/frappe/frappe-bench
    bench worker --queue "$2"
    ;;
  scheduler)
    echo "Starte Scheduler..."
    cd /home/frappe/frappe-bench
    bench schedule
    ;;
  *)
    echo "Führe benutzerdefinierten Befehl aus: $@"
    exec "$@"
    ;;
esac
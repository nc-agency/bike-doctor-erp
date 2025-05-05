# Backend Dockerfile für bike.doctor ERPNext
# Erstellt am: 2025-05-05
# Optimierungen für bessere Performance und Stabilität
# Diese Datei dient zur Erweiterung des Standard-ERPNext-Images mit zusätzlichen Konfigurationen

FROM frappe/erpnext:v15

USER root

# Installiere zusätzliche Tools für bessere Systemdiagnose
RUN apt-get update && apt-get install -y \
    htop \
    vim \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optimierung der Python-Umgebung
RUN pip install --upgrade pip \
    && pip install --no-cache-dir \
    sentry-sdk \
    redis-sentinel-url \
    pymemcache

# Konfiguriere Gunicorn für bessere Performance
COPY gunicorn_conf.py /home/frappe/frappe-bench/

# Füge benutzerdefiniertes Startup-Skript hinzu
COPY startup.sh /home/frappe/
RUN chmod +x /home/frappe/startup.sh

USER frappe

# Setze Umgebungsvariablen für Redis-Verbindungen
ENV BENCH_LOCAL_REDIS=0 \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["/home/frappe/startup.sh"]

# Standard-Befehl, wenn kein anderer Befehl angegeben wird
CMD ["start"]
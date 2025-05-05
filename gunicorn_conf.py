# Gunicorn-Konfigurationsdatei für bike.doctor ERPNext
# Erstellt am: 2025-05-05
# Optimierte Einstellungen für Performance und Stabilität

import os
import multiprocessing

# Anzahl der Worker-Prozesse
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Anzahl der Worker-Threads pro Prozess
threads = 4

# Timeout in Sekunden
timeout = 120

# Maximale Anfragen pro Worker
max_requests = 5000
max_requests_jitter = 500

# Arbeitsmodus (geev oder sync)
worker_class = 'gthread'

# Verbindungsoptionen
bind = '0.0.0.0:8000'
keepalive = 30

# Log-Konfiguration
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Worker Recycling
graceful_timeout = 30
preload_app = False

# Server Hook-Funktionen
def on_starting(server):
    """Log when server starts."""
    server.log.info('Gunicorn server is starting')

def on_exit(server):
    """Log when server exits."""
    server.log.info('Gunicorn server is shutting down')
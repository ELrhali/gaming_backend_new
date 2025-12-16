"""
Configuration Gunicorn pour Goback Backend
"""
import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/home/gobagma/logs/gunicorn_access.log"
errorlog = "/home/gobagma/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "goback_backend"

# Server mechanics
daemon = False
pidfile = "/home/gobagma/run/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (si nécessaire)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"

# Server hooks
def on_starting(server):
    print("Gunicorn is starting...")

def on_reload(server):
    print("Gunicorn is reloading...")

def when_ready(server):
    print("Gunicorn is ready. Spawning workers")

def on_exit(server):
    print("Gunicorn is shutting down...")

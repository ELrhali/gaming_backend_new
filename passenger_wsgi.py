"""
Passenger WSGI config for Goback project on Nidohost.
"""
import os
import sys

# Chemin vers le projet Django sur le serveur Nidohost
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajouter le chemin du projet au PYTHONPATH
sys.path.insert(0, BASE_DIR)

# Ajouter le chemin de l'environnement virtuel
VENV_PATH = os.path.join(BASE_DIR, '.venv', 'lib', 'python3.11', 'site-packages')
if os.path.exists(VENV_PATH):
    sys.path.insert(0, VENV_PATH)

# Alternative pour Python 3.10
VENV_PATH_310 = os.path.join(BASE_DIR, '.venv', 'lib', 'python3.10', 'site-packages')
if os.path.exists(VENV_PATH_310):
    sys.path.insert(0, VENV_PATH_310)

# Définir les variables d'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Charger les variables d'environnement depuis .env si disponible
from pathlib import Path
env_file = Path(BASE_DIR) / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Importer l'application WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

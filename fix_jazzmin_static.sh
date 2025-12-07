#!/bin/bash
# Script de correction pour collecter les fichiers statiques Jazzmin au bon endroit

echo "=== Correction des fichiers statiques Jazzmin ==="

cd ~/backend
source ~/virtualenv/backend/3.11/bin/activate

# 1. Mettre à jour depuis GitHub
echo "1. Mise à jour depuis GitHub..."
git fetch origin
git reset --hard origin/master

# 2. Copier le fichier .env.production vers .env
echo "2. Configuration de l'environnement..."
cp .env.production .env

# 3. Vérifier STATIC_ROOT
echo "3. Vérification de STATIC_ROOT..."
grep "STATIC_ROOT" .env
python -c "
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
static_root = os.getenv('STATIC_ROOT')
print(f'STATIC_ROOT configuré à: {static_root}')
"

# 4. Vérifier que jazzmin est dans INSTALLED_APPS
echo "4. Vérification de jazzmin dans INSTALLED_APPS..."
python -c "
import os, sys
sys.path.insert(0, '/home/mafourn2/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from django.conf import settings
apps = settings.INSTALLED_APPS
if 'jazzmin' in apps:
    position = apps.index('jazzmin')
    print(f'✓ jazzmin trouvé à la position {position}')
    if position == 0:
        print('✓ jazzmin est en première position (CORRECT)')
    else:
        print('✗ jazzmin devrait être en première position')
else:
    print('✗ jazzmin NOT FOUND in INSTALLED_APPS')
"

# 5. Supprimer l'ancien dossier static
echo "5. Nettoyage de l'ancien dossier static..."
rm -rf ~/public_html/static/*

# 6. Collecter les fichiers statiques
echo "6. Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# 7. Vérifier que Jazzmin est bien collecté
echo "7. Vérification des fichiers Jazzmin..."
if [ -d ~/public_html/static/jazzmin ]; then
    echo "✓ Dossier jazzmin trouvé"
    ls -lh ~/public_html/static/jazzmin/
    echo "Fichiers CSS Jazzmin:"
    ls ~/public_html/static/jazzmin/css/ 2>/dev/null
    echo "Fichiers JS Jazzmin:"
    ls ~/public_html/static/jazzmin/js/ 2>/dev/null
else
    echo "✗ Dossier jazzmin NON TROUVÉ - PROBLÈME!"
    echo "Localisation de jazzmin:"
    python -c "import jazzmin; import os; print(os.path.dirname(jazzmin.__file__))"
fi

# 8. Permissions
echo "8. Configuration des permissions..."
chmod -R 755 ~/public_html/static/
chmod -R 755 ~/public_html/media/

# 9. Compter les fichiers
echo "9. Statistiques des fichiers statiques:"
echo "Total fichiers: $(find ~/public_html/static/ -type f | wc -l)"
echo "Fichiers admin: $(find ~/public_html/static/admin -type f 2>/dev/null | wc -l)"
echo "Fichiers jazzmin: $(find ~/public_html/static/jazzmin -type f 2>/dev/null | wc -l)"

# 10. Redémarrer Gunicorn
echo "10. Redémarrage de Gunicorn..."
pkill -f gunicorn
sleep 3
~/backend/start_django.sh
sleep 2

# 11. Vérifier Gunicorn
echo "11. Vérification de Gunicorn..."
if ps aux | grep -v grep | grep gunicorn > /dev/null; then
    echo "✓ Gunicorn actif"
    ps aux | grep gunicorn | grep -v grep
else
    echo "✗ Gunicorn non actif"
fi

# 12. Test final
echo "12. Test de l'interface admin..."
echo "Réponse HTTP:"
curl -I https://mafourniturescolaire.ma/django-admin/ 2>/dev/null | head -1
echo ""
echo "Test CSS Jazzmin:"
curl -I https://mafourniturescolaire.ma/static/jazzmin/css/main.css 2>/dev/null | head -1

echo ""
echo "=== Terminé ==="
echo "Ouvrez: https://mafourniturescolaire.ma/django-admin/"
echo "Si l'interface n'est toujours pas correcte, exécutez:"
echo "  tail -f ~/logs/gunicorn_error.log"

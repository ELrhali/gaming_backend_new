#!/bin/bash
# Script de déploiement de l'interface Jazzmin améliorée

echo "=== Déploiement de l'interface admin améliorée ==="

# 1. Sauvegarder les changements locaux
echo "Étape 1: Sauvegarde des changements locaux..."
cd ~/backend
git stash

# 2. Pull les derniers changements
echo "Étape 2: Récupération des derniers changements..."
git pull origin master

# 3. Vérifier l'installation de Jazzmin
echo "Étape 3: Vérification de django-jazzmin..."
source ~/virtualenv/backend/3.11/bin/activate
pip install django-jazzmin --upgrade

# 4. Collecter les fichiers statiques
echo "Étape 4: Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# 5. Vérifier que Jazzmin est dans les static files
echo "Étape 5: Vérification des fichiers Jazzmin..."
ls -la ~/public_html/static/ | grep -i jazzmin
if [ $? -eq 0 ]; then
    echo "✓ Fichiers Jazzmin trouvés"
else
    echo "✗ Fichiers Jazzmin non trouvés - Problème de collecte"
fi

# 6. Permissions
echo "Étape 6: Configuration des permissions..."
chmod -R 755 ~/public_html/static/

# 7. Redémarrer Gunicorn
echo "Étape 7: Redémarrage de Gunicorn..."
pkill -f gunicorn
sleep 2
~/backend/start_django.sh

# 8. Vérifier que Gunicorn tourne
echo "Étape 8: Vérification de Gunicorn..."
sleep 3
ps aux | grep gunicorn | grep -v grep
if [ $? -eq 0 ]; then
    echo "✓ Gunicorn est actif"
else
    echo "✗ Gunicorn n'est pas actif - Problème de démarrage"
fi

# 9. Tester l'accès
echo "Étape 9: Test de l'interface admin..."
curl -I https://mafourniturescolaire.ma/django-admin/ 2>/dev/null | head -1

echo ""
echo "=== Déploiement terminé ==="
echo "Allez sur: https://mafourniturescolaire.ma/django-admin/"
echo ""

#!/bin/bash
# Script de déploiement automatique pour NindoHost
# À placer dans /home/mafourn2/deploy.sh

echo "🚀 Début du déploiement..."

# Aller dans le dossier backend
cd ~/backend || exit

# Activer l'environnement virtuel
echo "📦 Activation de l'environnement virtuel..."
source ~/virtualenv/backend/3.11/bin/activate

# Mettre à jour le code (si Git est configuré)
if [ -d .git ]; then
    echo "📥 Mise à jour du code depuis Git..."
    git pull origin master
fi

# Installer/Mettre à jour les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Migrations de base de données
echo "🗄️  Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Redémarrer l'application
echo "🔄 Redémarrage de l'application..."
touch passenger_wsgi.py

echo "✅ Déploiement terminé avec succès!"
echo "🌐 Votre site est maintenant à jour sur https://mafourniturescolaire.ma"

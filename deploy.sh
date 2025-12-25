#!/bin/bash

# Script de déploiement pour gaming Backend sur Nidohost
# Ce script doit être exécuté sur le serveur après avoir cloné le repo

set -e  # Arrêter en cas d'erreur

echo "=========================================="
echo "  Déploiement gaming Backend - Nidohost  "
echo "=========================================="

# Variables
PROJECT_DIR="/home/gobackma/gaming_backend"
VENV_DIR="/home/gobackma/venv"
PYTHON_VERSION="python3.11"  # Ajuster selon la version disponible sur le serveur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[1/10] Création des répertoires nécessaires...${NC}"
mkdir -p /home/gobackma/logs
mkdir -p /home/gobackma/run
mkdir -p /home/gobackma/backup

echo -e "${YELLOW}[2/10] Mise à jour du système...${NC}"
# Note: Cette commande nécessite les droits sudo
# sudo apt update && sudo apt upgrade -y

echo -e "${YELLOW}[3/10] Installation des dépendances système...${NC}"
# sudo apt install -y python3.11 python3.11-venv python3.11-dev 
# sudo apt install -y mysql-server libmysqlclient-dev
# sudo apt install -y nginx supervisor
# sudo apt install -y git curl wget

echo -e "${YELLOW}[4/10] Création de l'environnement virtuel Python...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_VERSION -m venv $VENV_DIR
    echo -e "${GREEN}✓ Environnement virtuel créé${NC}"
else
    echo -e "${GREEN}✓ Environnement virtuel existe déjà${NC}"
fi

echo -e "${YELLOW}[5/10] Activation de l'environnement virtuel...${NC}"
source $VENV_DIR/bin/activate

echo -e "${YELLOW}[6/10] Installation des packages Python...${NC}"
cd $PROJECT_DIR
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}[7/10] Configuration de l'environnement...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env.production $PROJECT_DIR/.env
    echo -e "${RED}⚠ IMPORTANT: Éditez le fichier .env avec vos vraies valeurs!${NC}"
    echo -e "${RED}  nano $PROJECT_DIR/.env${NC}"
else
    echo -e "${GREEN}✓ Fichier .env existe déjà${NC}"
fi

echo -e "${YELLOW}[8/10] Collecte des fichiers statiques...${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}[9/10] Migrations de la base de données...${NC}"
python manage.py migrate

echo -e "${YELLOW}[10/10] Création du superutilisateur (si nécessaire)...${NC}"
echo "Pour créer un superutilisateur, exécutez manuellement:"
echo "  python manage.py createsuperuser"

echo ""
echo -e "${GREEN}=========================================="
echo -e "  Déploiement terminé avec succès! ✓"
echo -e "==========================================${NC}"
echo ""
echo "Prochaines étapes:"
echo "  1. Éditez le fichier .env avec vos vraies valeurs"
echo "  2. Configurez Nginx (voir nginx_gaming.conf)"
echo "  3. Configurez Supervisor (voir supervisor_gaming.conf)"
echo "  4. Redémarrez les services:"
echo "     sudo systemctl restart nginx"
echo "     sudo supervisorctl reread"
echo "     sudo supervisorctl update"
echo "     sudo supervisorctl start gaming"
echo ""

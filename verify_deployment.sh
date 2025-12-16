#!/bin/bash

# Script de vérification post-déploiement
# À exécuter sur le serveur après le déploiement

echo "================================================"
echo "  Vérification Post-Déploiement Goback Backend"
echo "================================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Compteurs
PASS=0
FAIL=0
WARN=0

# Fonction de vérification
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC} - $1"
        ((PASS++))
    else
        echo -e "${RED}✗ FAIL${NC} - $1"
        ((FAIL++))
    fi
}

check_warn() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ OK${NC} - $1"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠ WARN${NC} - $1"
        ((WARN++))
    fi
}

echo -e "${BLUE}[1/10] Vérification des répertoires...${NC}"
test -d "/home/gobagma/goback_backend"
check "Répertoire backend existe"

test -d "/home/gobagma/venv"
check "Environnement virtuel existe"

test -d "/home/gobagma/public_html/backend/staticfiles"
check "Répertoire staticfiles existe"

test -d "/home/gobagma/public_html/backend/media"
check "Répertoire media existe"

test -d "/home/gobagma/logs"
check "Répertoire logs existe"

echo ""
echo -e "${BLUE}[2/10] Vérification des fichiers de configuration...${NC}"
test -f "/home/gobagma/goback_backend/.env"
check "Fichier .env existe"

test -f "/home/gobagma/goback_backend/manage.py"
check "Fichier manage.py existe"

test -f "/home/gobagma/goback_backend/gunicorn_config.py"
check "Configuration Gunicorn existe"

echo ""
echo -e "${BLUE}[3/10] Vérification Python et packages...${NC}"
source /home/gobagma/venv/bin/activate

python3 --version > /dev/null 2>&1
check "Python est installé"

pip show django > /dev/null 2>&1
check "Django est installé"

pip show gunicorn > /dev/null 2>&1
check "Gunicorn est installé"

pip show pymysql > /dev/null 2>&1
check "PyMySQL est installé"

echo ""
echo -e "${BLUE}[4/10] Vérification de la base de données...${NC}"
cd /home/gobagma/goback_backend

python manage.py check --database default > /dev/null 2>&1
check "Connexion base de données OK"

python manage.py showmigrations | grep -q "\[X\]"
check_warn "Migrations appliquées"

echo ""
echo -e "${BLUE}[5/10] Vérification des services...${NC}"
systemctl is-active nginx > /dev/null 2>&1
check "Nginx est actif"

supervisorctl status goback | grep -q "RUNNING"
check "Gunicorn (via Supervisor) est actif"

echo ""
echo -e "${BLUE}[6/10] Vérification des ports...${NC}"
netstat -tlnp 2>/dev/null | grep -q ":8000"
check "Port 8000 (Gunicorn) écoute"

netstat -tlnp 2>/dev/null | grep -q ":80"
check "Port 80 (HTTP) écoute"

netstat -tlnp 2>/dev/null | grep -q ":443"
check_warn "Port 443 (HTTPS) écoute"

echo ""
echo -e "${BLUE}[7/10] Vérification des fichiers statiques...${NC}"
test -d "/home/gobagma/public_html/backend/staticfiles/admin"
check "Fichiers static admin collectés"

COUNT=$(find /home/gobagma/public_html/backend/staticfiles -type f | wc -l)
if [ $COUNT -gt 10 ]; then
    echo -e "${GREEN}✓ OK${NC} - $COUNT fichiers statiques trouvés"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ WARN${NC} - Seulement $COUNT fichiers statiques"
    ((WARN++))
fi

echo ""
echo -e "${BLUE}[8/10] Vérification des permissions...${NC}"
test -r "/home/gobagma/goback_backend/manage.py"
check "Permissions lecture backend OK"

test -w "/home/gobagma/logs"
check "Permissions écriture logs OK"

test -w "/home/gobagma/public_html/backend/media"
check "Permissions écriture media OK"

echo ""
echo -e "${BLUE}[9/10] Test de l'application...${NC}"
curl -s http://127.0.0.1:8000 > /dev/null 2>&1
check "Application répond sur localhost:8000"

curl -s http://127.0.0.1:8000/api/products/ > /dev/null 2>&1
check_warn "API produits accessible"

curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1
check_warn "Admin panel accessible"

echo ""
echo -e "${BLUE}[10/10] Vérification SSL/HTTPS...${NC}"
if [ -d "/etc/letsencrypt/live" ]; then
    ls /etc/letsencrypt/live/ | grep -q "api.gobag.ma"
    check_warn "Certificat SSL installé pour api.gobag.ma"
else
    echo -e "${YELLOW}⚠ WARN${NC} - SSL non configuré (exécuter: sudo certbot --nginx -d api.gobag.ma)"
    ((WARN++))
fi

echo ""
echo "================================================"
echo "              RÉSUMÉ DES VÉRIFICATIONS         "
echo "================================================"
echo -e "${GREEN}✓ Réussis:${NC} $PASS"
echo -e "${YELLOW}⚠ Avertissements:${NC} $WARN"
echo -e "${RED}✗ Échecs:${NC} $FAIL"
echo "================================================"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ SUCCÈS - Le déploiement semble correct!${NC}"
    echo ""
    echo "Prochaines étapes recommandées:"
    echo "  1. Configurer SSL: sudo certbot --nginx -d api.gobag.ma"
    echo "  2. Tester l'API: curl https://api.gobag.ma/api/products/"
    echo "  3. Configurer le backup: crontab -e"
    echo "  4. Accéder à l'admin: https://api.gobag.ma/admin/"
    exit 0
else
    echo -e "${RED}✗ ERREURS DÉTECTÉES - Vérifiez les logs${NC}"
    echo ""
    echo "Commandes de diagnostic:"
    echo "  sudo supervisorctl status"
    echo "  sudo systemctl status nginx"
    echo "  tail -f /home/gobagma/logs/gunicorn_error.log"
    echo "  tail -f /home/gobagma/logs/nginx_error.log"
    exit 1
fi

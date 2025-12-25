# Guide de Déploiement gaming Backend sur Nidohost

## 📋 Informations du Serveur

- **IP**: 178.63.126.247
- **Username**: gobackma
- **Password**: 3$lL_L3J~UU*
- **Domain Backend**: api.goback.ma (à configurer)
- **Domain Frontend**: https://goback.ma

## 🚀 Étapes de Déploiement

### 1. Connexion au Serveur

```bash
ssh gobackma@178.63.126.247
# Entrez le mot de passe: 3$lL_L3J~UU*
```

### 2. Installation des Dépendances Système

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation de Python 3.11 (ou version disponible)
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Installation de MySQL
sudo apt install -y mysql-server libmysqlclient-dev

# Installation de Nginx et Supervisor
sudo apt install -y nginx supervisor

# Installation d'outils utiles
sudo apt install -y git curl wget nano htop
```

### 3. Configuration de la Base de Données MySQL

```bash
# Se connecter à MySQL
sudo mysql -u root

# Dans MySQL, créer la base de données et l'utilisateur
CREATE DATABASE gobackma_gaming_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gobackma_gaming_user'@'localhost' IDENTIFIED BY 'VotreMotDePasseSecurisé123!';
GRANT ALL PRIVILEGES ON gobackma_gaming_db.* TO 'gobackma_gaming_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Clonage du Projet depuis GitHub

```bash
cd /home/gobackma
git clone https://github.com/votre-username/gaming_backend.git
cd gaming_backend
```

### 5. Configuration de l'Environnement Python

```bash
# Créer l'environnement virtuel
python3.11 -m venv /home/gobackma/venv

# Activer l'environnement virtuel
source /home/gobackma/venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### 6. Configuration du Fichier .env

```bash
# Copier le template de production
cp .env.production .env

# Éditer le fichier .env
nano .env
```

**Contenu du fichier .env** (à personnaliser):

```ini
# Django
SECRET_KEY=GENERER_UNE_CLE_SECRETE_UNIQUE_ICI
DEBUG=False
ALLOWED_HOSTS=178.63.126.247,goback.ma,www.goback.ma,api.goback.ma

# Database
DB_NAME=gobackma_gaming_db
DB_USER=gobackma_gaming_user
DB_PASSWORD=VotreMotDePasseSecurisé123!
DB_HOST=localhost
DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=https://goback.ma,https://www.goback.ma
CSRF_TRUSTED_ORIGINS=https://goback.ma,https://www.goback.ma,https://api.goback.ma

# Static & Media
STATIC_URL=/static/
STATIC_ROOT=/home/gobackma/public_html/backend/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/home/gobackma/public_html/gaming_backend/media
```

**Pour générer une SECRET_KEY sécurisée**:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7. Migration de la Base de Données Locale vers le Serveur

#### Option A: Export/Import SQL (Recommandé pour base existante)

**Sur votre machine locale (Windows)**:

```powershell
# Dans le terminal PowerShell
cd C:\Users\MSI\Desktop\gaming\gaming_backend

# Export de la base de données locale
# Assurez-vous que MySQL est installé localement
mysqldump -u root -p gaming_db > gaming_db_backup.sql

# Transférer le fichier vers le serveur (utiliser WinSCP, FileZilla ou scp)
# Via PowerShell avec scp (si disponible):
scp gaming_db_backup.sql gobackma@178.63.126.247:/home/gobackma/
```

**Sur le serveur**:

```bash
# Importer la base de données
mysql -u gobackma_gaming_user -p gobackma_gaming_db < /home/gobackma/gaming_db_backup.sql

# Nettoyer le fichier de backup
rm /home/gobackma/gaming_db_backup.sql
```

#### Option B: Utiliser Django dumpdata/loaddata

**Sur votre machine locale**:

```powershell
cd C:\Users\MSI\Desktop\gaming\gaming_backend
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > datadump.json
```

Transférez ensuite `datadump.json` sur le serveur et exécutez:

```bash
python manage.py loaddata datadump.json
```

### 8. Migration du Dossier Media

**Sur votre machine locale**:

```powershell
# Compresser le dossier media
Compress-Archive -Path .\media\* -DestinationPath media.zip

# Transférer vers le serveur (utiliser WinSCP, FileZilla ou scp)
scp media.zip gobackma@178.63.126.247:/home/gobackma/
```

**Sur le serveur**:

```bash
# Créer le répertoire media
mkdir -p /home/gobackma/public_html/backend/media

# Décompresser
unzip /home/gobackma/media.zip -d /home/gobackma/public_html/backend/media/

# Nettoyer
rm /home/gobackma/media.zip

# Définir les permissions
chmod -R 755 /home/gobackma/public_html/backend/media
```

### 9. Django - Migrations et Collecte des Fichiers Statiques

```bash
cd /home/gobackma/gaming_backend
source /home/gobackma/venv/bin/activate

# Créer les répertoires nécessaires
mkdir -p /home/gobackma/logs
mkdir -p /home/gobackma/run
mkdir -p /home/gobackma/public_html/backend

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur (optionnel si pas déjà dans la base)
python manage.py createsuperuser
```

### 10. Configuration de Gunicorn avec Supervisor

```bash
# Copier la configuration Supervisor
sudo cp supervisor_gaming.conf /etc/supervisor/conf.d/gaming.conf

# Recharger Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Démarrer l'application
sudo supervisorctl start gaming

# Vérifier le statut
sudo supervisorctl status gaming
```

### 11. Configuration de Nginx

```bash
# Copier la configuration Nginx
sudo cp nginx_gaming.conf /etc/nginx/sites-available/gaming

# Créer le lien symbolique
sudo ln -s /etc/nginx/sites-available/gaming /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Si tout est OK, redémarrer Nginx
sudo systemctl restart nginx
```

### 12. Installation du Certificat SSL (Let's Encrypt)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir et installer le certificat SSL pour api.goback.ma
sudo certbot --nginx -d api.goback.ma

# Le renouvellement automatique est configuré par défaut
# Vérifier avec:
sudo certbot renew --dry-run
```

### 13. Configuration DNS

Chez votre registrar de domaine (où goback.ma est enregistré), configurez:

**Pour le backend (API)**:
- Type: A
- Nom: api
- Valeur: 178.63.126.247
- TTL: 3600

**Pour le frontend**:
- Type: A
- Nom: @
- Valeur: (IP de Vercel - sera configuré plus tard)
- TTL: 3600

**Pour le www**:
- Type: CNAME
- Nom: www
- Valeur: goback.ma
- TTL: 3600

### 14. Tests de Vérification

```bash
# Vérifier que Gunicorn fonctionne
curl http://127.0.0.1:8000

# Vérifier Nginx
curl http://178.63.126.247

# Vérifier HTTPS (après configuration SSL)
curl https://api.goback.ma

# Tester l'API
curl https://api.goback.ma/api/products/
curl https://api.goback.ma/api/categories/
```

### 15. Commandes de Gestion Utiles

```bash
# Voir les logs Gunicorn
tail -f /home/gobackma/logs/gunicorn_error.log

# Voir les logs Nginx
tail -f /home/gobackma/logs/nginx_error.log

# Voir les logs Supervisor
tail -f /home/gobackma/logs/supervisor_gaming.log

# Redémarrer l'application
sudo supervisorctl restart gaming

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo supervisorctl status
sudo systemctl status nginx

# Se connecter à la base de données
mysql -u gobackma_gaming_user -p gobackma_gaming_db
```

## 🔄 Mises à Jour du Code

Pour mettre à jour le code après des modifications:

```bash
cd /home/gobackma/gaming_backend
git pull origin master

source /home/gobackma/venv/bin/activate

# Installer les nouvelles dépendances si nécessaire
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les nouveaux fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer l'application
sudo supervisorctl restart gaming
```

## 🔐 Sécurité

### Firewall (UFW)

```bash
# Activer le firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Vérifier le statut
sudo ufw status
```

### Sécurisation MySQL

```bash
sudo mysql_secure_installation
```

### Permissions des Fichiers

```bash
# Propriétaire correct
sudo chown -R gobackma:gobackma /home/gobackma/gaming_backend
sudo chown -R gobackma:gobackma /home/gobackma/public_html

# Permissions appropriées
chmod -R 755 /home/gobackma/gaming_backend
chmod -R 755 /home/gobackma/public_html/backend/staticfiles
chmod -R 755 /home/gobackma/public_html/backend/media
```

## 📊 Monitoring

### Créer un script de monitoring (optionnel)

```bash
nano /home/gobackma/monitor.sh
```

```bash
#!/bin/bash
# Script de monitoring simple

echo "=== Status des Services ==="
sudo supervisorctl status
echo ""
sudo systemctl status nginx --no-pager
echo ""

echo "=== Utilisation Disque ==="
df -h
echo ""

echo "=== Utilisation Mémoire ==="
free -h
echo ""

echo "=== Processus Gunicorn ==="
ps aux | grep gunicorn
```

```bash
chmod +x /home/gobackma/monitor.sh
```

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
tail -100 /home/gobackma/logs/gunicorn_error.log
tail -100 /home/gobackma/logs/supervisor_gaming.log

# Vérifier la configuration Supervisor
sudo supervisorctl tail gaming stderr
```

### Erreur 502 Bad Gateway

```bash
# Vérifier que Gunicorn écoute bien sur le port 8000
netstat -tlnp | grep 8000

# Redémarrer l'application
sudo supervisorctl restart gaming
```

### Problèmes de base de données

```bash
# Se connecter à MySQL
mysql -u gobackma_gaming_user -p gobackma_gaming_db

# Vérifier les tables
SHOW TABLES;

# Vérifier les migrations Django
cd /home/gobackma/gaming_backend
source /home/gobackma/venv/bin/activate
python manage.py showmigrations
```

## 📱 Frontend Configuration

Une fois le backend déployé, vous pourrez configurer le frontend sur Vercel avec:

- **Repository**: gaming_frontend
- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Environment Variable**: 
  - `NEXT_PUBLIC_API_URL=https://api.goback.ma`

## ✅ Checklist de Déploiement

- [ ] Serveur configuré et accessible
- [ ] MySQL installé et configuré
- [ ] Base de données créée et importée
- [ ] Environnement virtuel Python créé
- [ ] Dépendances Python installées
- [ ] Fichier .env configuré
- [ ] Migrations appliquées
- [ ] Fichiers statiques collectés
- [ ] Fichiers media transférés
- [ ] Gunicorn configuré avec Supervisor
- [ ] Nginx configuré
- [ ] Certificat SSL installé
- [ ] DNS configuré
- [ ] Tests de fonctionnement réussis
- [ ] Firewall activé
- [ ] Backups configurés

## 🆘 Support

En cas de problème:
1. Vérifiez les logs (`/home/gobackma/logs/`)
2. Consultez la documentation Django
3. Vérifiez la configuration Nginx et Supervisor

## 🎉 Félicitations !

Votre backend Django est maintenant déployé sur Nidohost et accessible via https://api.goback.ma

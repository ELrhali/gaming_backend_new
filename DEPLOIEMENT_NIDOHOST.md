# Guide de Déploiement Goback Backend sur Nidohost

## 📋 Informations du Serveur

- **IP**: 176.9.31.158
- **Username**: gobagma
- **Password**: 3$lL_L3J~UU*
- **Domain Backend**: api.gobag.ma (à configurer)
- **Domain Frontend**: https://gobag.ma

## 🚀 Étapes de Déploiement

### 1. Connexion au Serveur

```bash
ssh gobagma@176.9.31.158
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
CREATE DATABASE gobagma_goback_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gobagma_goback_user'@'localhost' IDENTIFIED BY 'VotreMotDePasseSecurisé123!';
GRANT ALL PRIVILEGES ON gobagma_goback_db.* TO 'gobagma_goback_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Clonage du Projet depuis GitHub

```bash
cd /home/gobagma
git clone https://github.com/votre-username/goback_backend.git
cd goback_backend
```

### 5. Configuration de l'Environnement Python

```bash
# Créer l'environnement virtuel
python3.11 -m venv /home/gobagma/venv

# Activer l'environnement virtuel
source /home/gobagma/venv/bin/activate

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
ALLOWED_HOSTS=176.9.31.158,gobag.ma,www.gobag.ma,api.gobag.ma

# Database
DB_NAME=gobagma_goback_db
DB_USER=gobagma_goback_user
DB_PASSWORD=VotreMotDePasseSecurisé123!
DB_HOST=localhost
DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=https://gobag.ma,https://www.gobag.ma
CSRF_TRUSTED_ORIGINS=https://gobag.ma,https://www.gobag.ma,https://api.gobag.ma

# Static & Media
STATIC_URL=/static/
STATIC_ROOT=/home/gobagma/public_html/backend/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/home/gobagma/public_html/backend/media
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
cd C:\Users\MSI\Desktop\goback\goback_backend

# Export de la base de données locale
# Assurez-vous que MySQL est installé localement
mysqldump -u root -p goback_db > goback_db_backup.sql

# Transférer le fichier vers le serveur (utiliser WinSCP, FileZilla ou scp)
# Via PowerShell avec scp (si disponible):
scp goback_db_backup.sql gobagma@176.9.31.158:/home/gobagma/
```

**Sur le serveur**:

```bash
# Importer la base de données
mysql -u gobagma_goback_user -p gobagma_goback_db < /home/gobagma/goback_db_backup.sql

# Nettoyer le fichier de backup
rm /home/gobagma/goback_db_backup.sql
```

#### Option B: Utiliser Django dumpdata/loaddata

**Sur votre machine locale**:

```powershell
cd C:\Users\MSI\Desktop\goback\goback_backend
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
scp media.zip gobagma@176.9.31.158:/home/gobagma/
```

**Sur le serveur**:

```bash
# Créer le répertoire media
mkdir -p /home/gobagma/public_html/backend/media

# Décompresser
unzip /home/gobagma/media.zip -d /home/gobagma/public_html/backend/media/

# Nettoyer
rm /home/gobagma/media.zip

# Définir les permissions
chmod -R 755 /home/gobagma/public_html/backend/media
```

### 9. Django - Migrations et Collecte des Fichiers Statiques

```bash
cd /home/gobagma/goback_backend
source /home/gobagma/venv/bin/activate

# Créer les répertoires nécessaires
mkdir -p /home/gobagma/logs
mkdir -p /home/gobagma/run
mkdir -p /home/gobagma/public_html/backend

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
sudo cp supervisor_goback.conf /etc/supervisor/conf.d/goback.conf

# Recharger Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Démarrer l'application
sudo supervisorctl start goback

# Vérifier le statut
sudo supervisorctl status goback
```

### 11. Configuration de Nginx

```bash
# Copier la configuration Nginx
sudo cp nginx_goback.conf /etc/nginx/sites-available/goback

# Créer le lien symbolique
sudo ln -s /etc/nginx/sites-available/goback /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Si tout est OK, redémarrer Nginx
sudo systemctl restart nginx
```

### 12. Installation du Certificat SSL (Let's Encrypt)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir et installer le certificat SSL pour api.gobag.ma
sudo certbot --nginx -d api.gobag.ma

# Le renouvellement automatique est configuré par défaut
# Vérifier avec:
sudo certbot renew --dry-run
```

### 13. Configuration DNS

Chez votre registrar de domaine (où gobag.ma est enregistré), configurez:

**Pour le backend (API)**:
- Type: A
- Nom: api
- Valeur: 176.9.31.158
- TTL: 3600

**Pour le frontend**:
- Type: A
- Nom: @
- Valeur: (IP de Vercel - sera configuré plus tard)
- TTL: 3600

**Pour le www**:
- Type: CNAME
- Nom: www
- Valeur: gobag.ma
- TTL: 3600

### 14. Tests de Vérification

```bash
# Vérifier que Gunicorn fonctionne
curl http://127.0.0.1:8000

# Vérifier Nginx
curl http://176.9.31.158

# Vérifier HTTPS (après configuration SSL)
curl https://api.gobag.ma

# Tester l'API
curl https://api.gobag.ma/api/products/
curl https://api.gobag.ma/api/categories/
```

### 15. Commandes de Gestion Utiles

```bash
# Voir les logs Gunicorn
tail -f /home/gobagma/logs/gunicorn_error.log

# Voir les logs Nginx
tail -f /home/gobagma/logs/nginx_error.log

# Voir les logs Supervisor
tail -f /home/gobagma/logs/supervisor_goback.log

# Redémarrer l'application
sudo supervisorctl restart goback

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo supervisorctl status
sudo systemctl status nginx

# Se connecter à la base de données
mysql -u gobagma_goback_user -p gobagma_goback_db
```

## 🔄 Mises à Jour du Code

Pour mettre à jour le code après des modifications:

```bash
cd /home/gobagma/goback_backend
git pull origin master

source /home/gobagma/venv/bin/activate

# Installer les nouvelles dépendances si nécessaire
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les nouveaux fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer l'application
sudo supervisorctl restart goback
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
sudo chown -R gobagma:gobagma /home/gobagma/goback_backend
sudo chown -R gobagma:gobagma /home/gobagma/public_html

# Permissions appropriées
chmod -R 755 /home/gobagma/goback_backend
chmod -R 755 /home/gobagma/public_html/backend/staticfiles
chmod -R 755 /home/gobagma/public_html/backend/media
```

## 📊 Monitoring

### Créer un script de monitoring (optionnel)

```bash
nano /home/gobagma/monitor.sh
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
chmod +x /home/gobagma/monitor.sh
```

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
tail -100 /home/gobagma/logs/gunicorn_error.log
tail -100 /home/gobagma/logs/supervisor_goback.log

# Vérifier la configuration Supervisor
sudo supervisorctl tail goback stderr
```

### Erreur 502 Bad Gateway

```bash
# Vérifier que Gunicorn écoute bien sur le port 8000
netstat -tlnp | grep 8000

# Redémarrer l'application
sudo supervisorctl restart goback
```

### Problèmes de base de données

```bash
# Se connecter à MySQL
mysql -u gobagma_goback_user -p gobagma_goback_db

# Vérifier les tables
SHOW TABLES;

# Vérifier les migrations Django
cd /home/gobagma/goback_backend
source /home/gobagma/venv/bin/activate
python manage.py showmigrations
```

## 📱 Frontend Configuration

Une fois le backend déployé, vous pourrez configurer le frontend sur Vercel avec:

- **Repository**: goback_frontend
- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Environment Variable**: 
  - `NEXT_PUBLIC_API_URL=https://api.gobag.ma`

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
1. Vérifiez les logs (`/home/gobagma/logs/`)
2. Consultez la documentation Django
3. Vérifiez la configuration Nginx et Supervisor

## 🎉 Félicitations !

Votre backend Django est maintenant déployé sur Nidohost et accessible via https://api.gobag.ma

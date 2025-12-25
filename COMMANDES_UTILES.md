# 🔧 Commandes Utiles - Serveur Nidohost

## 🔌 Connexion

```bash
# SSH
ssh gobackma@178.63.126.247
# Password: 3$lL_L3J~UU*

# Aller dans le projet
cd /home/gobackma/gaming_backend

# Activer l'environnement virtuel
source /home/gobackma/venv/bin/activate
```

## 🔄 Gestion des Services

### Gunicorn (via Supervisor)

```bash
# Status
sudo supervisorctl status gaming

# Démarrer
sudo supervisorctl start gaming

# Arrêter
sudo supervisorctl stop gaming

# Redémarrer
sudo supervisorctl restart gaming

# Recharger la configuration
sudo supervisorctl reread
sudo supervisorctl update

# Voir les logs en temps réel
sudo supervisorctl tail -f gaming stderr
```

### Nginx

```bash
# Status
sudo systemctl status nginx

# Démarrer
sudo systemctl start nginx

# Arrêter
sudo systemctl stop nginx

# Redémarrer
sudo systemctl restart nginx

# Recharger (sans downtime)
sudo systemctl reload nginx

# Tester la configuration
sudo nginx -t

# Voir la configuration active
sudo nginx -T
```

### MySQL

```bash
# Status
sudo systemctl status mysql

# Démarrer
sudo systemctl start mysql

# Arrêter
sudo systemctl stop mysql

# Redémarrer
sudo systemctl restart mysql

# Se connecter
mysql -u gobackma_gaming_user -p gobackma_gaming_db
```

## 📊 Logs

### Voir les logs

```bash
# Gunicorn - erreurs
tail -f /home/gobackma/logs/gunicorn_error.log

# Gunicorn - accès
tail -f /home/gobackma/logs/gunicorn_access.log

# Nginx - erreurs
tail -f /home/gobackma/logs/nginx_error.log

# Nginx - accès
tail -f /home/gobackma/logs/nginx_access.log

# Supervisor
tail -f /home/gobackma/logs/supervisor_gaming.log

# Toutes les erreurs récentes
tail -100 /home/gobackma/logs/gunicorn_error.log
tail -100 /home/gobackma/logs/nginx_error.log

# Suivre plusieurs logs simultanément
tail -f /home/gobackma/logs/*.log
```

### Analyser les logs

```bash
# Nombre de requêtes par IP
awk '{print $1}' /home/gobackma/logs/nginx_access.log | sort | uniq -c | sort -rn | head -20

# Erreurs 500
grep "500" /home/gobackma/logs/nginx_access.log

# Erreurs récentes
grep "ERROR" /home/gobackma/logs/gunicorn_error.log | tail -20
```

## 🐍 Django Management

```bash
cd /home/gobackma/gaming_backend
source /home/gobackma/venv/bin/activate

# Vérifier la configuration
python manage.py check

# Vérifier la base de données
python manage.py check --database default

# Créer un superuser
python manage.py createsuperuser

# Migrations
python manage.py showmigrations
python manage.py migrate
python manage.py makemigrations

# Collecter les static files
python manage.py collectstatic --noinput

# Shell Django
python manage.py shell

# Ouvrir le shell de la DB
python manage.py dbshell

# Vider une table
python manage.py flush

# Charger des données
python manage.py loaddata fixture.json

# Exporter des données
python manage.py dumpdata shop.Product --indent 2 > products.json
```

## 🗄️ Base de Données

### Connexion MySQL

```bash
# Se connecter
mysql -u gobackma_gaming_user -p gobackma_gaming_db

# Se connecter en root
sudo mysql -u root
```

### Commandes SQL utiles

```sql
-- Lister les tables
SHOW TABLES;

-- Structure d'une table
DESCRIBE shop_product;

-- Compter les enregistrements
SELECT COUNT(*) FROM shop_product;

-- Voir les produits
SELECT id, name, sku, price FROM shop_product LIMIT 10;

-- Voir les catégories
SELECT * FROM shop_category;

-- Taille de la base de données
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'gobackma_gaming_db';

-- Optimiser les tables
OPTIMIZE TABLE shop_product;

-- Quitter
EXIT;
```

### Backup et Restore

```bash
# Backup
mysqldump -u gobackma_gaming_user -p gobackma_gaming_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup compressé
mysqldump -u gobackma_gaming_user -p gobackma_gaming_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Restore
mysql -u gobackma_gaming_user -p gobackma_gaming_db < backup.sql

# Restore compressé
gunzip < backup.sql.gz | mysql -u gobackma_gaming_user -p gobackma_gaming_db

# Script automatique
/home/gobackma/gaming_backend/backup.sh
```

## 📁 Fichiers et Répertoires

### Navigation

```bash
# Répertoire projet
cd /home/gobackma/gaming_backend

# Logs
cd /home/gobackma/logs

# Static files
cd /home/gobackma/public_html/backend/staticfiles

# Media files
cd /home/gobackma/public_html/backend/media

# Backups
cd /home/gobackma/backup
```

### Permissions

```bash
# Voir les permissions
ls -la /home/gobackma/gaming_backend

# Changer le propriétaire
sudo chown -R gobackma:gobackma /home/gobackma/gaming_backend

# Changer les permissions
chmod -R 755 /home/gobackma/gaming_backend
chmod -R 755 /home/gobackma/public_html/backend

# Permissions media (lecture/écriture)
chmod -R 755 /home/gobackma/public_html/backend/media

# Permissions logs (écriture)
chmod -R 755 /home/gobackma/logs
```

### Espace disque

```bash
# Espace disque total
df -h

# Taille des répertoires
du -sh /home/gobackma/*

# Taille du projet
du -sh /home/gobackma/gaming_backend

# Taille des media
du -sh /home/gobackma/public_html/backend/media

# Plus gros fichiers
find /home/gobackma -type f -size +10M -exec ls -lh {} \; | sort -k 5 -h

# Nettoyer les logs anciens
find /home/gobackma/logs -name "*.log" -mtime +30 -delete
```

## 🔄 Mise à Jour du Code

### Depuis GitHub

```bash
cd /home/gobackma/gaming_backend

# Vérifier le statut Git
git status

# Voir les branches
git branch -a

# Pull la dernière version
git pull origin master

# Si conflit, forcer (ATTENTION: écrase les changements locaux)
git fetch origin
git reset --hard origin/master

# Après le pull
source /home/gobackma/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart gaming
```

### Mise à jour manuelle

```bash
# Télécharger un fichier depuis votre PC
# Utiliser WinSCP ou scp

# Depuis Windows (PowerShell)
scp C:\path\to\file.py gobackma@178.63.126.247:/home/gobackma/gaming_backend/

# Redémarrer après modification
sudo supervisorctl restart gaming
```

## 🔍 Monitoring

### Processus

```bash
# Voir les processus Gunicorn
ps aux | grep gunicorn

# Nombre de workers
ps aux | grep gunicorn | wc -l

# Processus Nginx
ps aux | grep nginx

# Tuer un processus (si nécessaire)
kill -9 <PID>

# Voir tous les processus par CPU
top

# Interface interactive
htop
```

### Réseau

```bash
# Ports en écoute
netstat -tlnp

# Vérifier port 8000 (Gunicorn)
netstat -tlnp | grep 8000

# Vérifier port 80 (HTTP)
netstat -tlnp | grep :80

# Vérifier port 443 (HTTPS)
netstat -tlnp | grep :443

# Connexions actives
netstat -an | grep ESTABLISHED

# Test de connexion
curl http://127.0.0.1:8000
curl https://api.goback.ma
```

### Système

```bash
# Mémoire
free -h

# CPU
lscpu
cat /proc/cpuinfo

# Uptime
uptime

# Charge système
w

# Statistiques système
vmstat 1 5

# Informations disque
lsblk
```

## 🔐 Sécurité

### Firewall (UFW)

```bash
# Status
sudo ufw status verbose

# Activer
sudo ufw enable

# Désactiver
sudo ufw disable

# Autoriser un port
sudo ufw allow 8000

# Supprimer une règle
sudo ufw delete allow 8000

# Règles numérotées
sudo ufw status numbered

# Supprimer par numéro
sudo ufw delete 2
```

### SSL/Certificats

```bash
# Renouveler le certificat
sudo certbot renew

# Renouvellement automatique (test)
sudo certbot renew --dry-run

# Lister les certificats
sudo certbot certificates

# Voir l'expiration
sudo certbot certificates | grep "Expiry Date"

# Forcer le renouvellement
sudo certbot renew --force-renewal
```

### Logs de sécurité

```bash
# Tentatives de connexion SSH
sudo grep "Failed password" /var/log/auth.log

# Connexions SSH réussies
sudo grep "Accepted password" /var/log/auth.log

# Dernières connexions
last -20
```

## 🧹 Maintenance

### Nettoyage

```bash
# Nettoyer les packages
sudo apt autoremove
sudo apt autoclean

# Nettoyer les logs anciens
find /home/gobackma/logs -name "*.log" -mtime +30 -delete

# Nettoyer les backups anciens
find /home/gobackma/backup -name "*.sql.gz" -mtime +7 -delete

# Nettoyer le cache Python
find /home/gobackma/gaming_backend -type d -name "__pycache__" -exec rm -r {} +

# Optimiser MySQL
mysql -u gobackma_gaming_user -p -e "OPTIMIZE TABLE gobackma_gaming_db.shop_product;"
```

### Backup rapide

```bash
# Backup complet
/home/gobackma/gaming_backend/backup.sh

# Backup manuel DB
mysqldump -u gobackma_gaming_user -p gobackma_gaming_db | gzip > /home/gobackma/backup/manual_backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup manuel media
tar -czf /home/gobackma/backup/media_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/gobackma/public_html/backend/media/
```

## 🧪 Tests

### Test de l'API

```bash
# Health check
curl http://127.0.0.1:8000/health/

# API produits
curl http://127.0.0.1:8000/api/products/

# API produits (avec détails)
curl -i http://127.0.0.1:8000/api/products/

# API catégories
curl http://127.0.0.1:8000/api/categories/

# Admin (devrait rediriger vers login)
curl -I http://127.0.0.1:8000/admin/

# Test HTTPS externe
curl https://api.goback.ma/api/products/

# Test avec headers
curl -H "Content-Type: application/json" https://api.goback.ma/api/products/
```

### Test de performance

```bash
# Installer ab (Apache Bench)
sudo apt install apache2-utils

# Test de charge (100 requêtes, 10 concurrentes)
ab -n 100 -c 10 http://127.0.0.1:8000/api/products/

# Test avec authentification
ab -n 100 -c 10 -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/products/
```

## 🔄 Redémarrage Complet

```bash
# Tout redémarrer dans l'ordre
sudo supervisorctl stop gaming
sudo systemctl restart nginx
sudo systemctl restart mysql
sleep 2
sudo supervisorctl start gaming

# Vérifier
sudo supervisorctl status
sudo systemctl status nginx
curl http://127.0.0.1:8000/api/products/
```

## 📞 Diagnostic Rapide

```bash
# Script de vérification
cd /home/gobackma/gaming_backend
chmod +x verify_deployment.sh
./verify_deployment.sh

# Vérification manuelle complète
echo "=== Services ==="
sudo supervisorctl status
sudo systemctl status nginx --no-pager

echo -e "\n=== Ports ==="
netstat -tlnp | grep -E ":(80|443|8000)"

echo -e "\n=== Processus ==="
ps aux | grep -E "(gunicorn|nginx)" | grep -v grep

echo -e "\n=== Logs récents ==="
tail -5 /home/gobackma/logs/gunicorn_error.log
tail -5 /home/gobackma/logs/nginx_error.log

echo -e "\n=== API Test ==="
curl -s http://127.0.0.1:8000/api/products/ | head -c 100

echo -e "\n=== Espace disque ==="
df -h /home

echo -e "\n=== Mémoire ==="
free -h
```

---

**Astuce**: Créez des alias pour les commandes fréquentes:

```bash
# Éditer ~/.bashrc
nano ~/.bashrc

# Ajouter ces alias
alias gaming='cd /home/gobackma/gaming_backend && source /home/gobackma/venv/bin/activate'
alias logs='tail -f /home/gobackma/logs/gunicorn_error.log'
alias restart='sudo supervisorctl restart gaming'
alias status='sudo supervisorctl status && sudo systemctl status nginx --no-pager'

# Recharger
source ~/.bashrc
```

Ensuite vous pouvez utiliser: `gaming`, `logs`, `restart`, `status` directement!

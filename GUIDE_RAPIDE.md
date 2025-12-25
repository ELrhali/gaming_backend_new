# 🚀 Guide Rapide - Déploiement Backend sur Nidohost

## 📝 Informations de Connexion

```
IP: 178.63.126.247
Username: gobackma
Password: 3$lL_L3J~UU*
Backend URL: https://api.goback.ma
Frontend URL: https://goback.ma
```

## ⚡ Commandes Rapides

### 1. Connexion SSH
```bash
ssh gobackma@178.63.126.247
```

### 2. Préparation du Serveur (première fois)
```bash
# Installation des dépendances système
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y mysql-server libmysqlclient-dev
sudo apt install -y nginx supervisor git

# Configuration MySQL
sudo mysql -u root
```

Dans MySQL:
```sql
CREATE DATABASE gobackma_gaming_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gobackma_gaming_root'@'localhost' IDENTIFIED BY 'VotreMotDePasseTresFort123!';
GRANT ALL PRIVILEGES ON gobackma_gaming_db.* TO 'gobackma_gaming_root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Clone du Projet
```bash
cd /home/gobackma
git clone https://github.com/votre-repo/goback_backend.git
cd goback_backend
```

### 4. Environnement Python
```bash
python3.11 -m venv /home/gobackma/venv
source /home/gobackma/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configuration .env
```bash
cp .env.production .env
nano .env
```

Générer SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Transfer de la Base de Données

**Sur Windows (local)**:
```powershell
# Export DB
cd C:\Users\MSI\Desktop\gaming\goback_backend
mysqldump -u root -p gaming_db > gaming_db_backup.sql

# Upload avec WinSCP ou:
scp gaming_db_backup.sql gobackma@178.63.126.247:/home/gobackma/
```

**Sur le serveur**:
```bash
mysql -u gobackma_gaming_root -p gobackma_gaming_db < /home/gobackma/gaming_db_backup.sql
rm /home/gobackma/gaming_db_backup.sql
```

### 7. Transfer des Fichiers Media

**Sur Windows (local)**:
```powershell
# Compresser
cd C:\Users\MSI\Desktop\gaming\goback_backend
Compress-Archive -Path .\media\* -DestinationPath media.zip

# Upload avec WinSCP ou FileZilla
```

**Sur le serveur**:
```bash
mkdir -p /home/gobackma/public_html/backend/media
unzip /home/gobackma/media.zip -d /home/gobackma/public_html/backend/media/
rm /home/gobackma/media.zip
chmod -R 755 /home/gobackma/public_html/backend/media
```

### 8. Django Setup
```bash
cd /home/gobackma/goback_backend
source /home/gobackma/venv/bin/activate

# Créer répertoires
mkdir -p /home/gobackma/logs /home/gobackma/run /home/gobackma/public_html/backend

# Migrations et static
python manage.py migrate
python manage.py collectstatic --noinput

# Créer superuser (si nécessaire)
python manage.py createsuperuser
```

### 9. Supervisor (Gunicorn)
```bash
sudo cp supervisor_gaming.conf /etc/supervisor/conf.d/gaming.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gaming
sudo supervisorctl status
```

### 10. Nginx
```bash
sudo cp nginx_gaming.conf /etc/nginx/sites-available/gaming
sudo ln -s /etc/nginx/sites-available/gaming /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11. SSL Certificate
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.goback.ma
```

### 12. Firewall
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## 🔧 Commandes de Gestion

### Redémarrer l'application
```bash
sudo supervisorctl restart gaming
```

### Voir les logs
```bash
# Gunicorn
tail -f /home/gobackma/logs/gunicorn_error.log

# Supervisor
tail -f /home/gobackma/logs/supervisor_gaming.log

# Nginx
tail -f /home/gobackma/logs/nginx_error.log
```

### Mettre à jour le code
```bash
cd /home/gobackma/goback_backend
git pull origin master
source /home/gobackma/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart gaming
```

### Vérifier les services
```bash
sudo supervisorctl status
sudo systemctl status nginx
netstat -tlnp | grep 8000
```

### Backup manuel
```bash
chmod +x /home/gobackma/goback_backend/backup.sh
/home/gobackma/goback_backend/backup.sh
```

### Configurer backup automatique (cron)
```bash
crontab -e
```
Ajouter:
```
# Backup tous les jours à 2h du matin
0 2 * * * /home/gobackma/goback_backend/backup.sh
```

## 🧪 Tests

```bash
# Test local
curl http://127.0.0.1:8000

# Test API
curl https://api.goback.ma/api/products/
curl https://api.goback.ma/api/categories/
curl https://api.goback.ma/admin/
```

## 🌐 Configuration DNS

Chez votre registrar (où goback.ma est enregistré):

**Backend API**:
- Type: A
- Nom: api
- Valeur: 178.63.126.247
- TTL: 3600

**Frontend** (après déploiement Vercel):
- Type: A
- Nom: @
- Valeur: (IP Vercel)
- TTL: 3600

## 📱 Prochaine Étape: Frontend sur Vercel

Une fois le backend opérationnel:

1. Aller sur https://vercel.com
2. Importer le repository `gaming_frontend`
3. Configurer:
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Ajouter variable d'environnement:
   - `NEXT_PUBLIC_API_URL=https://api.goback.ma`
5. Configurer le domaine `goback.ma`

## ✅ Checklist Rapide

- [ ] Connexion SSH OK
- [ ] MySQL installé et DB créée
- [ ] Projet cloné
- [ ] Environnement Python créé
- [ ] .env configuré
- [ ] Base de données importée
- [ ] Fichiers media transférés
- [ ] Migrations appliquées
- [ ] Static files collectés
- [ ] Supervisor configuré et actif
- [ ] Nginx configuré et actif
- [ ] SSL installé
- [ ] DNS configuré
- [ ] Tests réussis

## 🆘 Problèmes Courants

### Error 502 Bad Gateway
```bash
sudo supervisorctl status gaming
sudo supervisorctl restart gaming
tail -f /home/gobackma/logs/gunicorn_error.log
```

### Permission Denied
```bash
sudo chown -R gobackma:gobackma /home/gobackma/goback_backend
chmod -R 755 /home/gobackma/public_html/backend
```

### Database Connection Error
```bash
# Vérifier les credentials dans .env
nano /home/gobackma/goback_backend/.env

# Tester la connexion MySQL
mysql -u gobackma_gaming_root -p gobackma_gaming_db
```

## 📞 Support

Pour plus de détails, consultez: [DEPLOIEMENT_NIDOHOST.md](./DEPLOIEMENT_NIDOHOST.md)

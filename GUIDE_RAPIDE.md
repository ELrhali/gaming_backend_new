# 🚀 Guide Rapide - Déploiement Backend sur Nidohost

## 📝 Informations de Connexion

```
IP: 176.9.31.158
Username: gobagma
Password: 3$lL_L3J~UU*
Backend URL: https://api.gobag.ma
Frontend URL: https://gobag.ma
```

## ⚡ Commandes Rapides

### 1. Connexion SSH
```bash
ssh gobagma@176.9.31.158
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
CREATE DATABASE gobagma_goback_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gobagma_goback_user'@'localhost' IDENTIFIED BY 'VotreMotDePasseTresFort123!';
GRANT ALL PRIVILEGES ON gobagma_goback_db.* TO 'gobagma_goback_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Clone du Projet
```bash
cd /home/gobagma
git clone https://github.com/votre-repo/goback_backend.git
cd goback_backend
```

### 4. Environnement Python
```bash
python3.11 -m venv /home/gobagma/venv
source /home/gobagma/venv/bin/activate
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
cd C:\Users\MSI\Desktop\goback\goback_backend
mysqldump -u root -p goback_db > goback_db_backup.sql

# Upload avec WinSCP ou:
scp goback_db_backup.sql gobagma@176.9.31.158:/home/gobagma/
```

**Sur le serveur**:
```bash
mysql -u gobagma_goback_user -p gobagma_goback_db < /home/gobagma/goback_db_backup.sql
rm /home/gobagma/goback_db_backup.sql
```

### 7. Transfer des Fichiers Media

**Sur Windows (local)**:
```powershell
# Compresser
cd C:\Users\MSI\Desktop\goback\goback_backend
Compress-Archive -Path .\media\* -DestinationPath media.zip

# Upload avec WinSCP ou FileZilla
```

**Sur le serveur**:
```bash
mkdir -p /home/gobagma/public_html/backend/media
unzip /home/gobagma/media.zip -d /home/gobagma/public_html/backend/media/
rm /home/gobagma/media.zip
chmod -R 755 /home/gobagma/public_html/backend/media
```

### 8. Django Setup
```bash
cd /home/gobagma/goback_backend
source /home/gobagma/venv/bin/activate

# Créer répertoires
mkdir -p /home/gobagma/logs /home/gobagma/run /home/gobagma/public_html/backend

# Migrations et static
python manage.py migrate
python manage.py collectstatic --noinput

# Créer superuser (si nécessaire)
python manage.py createsuperuser
```

### 9. Supervisor (Gunicorn)
```bash
sudo cp supervisor_goback.conf /etc/supervisor/conf.d/goback.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start goback
sudo supervisorctl status
```

### 10. Nginx
```bash
sudo cp nginx_goback.conf /etc/nginx/sites-available/goback
sudo ln -s /etc/nginx/sites-available/goback /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11. SSL Certificate
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.gobag.ma
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
sudo supervisorctl restart goback
```

### Voir les logs
```bash
# Gunicorn
tail -f /home/gobagma/logs/gunicorn_error.log

# Supervisor
tail -f /home/gobagma/logs/supervisor_goback.log

# Nginx
tail -f /home/gobagma/logs/nginx_error.log
```

### Mettre à jour le code
```bash
cd /home/gobagma/goback_backend
git pull origin master
source /home/gobagma/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart goback
```

### Vérifier les services
```bash
sudo supervisorctl status
sudo systemctl status nginx
netstat -tlnp | grep 8000
```

### Backup manuel
```bash
chmod +x /home/gobagma/goback_backend/backup.sh
/home/gobagma/goback_backend/backup.sh
```

### Configurer backup automatique (cron)
```bash
crontab -e
```
Ajouter:
```
# Backup tous les jours à 2h du matin
0 2 * * * /home/gobagma/goback_backend/backup.sh
```

## 🧪 Tests

```bash
# Test local
curl http://127.0.0.1:8000

# Test API
curl https://api.gobag.ma/api/products/
curl https://api.gobag.ma/api/categories/
curl https://api.gobag.ma/admin/
```

## 🌐 Configuration DNS

Chez votre registrar (où gobag.ma est enregistré):

**Backend API**:
- Type: A
- Nom: api
- Valeur: 176.9.31.158
- TTL: 3600

**Frontend** (après déploiement Vercel):
- Type: A
- Nom: @
- Valeur: (IP Vercel)
- TTL: 3600

## 📱 Prochaine Étape: Frontend sur Vercel

Une fois le backend opérationnel:

1. Aller sur https://vercel.com
2. Importer le repository `goback_frontend`
3. Configurer:
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Ajouter variable d'environnement:
   - `NEXT_PUBLIC_API_URL=https://api.gobag.ma`
5. Configurer le domaine `gobag.ma`

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
sudo supervisorctl status goback
sudo supervisorctl restart goback
tail -f /home/gobagma/logs/gunicorn_error.log
```

### Permission Denied
```bash
sudo chown -R gobagma:gobagma /home/gobagma/goback_backend
chmod -R 755 /home/gobagma/public_html/backend
```

### Database Connection Error
```bash
# Vérifier les credentials dans .env
nano /home/gobagma/goback_backend/.env

# Tester la connexion MySQL
mysql -u gobagma_goback_user -p gobagma_goback_db
```

## 📞 Support

Pour plus de détails, consultez: [DEPLOIEMENT_NIDOHOST.md](./DEPLOIEMENT_NIDOHOST.md)

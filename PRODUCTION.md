# 🏭 Gaming Backend - Configuration Production

## 🌐 URLs de Production

- **Backend API**: https://api.goback.ma
- **Admin Panel**: https://api.goback.ma/admin/
- **Frontend**: https://goback.ma

## 📦 Fichiers de Déploiement

### Fichiers créés pour la production:

1. **`.env.production`** - Template des variables d'environnement
2. **`gunicorn_config.py`** - Configuration Gunicorn (WSGI server)
3. **`supervisor_gaming.conf`** - Configuration Supervisor (process manager)
4. **`nginx_gaming.conf`** - Configuration Nginx (web server)
5. **`deploy.sh`** - Script de déploiement automatisé
6. **`backup.sh`** - Script de backup automatique
7. **`DEPLOIEMENT_NIDOHOST.md`** - Guide complet de déploiement
8. **`GUIDE_RAPIDE.md`** - Guide rapide avec commandes essentielles

## 🚀 Déploiement en 3 Étapes

### 1. Préparation Locale

Sur votre machine Windows:

```powershell
# Aller dans le répertoire backend
cd C:\Users\MSI\Desktop\gaming\goback_backend

# Export de la base de données
mysqldump -u root -p gaming_db > gaming_db_backup.sql

# Compresser les fichiers media
Compress-Archive -Path .\media\* -DestinationPath media.zip

# Commit et push vers GitHub
git add .
git commit -m "Configuration production pour Nidohost"
git push origin master
```

### 2. Configuration Serveur

Connectez-vous au serveur:

```bash
ssh gobackma@178.63.126.247
# Password: 3$lL_L3J~UU*
```

Suivez le guide: [GUIDE_RAPIDE.md](./GUIDE_RAPIDE.md)

### 3. Vérification

Tests après déploiement:

```bash
# Test API
curl https://api.goback.ma/api/products/
curl https://api.goback.ma/api/categories/

# Accéder à l'admin
# https://api.goback.ma/admin/
```

## 🔐 Variables d'Environnement (Production)

Variables importantes à configurer dans `.env` sur le serveur:

```ini
# Sécurité
SECRET_KEY=<générer-une-clé-unique-sécurisée>
DEBUG=False
ALLOWED_HOSTS=178.63.126.247,goback.ma,www.goback.ma,api.goback.ma

# Base de données
DB_NAME=gobackma_gaming_db
DB_USER=gobackma_gaming_root
DB_PASSWORD=<mot-de-passe-sécurisé>
DB_HOST=localhost
DB_PORT=3306

# CORS (Frontend)
CORS_ALLOWED_ORIGINS=https://goback.ma,https://www.goback.ma
CSRF_TRUSTED_ORIGINS=https://goback.ma,https://www.goback.ma,https://api.goback.ma

# Chemins
STATIC_ROOT=/home/gobackma/public_html/backend/staticfiles
MEDIA_ROOT=/home/gobackma/public_html/goback_backend/media
```

## 📊 Architecture de Production

```
┌─────────────────────────────────────────┐
│          Internet (HTTPS)                │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼───────┐
         │  Nginx (443)  │  ← Reverse Proxy + SSL
         │  Web Server   │
         └───────┬───────┘
                 │
         ┌───────▼────────┐
         │ Gunicorn (8000)│  ← WSGI Server
         │  via Supervisor│
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │ Django (Python)│  ← Application
         │  gaming API    │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │  MySQL Server  │  ← Database
         │  gaming_db     │
         └────────────────┘
```

## 🛠️ Stack Technique Production

- **OS**: Ubuntu/Debian Linux
- **Python**: 3.11+
- **WSGI Server**: Gunicorn
- **Web Server**: Nginx
- **Database**: MySQL 8.0+
- **Process Manager**: Supervisor
- **SSL**: Let's Encrypt (Certbot)

## 📁 Structure sur le Serveur

```
/home/gobackma/
├── goback_backend/           # Code source
│   ├── config/
│   ├── shop/
│   ├── orders/
│   ├── admin_panel/
│   ├── manage.py
│   ├── gunicorn_config.py
│   ├── .env                  # Variables production
│   └── requirements.txt
│
├── venv/                     # Environnement Python
│
├── public_html/
│   └── backend/
│       ├── staticfiles/      # Static files
│       └── media/            # Media uploads
│
├── logs/                     # Logs applicatifs
│   ├── gunicorn_access.log
│   ├── gunicorn_error.log
│   ├── nginx_access.log
│   └── nginx_error.log
│
├── run/                      # PID files
│   └── gunicorn.pid
│
└── backup/                   # Backups automatiques
    ├── db_backup_*.sql.gz
    └── media_backup_*.tar.gz
```

## 🔄 Workflow de Mise à Jour

1. **Développement local** → Test
2. **Commit & Push** → GitHub
3. **Pull sur serveur** → Deploy
4. **Restart services** → Production

Commandes:
```bash
cd /home/gobackma/goback_backend
git pull origin master
source /home/gobackma/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart gaming
```

## 🔒 Sécurité

### Configurations importantes:

1. **SSL/TLS**: Certificat Let's Encrypt
2. **Firewall**: UFW activé (ports 22, 80, 443)
3. **DEBUG**: `False` en production
4. **SECRET_KEY**: Unique et sécurisée
5. **Permissions**: Fichiers et dossiers appropriés
6. **CORS**: Uniquement domaines autorisés
7. **MySQL**: User avec privilèges limités

### Headers de sécurité (Nginx):

- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

## 📈 Monitoring & Logs

### Vérification des services:

```bash
# Status général
sudo supervisorctl status
sudo systemctl status nginx

# Logs en temps réel
tail -f /home/gobackma/logs/gunicorn_error.log
tail -f /home/gobackma/logs/nginx_error.log

# Utilisation système
htop
df -h
free -h
```

## 💾 Backups

### Backup automatique configuré:

- **Fréquence**: Quotidien (2h du matin)
- **Rétention**: 7 jours
- **Contenu**: Base de données + Media files
- **Script**: `backup.sh`

### Backup manuel:

```bash
/home/gobackma/goback_backend/backup.sh
```

## 🐛 Dépannage

### Problème: 502 Bad Gateway

```bash
sudo supervisorctl status gaming
sudo supervisorctl restart gaming
tail -f /home/gobackma/logs/gunicorn_error.log
```

### Problème: Static files non chargés

```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Problème: Erreur de base de données

```bash
# Vérifier la connexion
mysql -u gobackma_gaming_root -p gobackma_gaming_db

# Vérifier .env
cat /home/gobackma/goback_backend/.env
```

## 📞 Support & Documentation

- **Guide Complet**: [DEPLOIEMENT_NIDOHOST.md](./DEPLOIEMENT_NIDOHOST.md)
- **Guide Rapide**: [GUIDE_RAPIDE.md](./GUIDE_RAPIDE.md)
- **GitHub**: Votre repository
- **Django Docs**: https://docs.djangoproject.com

## ✅ Checklist de Production

- [ ] Code déployé sur le serveur
- [ ] Base de données configurée et importée
- [ ] Fichiers media transférés
- [ ] Variables d'environnement configurées
- [ ] Migrations appliquées
- [ ] Static files collectés
- [ ] Gunicorn + Supervisor opérationnels
- [ ] Nginx configuré
- [ ] SSL/HTTPS activé
- [ ] DNS configuré
- [ ] Firewall activé
- [ ] Backups configurés
- [ ] Tests de fonctionnement OK
- [ ] Monitoring en place

## 🎯 Prochaines Étapes

1. ✅ Backend déployé sur Nidohost
2. ⏳ Frontend à déployer sur Vercel
3. ⏳ Configuration DNS complète
4. ⏳ Tests end-to-end
5. ⏳ Documentation utilisateur

---

**Status**: 🚀 Ready for Production

**Dernière mise à jour**: Décembre 2025

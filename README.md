# 🛍️ Goback Backend - E-commerce Django API

Backend Django pour la plateforme e-commerce Goback (Sacs, Valises et Bagages).

## 🌐 URLs de Production

- **API Backend**: https://api.gobag.ma
- **Admin Panel**: https://api.gobag.ma/admin/
- **Frontend**: https://gobag.ma

## 🚀 Déploiement sur Nidohost

### 📖 Documentation Complète

Le backend est configuré et prêt pour le déploiement sur Nidohost. Consultez:

1. **[FEUILLE_DE_ROUTE.md](./FEUILLE_DE_ROUTE.md)** - Plan d'action complet avec timeline
2. **[GUIDE_RAPIDE.md](./GUIDE_RAPIDE.md)** - Commandes essentielles
3. **[DEPLOIEMENT_NIDOHOST.md](./DEPLOIEMENT_NIDOHOST.md)** - Guide détaillé étape par étape
4. **[PRODUCTION.md](./PRODUCTION.md)** - Architecture et configuration production

### ⚡ Démarrage Rapide

#### Sur Windows (Préparation):

```powershell
cd C:\Users\MSI\Desktop\goback\goback_backend
.\prepare_upload.ps1
```

#### Sur le Serveur Nidohost:

```bash
ssh gobagma@176.9.31.158
cd /home/gobagma
git clone https://github.com/votre-repo/goback_backend.git
cd goback_backend
./deploy.sh
```

Suivez ensuite les instructions dans [GUIDE_RAPIDE.md](./GUIDE_RAPIDE.md)

## 📦 Technologies

- **Framework**: Django 4.2+
- **Database**: MySQL 8.0+
- **WSGI Server**: Gunicorn
- **Web Server**: Nginx
- **Process Manager**: Supervisor
- **SSL**: Let's Encrypt (Certbot)
- **API**: Django REST Framework
- **Admin**: Django Jazzmin

## 🏗️ Architecture Production

```
Internet (HTTPS) → Nginx (443) → Gunicorn (8000) → Django → MySQL
```

## 📂 Structure du Projet

```
goback_backend/
├── config/              # Configuration Django
│   ├── settings.py     # Settings avec support .env
│   ├── urls.py
│   └── wsgi.py
├── shop/               # App principale (produits, catégories)
├── orders/             # App gestion des commandes
├── admin_panel/        # Panel d'administration personnalisé
├── media/              # Fichiers uploadés
├── templates/          # Templates Django
├── manage.py
├── requirements.txt    # Dépendances Python
├── .env.production     # Template variables production
├── gunicorn_config.py  # Configuration Gunicorn
├── supervisor_goback.conf  # Configuration Supervisor
├── nginx_goback.conf   # Configuration Nginx
├── deploy.sh           # Script de déploiement
├── backup.sh           # Script de backup
├── verify_deployment.sh # Script de vérification
└── prepare_upload.ps1  # Script Windows de préparation
```

## 🔧 Installation Locale (Développement)

### Prérequis

- Python 3.11+
- MySQL 8.0+
- pip

### Installation

```bash
# Clone
git clone https://github.com/votre-repo/goback_backend.git
cd goback_backend

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos valeurs

# Base de données
python manage.py migrate

# Collecter static files
python manage.py collectstatic

# Créer superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

Accédez à:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## 🔐 Variables d'Environnement

Créez un fichier `.env` avec:

```ini
# Django
SECRET_KEY=votre-cle-secrete-unique
DEBUG=True  # False en production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=goback_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# Static & Media
STATIC_URL=/static/
MEDIA_URL=/media/
```

## 📡 API Endpoints

### Produits
- `GET /api/products/` - Liste des produits
- `GET /api/products/{id}/` - Détail produit
- `GET /api/products/by-sku/{sku}/` - Produit par SKU

### Catégories
- `GET /api/categories/` - Liste des catégories
- `GET /api/categories/{id}/` - Détail catégorie

### Sous-catégories
- `GET /api/subcategories/` - Liste des sous-catégories
- `GET /api/subcategories/{id}/` - Détail sous-catégorie

### Marques
- `GET /api/brands/` - Liste des marques
- `GET /api/brands/{id}/` - Détail marque

### Collections
- `GET /api/collections/` - Liste des collections
- `GET /api/collections/{id}/` - Détail collection

### Sliders
- `GET /api/hero-slides/` - Slides hero

### Commandes
- `POST /api/orders/` - Créer une commande

## 🛡️ Sécurité Production

- ✅ DEBUG=False
- ✅ SECRET_KEY unique et sécurisée
- ✅ HTTPS via Let's Encrypt
- ✅ CORS configuré
- ✅ CSRF protection
- ✅ Headers de sécurité (Nginx)
- ✅ Firewall (UFW)
- ✅ SQL Injection protection (Django ORM)
- ✅ XSS protection

## 📊 Monitoring

### Logs

```bash
# Gunicorn
tail -f /home/gobagma/logs/gunicorn_error.log

# Nginx
tail -f /home/gobagma/logs/nginx_error.log

# Supervisor
tail -f /home/gobagma/logs/supervisor_goback.log
```

### Status des Services

```bash
sudo supervisorctl status goback
sudo systemctl status nginx
```

## 💾 Backups

Backup automatique configuré (quotidien à 2h):
- Base de données MySQL
- Fichiers media
- Rétention: 7 jours

Script: [backup.sh](./backup.sh)

## 🔄 Mise à Jour du Code

```bash
cd /home/gobagma/goback_backend
git pull origin master
source /home/gobagma/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart goback
```

## 🧪 Tests

```bash
# Vérification Django
python manage.py check

# Vérification base de données
python manage.py check --database default

# Migrations
python manage.py showmigrations

# Tests automatisés
python manage.py test
```

## 📱 Frontend

Le frontend Next.js est disponible dans: `../goback_frontend/`

Déploiement recommandé sur Vercel avec:
- `NEXT_PUBLIC_API_URL=https://api.gobag.ma`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est privé et propriétaire.

## 👥 Auteurs

- **Équipe Goback** - Développement initial

## 🆘 Support

Pour toute question ou problème:
1. Consultez la documentation dans `/docs`
2. Vérifiez les logs
3. Ouvrez une issue sur GitHub

## 📅 Roadmap

- [x] Configuration Django de base
- [x] Modèles de données
- [x] API REST
- [x] Admin panel personnalisé
- [x] Configuration production
- [x] Scripts de déploiement
- [ ] Déploiement sur Nidohost
- [ ] Tests unitaires
- [ ] CI/CD
- [ ] Documentation API (Swagger)
- [ ] Monitoring avancé

## ✅ Status

**Production**: Ready to Deploy 🚀

---

**Dernière mise à jour**: Décembre 2025

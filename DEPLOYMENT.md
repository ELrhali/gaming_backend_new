# Déploiement en Production - PC Store

## ⚠️ Avant de déployer

### 1. Sécurité

#### Changer la SECRET_KEY
Dans `config/settings.py`:
```python
# NE PAS utiliser cette clé en production!
# Générez une nouvelle clé avec:
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

SECRET_KEY = 'votre-nouvelle-cle-secrete-tres-longue'
```

#### Désactiver le mode DEBUG
```python
DEBUG = False
```

#### Configurer ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['votredomaine.com', 'www.votredomaine.com', 'votre-ip']
```

#### Configurer CSRF_TRUSTED_ORIGINS (Django 4.0+)
```python
CSRF_TRUSTED_ORIGINS = [
    'https://votredomaine.com',
    'https://www.votredomaine.com'
]
```

### 2. Base de Données

#### Option 1: MySQL en production
Créez un utilisateur MySQL dédié:
```sql
CREATE USER 'pcstore_user'@'localhost' IDENTIFIED BY 'mot_de_passe_fort';
GRANT ALL PRIVILEGES ON pc_store_db.* TO 'pcstore_user'@'localhost';
FLUSH PRIVILEGES;
```

Mettez à jour `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pc_store_db',
        'USER': 'pcstore_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),  # Utilisez des variables d'environnement
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. Fichiers Statiques et Média

#### Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

#### Configurer le serveur pour servir les médias
Utilisez Nginx ou Apache pour servir `/media/` et `/static/`

Exemple Nginx:
```nginx
location /static/ {
    alias /chemin/vers/backend/staticfiles/;
}

location /media/ {
    alias /chemin/vers/backend/media/;
}
```

### 4. Variables d'Environnement

Créez un fichier `.env`:
```env
SECRET_KEY=votre-cle-secrete
DEBUG=False
DB_NAME=pc_store_db
DB_USER=pcstore_user
DB_PASSWORD=mot_de_passe_fort
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
```

Installez python-decouple:
```bash
pip install python-decouple
```

Modifiez `settings.py`:
```python
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

### 5. HTTPS

Activez HTTPS avec Let's Encrypt (gratuit):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

Dans `settings.py`:
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

## 🚀 Options de Déploiement

### Option 1: VPS avec Gunicorn + Nginx

#### Installer Gunicorn
```bash
pip install gunicorn
```

#### Créer un fichier gunicorn_config.py
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
max_requests = 1000
timeout = 30
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
```

#### Lancer Gunicorn
```bash
gunicorn config.wsgi:application -c gunicorn_config.py
```

#### Configurer Nginx
```nginx
server {
    listen 80;
    server_name votredomaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /chemin/vers/backend/staticfiles/;
    }

    location /media/ {
        alias /chemin/vers/backend/media/;
    }
}
```

#### Créer un service systemd
Fichier `/etc/systemd/system/pcstore.service`:
```ini
[Unit]
Description=PC Store Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/chemin/vers/backend
Environment="PATH=/chemin/vers/venv/bin"
ExecStart=/chemin/vers/venv/bin/gunicorn config.wsgi:application -c gunicorn_config.py

[Install]
WantedBy=multi-user.target
```

Activer et démarrer:
```bash
sudo systemctl enable pcstore
sudo systemctl start pcstore
sudo systemctl status pcstore
```

### Option 2: Docker

#### Créer un Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Créer docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: pc_store_db
      MYSQL_USER: pcstore_user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql_data:/var/lib/mysql

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_PORT=3306

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### Option 3: Hébergement Managé

#### PythonAnywhere
1. Uploadez votre code
2. Créez un virtual environment
3. Installez les dépendances
4. Configurez la WSGI
5. Ajoutez les mappings pour /static/ et /media/

#### Heroku
```bash
# Installer Heroku CLI
# Créer Procfile
echo "web: gunicorn config.wsgi" > Procfile

# Créer runtime.txt
echo "python-3.11.0" > runtime.txt

# Déployer
heroku create votre-app-name
heroku addons:create jawsdb:kitefin  # MySQL
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 📊 Monitoring et Maintenance

### Logs
```bash
# Voir les logs en temps réel
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/error.log
```

### Sauvegarde de la base de données
```bash
# Créer un backup
mysqldump -u pcstore_user -p pc_store_db > backup_$(date +%Y%m%d).sql

# Restaurer un backup
mysql -u pcstore_user -p pc_store_db < backup_20231115.sql
```

### Script de backup automatique
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u pcstore_user -p'password' pc_store_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
find $BACKUP_DIR -mtime +7 -delete  # Supprimer les backups de plus de 7 jours
```

Ajouter au crontab:
```bash
0 2 * * * /chemin/vers/backup.sh
```

## 🔧 Performance

### Cache avec Redis
```bash
pip install django-redis
```

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Compression
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... autres middleware
]
```

## ✅ Checklist de Déploiement

- [ ] SECRET_KEY changée
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configuré
- [ ] Base de données sécurisée
- [ ] Variables d'environnement configurées
- [ ] Fichiers statiques collectés
- [ ] HTTPS activé
- [ ] Backups automatiques configurés
- [ ] Monitoring en place
- [ ] Logs configurés
- [ ] Tests effectués
- [ ] Documentation mise à jour

## 🆘 Support

Pour plus d'aide:
- Documentation Django: https://docs.djangoproject.com
- Django Deployment Checklist: `python manage.py check --deploy`

# 📋 FEUILLE DE ROUTE - DÉPLOIEMENT GOBACK

## ✅ BACKEND - PRÉPARATION COMPLÈTE

### Fichiers créés pour le déploiement:

| Fichier | Description | Status |
|---------|-------------|--------|
| `.env.production` | Template variables d'environnement | ✅ Créé |
| `gunicorn_config.py` | Configuration Gunicorn (WSGI) | ✅ Créé |
| `supervisor_goback.conf` | Configuration Supervisor | ✅ Créé |
| `nginx_goback.conf` | Configuration Nginx | ✅ Créé |
| `deploy.sh` | Script de déploiement | ✅ Créé |
| `backup.sh` | Script de backup automatique | ✅ Créé |
| `verify_deployment.sh` | Script de vérification | ✅ Créé |
| `connect_server.sh` | Script connexion SSH | ✅ Créé |
| `prepare_upload.ps1` | Script Windows préparation | ✅ Créé |
| `DEPLOIEMENT_NIDOHOST.md` | Guide complet | ✅ Créé |
| `GUIDE_RAPIDE.md` | Guide rapide | ✅ Créé |
| `PRODUCTION.md` | Documentation production | ✅ Créé |

---

## 🎯 PLAN D'ACTION - BACKEND

### Phase 1: Préparation Locale (Windows) ⏰ 15 min

```powershell
# Dans PowerShell, exécuter:
cd C:\Users\MSI\Desktop\goback\goback_backend

# Option A: Script automatique (Recommandé)
.\prepare_upload.ps1

# Option B: Manuel
mysqldump -u root -p goback_db > goback_db_backup.sql
Compress-Archive -Path .\media\* -DestinationPath media.zip

# Commit et push vers GitHub
git add .
git commit -m "Configuration production Nidohost"
git push origin master
```

**Résultat**: Fichiers SQL et ZIP prêts pour le transfert

---

### Phase 2: Configuration Serveur ⏰ 30-45 min

#### 2.1 Connexion au serveur

```bash
ssh gobagma@176.9.31.158
# Password: 3$lL_L3J~UU*
```

#### 2.2 Installation des dépendances

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y mysql-server libmysqlclient-dev
sudo apt install -y nginx supervisor git
```

#### 2.3 Configuration MySQL

```bash
sudo mysql -u root

# Dans MySQL:
CREATE DATABASE gobagma_goback_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gobagma_goback_user'@'localhost' IDENTIFIED BY 'VotreMotDePasseSecurisé123!';
GRANT ALL PRIVILEGES ON gobagma_goback_db.* TO 'gobagma_goback_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 2.4 Clone et configuration du projet

```bash
cd /home/gobagma
git clone https://github.com/votre-username/goback_backend.git
cd goback_backend

# Environnement Python
python3.11 -m venv /home/gobagma/venv
source /home/gobagma/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configuration .env
cp .env.production .env
nano .env  # Éditer avec vos valeurs
```

**Résultat**: Environnement configuré sur le serveur

---

### Phase 3: Transfert des Données ⏰ 20-30 min

#### 3.1 Transfert des fichiers

Utiliser **WinSCP** (recommandé):
1. Télécharger: https://winscp.net/
2. Connexion:
   - Protocole: SFTP
   - Hôte: 176.9.31.158
   - Port: 22
   - Username: gobagma
   - Password: 3$lL_L3J~UU*

3. Transférer:
   - `goback_db_backup.sql` → `/home/gobagma/`
   - `media.zip` → `/home/gobagma/`

#### 3.2 Import de la base de données

```bash
cd /home/gobagma
mysql -u gobagma_goback_user -p gobagma_goback_db < goback_db_backup.sql
rm goback_db_backup.sql
```

#### 3.3 Extraction des fichiers media

```bash
mkdir -p /home/gobagma/public_html/backend/media
unzip /home/gobagma/media.zip -d /home/gobagma/public_html/backend/media/
rm /home/gobagma/media.zip
chmod -R 755 /home/gobagma/public_html/backend/media
```

**Résultat**: Base de données et media transférés

---

### Phase 4: Configuration Django ⏰ 10 min

```bash
cd /home/gobagma/goback_backend
source /home/gobagma/venv/bin/activate

# Créer répertoires
mkdir -p /home/gobagma/logs /home/gobagma/run /home/gobagma/public_html/backend

# Migrations
python manage.py migrate

# Collecter static files
python manage.py collectstatic --noinput

# Créer superuser (si pas déjà dans la DB)
python manage.py createsuperuser
```

**Résultat**: Django configuré et prêt

---

### Phase 5: Services (Gunicorn + Nginx) ⏰ 15 min

#### 5.1 Supervisor (Gunicorn)

```bash
sudo cp supervisor_goback.conf /etc/supervisor/conf.d/goback.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start goback
sudo supervisorctl status goback
```

#### 5.2 Nginx

```bash
sudo cp nginx_goback.conf /etc/nginx/sites-available/goback
sudo ln -s /etc/nginx/sites-available/goback /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Résultat**: Backend accessible via HTTP

---

### Phase 6: SSL/HTTPS ⏰ 5 min

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.gobag.ma
```

**Résultat**: Backend accessible via HTTPS

---

### Phase 7: Sécurité ⏰ 5 min

```bash
# Firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# MySQL sécurisation
sudo mysql_secure_installation
```

**Résultat**: Serveur sécurisé

---

### Phase 8: Vérification ⏰ 5 min

```bash
cd /home/gobagma/goback_backend
chmod +x verify_deployment.sh
./verify_deployment.sh
```

**Tests manuels**:

```bash
# Test local
curl http://127.0.0.1:8000/api/products/

# Test HTTPS
curl https://api.gobag.ma/api/products/

# Accès admin
# Browser: https://api.gobag.ma/admin/
```

**Résultat**: Backend 100% fonctionnel ✅

---

## 🌐 DNS - CONFIGURATION REQUISE

### Chez votre registrar de domaine (gobag.ma):

| Type | Nom | Valeur | TTL |
|------|-----|--------|-----|
| A | api | 176.9.31.158 | 3600 |
| A | @ | (Vercel IP) | 3600 |
| CNAME | www | gobag.ma | 3600 |

**Propagation DNS**: 15 min à 48h (généralement < 2h)

---

## ⏭️ PROCHAINE ÉTAPE: FRONTEND SUR VERCEL

### Configuration Frontend:

1. **Aller sur**: https://vercel.com
2. **Importer**: Repository `goback_frontend`
3. **Framework**: Next.js
4. **Build Command**: `npm run build`
5. **Output Directory**: `.next`

6. **Environment Variables**:
```
NEXT_PUBLIC_API_URL=https://api.gobag.ma
```

7. **Custom Domain**:
   - Ajouter: `gobag.ma`
   - Ajouter: `www.gobag.ma`

8. **DNS Configuration**:
   - Suivre les instructions Vercel
   - Pointer les records A/CNAME vers Vercel

---

## 📊 TIMELINE ESTIMÉ

| Phase | Durée | Status |
|-------|-------|--------|
| Préparation locale | 15 min | ⏳ À faire |
| Configuration serveur | 30-45 min | ⏳ À faire |
| Transfert données | 20-30 min | ⏳ À faire |
| Configuration Django | 10 min | ⏳ À faire |
| Services (Nginx/Gunicorn) | 15 min | ⏳ À faire |
| SSL/HTTPS | 5 min | ⏳ À faire |
| Sécurité | 5 min | ⏳ À faire |
| Vérification | 5 min | ⏳ À faire |
| **TOTAL BACKEND** | **~2h** | ⏳ |
| Frontend Vercel | 20 min | ⏳ À faire |
| DNS Configuration | 2-48h | ⏳ À faire |
| **TOTAL PROJET** | **~2h30 + DNS** | ⏳ |

---

## 🎯 CHECKLIST COMPLÈTE

### Backend Nidohost

- [ ] 1. Fichiers SQL et media exportés
- [ ] 2. Connexion SSH réussie
- [ ] 3. Dépendances système installées
- [ ] 4. MySQL configuré et DB créée
- [ ] 5. Projet cloné depuis GitHub
- [ ] 6. Environnement Python créé
- [ ] 7. Requirements.txt installés
- [ ] 8. Fichier .env configuré
- [ ] 9. Base de données importée
- [ ] 10. Fichiers media transférés
- [ ] 11. Migrations Django appliquées
- [ ] 12. Static files collectés
- [ ] 13. Supervisor configuré
- [ ] 14. Nginx configuré
- [ ] 15. SSL/HTTPS activé
- [ ] 16. Firewall configuré
- [ ] 17. Tests de vérification OK
- [ ] 18. Backup automatique configuré

### Frontend Vercel

- [ ] 19. Repository importé sur Vercel
- [ ] 20. Variables d'environnement configurées
- [ ] 21. Build réussi
- [ ] 22. Domain gobag.ma ajouté
- [ ] 23. Domain www.gobag.ma ajouté
- [ ] 24. DNS configuré

### Post-Déploiement

- [ ] 25. Test API depuis frontend
- [ ] 26. Test commande depuis site
- [ ] 27. Test admin panel
- [ ] 28. Test upload images
- [ ] 29. Vérification SEO
- [ ] 30. Monitoring configuré

---

## 📚 DOCUMENTATION DISPONIBLE

1. **DEPLOIEMENT_NIDOHOST.md** - Guide complet étape par étape
2. **GUIDE_RAPIDE.md** - Commandes essentielles
3. **PRODUCTION.md** - Architecture et infos production
4. **Ce fichier** - Feuille de route et checklist

---

## 🆘 EN CAS DE PROBLÈME

### Logs à vérifier:

```bash
# Gunicorn
tail -f /home/gobagma/logs/gunicorn_error.log

# Nginx
tail -f /home/gobagma/logs/nginx_error.log

# Supervisor
tail -f /home/gobagma/logs/supervisor_goback.log
```

### Commandes de diagnostic:

```bash
sudo supervisorctl status
sudo systemctl status nginx
netstat -tlnp | grep 8000
python manage.py check
```

### Redémarrage:

```bash
sudo supervisorctl restart goback
sudo systemctl restart nginx
```

---

## 🎉 SUCCÈS!

Une fois tout terminé:

✅ Backend: https://api.gobag.ma/admin/
✅ Frontend: https://gobag.ma
✅ API: https://api.gobag.ma/api/products/

**Félicitations! Votre e-commerce est en ligne!** 🚀

---

**Date de création**: Décembre 2025
**Dernière mise à jour**: Décembre 2025
**Status**: 📋 Prêt pour le déploiement

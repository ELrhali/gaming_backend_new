# Guide de Démarrage Rapide - PC Store

## 🚀 Installation en 5 minutes

### Étape 1: Préparer MySQL
```sql
-- Connectez-vous à MySQL et exécutez:
CREATE DATABASE pc_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Étape 2: Configurer les identifiants
Ouvrez `config/settings.py` et modifiez la section DATABASES:
```python
DATABASES = {
    'default': {
        'NAME': 'pc_store_db',
        'USER': 'root',              # Votre utilisateur MySQL
        'PASSWORD': 'votre_password', # Votre mot de passe MySQL
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Étape 3: Lancer le script d'installation
```powershell
.\setup.ps1
```

Le script va:
- ✓ Créer l'environnement virtuel
- ✓ Installer toutes les dépendances
- ✓ Créer les dossiers nécessaires
- ✓ Créer les tables de la base de données
- ✓ Créer un compte administrateur

### Étape 4: Démarrer le serveur
```powershell
python manage.py runserver
```

### Étape 5: Accéder à l'interface admin
Ouvrez votre navigateur: **http://127.0.0.1:8000/admin-panel/login/**

---

## 📝 Première Configuration

### 1. Créer les catégories principales
- Composants
- PC
- Périphériques
- Accessoires

### 2. Ajouter des sous-catégories
Exemples pour Composants:
- Cartes Mères
- Cartes Graphiques
- Mémoire RAM
- Processeurs
- etc.

### 3. Ajouter des types/marques
Exemples pour Cartes Mères:
- Carte Mère AMD
- Carte Mère Intel

### 4. Ajouter vos premiers produits
Avec tous les détails: référence, prix, stock, images, etc.

---

## 🎯 Fonctionnalités Principales

### Dashboard
- Vue d'ensemble des statistiques
- Dernières commandes
- Best sellers

### Gestion Catalogue
- ✅ Catégories avec images
- ✅ Sous-catégories avec images
- ✅ Types/Marques
- ✅ Produits complets
- ✅ Collections

### Gestion Commandes
- ✅ Liste de toutes les commandes
- ✅ Détails client et produits
- ✅ Confirmation/Annulation
- ✅ Paiement COD uniquement

### Gestion Livraisons
- ✅ Suivi des colis
- ✅ Statuts de livraison
- ✅ Numéro de tracking
- ✅ Historique

---

## 🔐 Sécurité

- ✅ Authentification requise pour l'admin
- ✅ Accès restreint aux users staff
- ✅ Pas d'authentification côté client (COD seulement)

---

## 🆘 Problèmes Courants

### Erreur MySQL
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL")
```
**Solution**: Vérifiez que MySQL est démarré et que les identifiants sont corrects.

### Erreur mysqlclient
```
error: Microsoft Visual C++ 14.0 or greater is required
```
**Solution**: Installez MySQL Connector ou utilisez `pip install mysqlclient` avec les outils C++.

### Images ne s'affichent pas
**Solution**: Vérifiez que les dossiers `media/` existent et que `DEBUG = True` en développement.

---

## 📞 Commandes Utiles

### Créer un nouveau superuser
```powershell
python manage.py createsuperuser
```

### Réinitialiser la base de données
```powershell
python manage.py flush
```

### Collecter les fichiers statiques
```powershell
python manage.py collectstatic
```

### Voir les migrations
```powershell
python manage.py showmigrations
```

---

## 📚 Structure des URLs

- **Page d'accueil**: `/` (redirige vers dashboard ou login)
- **Admin Login**: `/admin-panel/login/`
- **Dashboard**: `/admin-panel/dashboard/`
- **Catégories**: `/admin-panel/categories/`
- **Produits**: `/admin-panel/products/`
- **Commandes**: `/admin-panel/orders/`
- **Livraisons**: `/admin-panel/deliveries/`
- **Utilisateurs**: `/admin-panel/users/`
- **Django Admin**: `/django-admin/` (interface par défaut)

---

## ✨ Prochaines Étapes

1. Ajoutez vos catégories et produits
2. Testez la création de commandes
3. Gérez les livraisons
4. Personnalisez le design si nécessaire
5. Configurez pour la production

---

Bonne chance avec votre boutique PC Store! 🎉

# PC Store - Site E-commerce Django

Site web e-commerce pour la vente de composants PC, périphériques et accessoires informatiques.

## 🚀 Fonctionnalités

### Interface Admin
- **Dashboard** : Vue d'ensemble des statistiques (produits, commandes, revenus)
- **Gestion des catégories** : 4 catégories principales (Composants, PC, Périphériques, Accessoires)
- **Gestion des sous-catégories** : Organisation hiérarchique avec images
- **Gestion des types** : Marques et modèles spécifiques
- **Gestion des produits** : Catalogue complet avec :
  - Référence, nom, description, caractéristiques
  - Prix, prix promo, stock
  - Images (principale + galerie)
  - Statuts (en stock, rupture, etc.)
  - Best sellers, nouveautés
- **Gestion des commandes** : 
  - Visualisation de toutes les commandes
  - Informations clients complètes
  - Confirmation/Annulation
  - Paiement à la livraison (COD)
- **Gestion des livraisons** :
  - Suivi des colis
  - Numéro de tracking
  - Statuts de livraison
  - Historique

### Sécurité
- Authentification admin uniquement (pas d'authentification client)
- Accès restreint aux utilisateurs staff

## 📋 Prérequis

- Python 3.8+
- MySQL 5.7+ ou MariaDB
- pip

## 🔧 Installation

### 1. Créer et activer un environnement virtuel

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

### 3. Configurer MySQL

Créez une base de données MySQL :

```sql
CREATE DATABASE pc_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Configurer les paramètres

Modifiez `config/settings.py` avec vos identifiants MySQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pc_store_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Créer les tables de la base de données

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur

```powershell
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte admin.

### 7. Créer les dossiers média et statique

```powershell
New-Item -ItemType Directory -Path "media", "static", "media\categories", "media\subcategories", "media\products"
```

### 8. Lancer le serveur

```powershell
python manage.py runserver
```

Le site sera accessible sur : http://127.0.0.1:8000

## 🔐 Accès Admin

- URL : http://127.0.0.1:8000/admin-panel/login/
- Utilisez les identifiants du superutilisateur créé à l'étape 6

## 📁 Structure du Projet

```
backend/
├── config/              # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                # Application catalogue
│   ├── models.py       # Category, SubCategory, Type, Product
│   └── admin.py
├── orders/              # Application commandes
│   ├── models.py       # Order, OrderItem, Customer, Delivery
│   └── admin.py
├── admin_panel/         # Interface admin personnalisée
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/           # Templates HTML
│   └── admin_panel/
├── media/              # Fichiers uploadés (images)
├── static/             # Fichiers statiques (CSS, JS)
└── manage.py
```

## 🗂️ Structure des Catégories

### Composants
- Cartes Mères (AMD, Intel)
- Cartes Graphiques (GeForce GTX, RTX)
- Mémoire RAM (DDR4, DDR5)
- Processeurs (i3, i5, i7, i9, Ryzen 3/5/7/9, Threadripper)
- Boîtiers (E-ATX, ATX, Mini-ITX)
- Alimentation PC (Bronze, Gold, Platinum)
- Stockage (HDD, SSD, NVME)
- Cooling (Air, Liquid, Ventilateurs)

### Périphériques
- Écran PC (4K, Full HD, QHD, différentes tailles)
- Clavier PC (Mécanique, Membrane, RGB, Wireless)
- Souris Gamer (Bluetooth, USB)
- Webcam PC
- Microphone PC
- Casque PC
- Enceinte Audio
- Tapis de souris
- Bundle PC
- Modem & routeur
- Video Surveillance
- Stockage externe (HDD, SSD)

### Accessoires
- Câbles
- Pâtes Thermiques
- Lecteur DVD
- Sac à dos
- Support Moniteurs
- Streaming (Microphones, Capture Card, Carte Son, Green Screen)

## 📊 Modèles de Données

### Product (Produit)
- Référence unique
- Nom, description, caractéristiques
- Meta (SEO)
- Catégorie, sous-catégorie, type
- Prix, prix promo
- Stock, statut
- Best seller, featured, nouveau
- Images
- Marque, garantie, poids

### Order (Commande)
- Numéro de commande unique
- Client (nom, téléphone, adresse)
- Statut (en attente, confirmée, livrée, etc.)
- Mode de paiement (COD)
- Montants (sous-total, frais livraison, total)
- Notes

### Delivery (Livraison)
- Numéro de suivi
- Statut
- Transporteur
- Dates (expédition, livraison)
- Nombre de colis

## 🛠️ Commandes Utiles

### Créer des migrations
```powershell
python manage.py makemigrations
```

### Appliquer les migrations
```powershell
python manage.py migrate
```

### Collecter les fichiers statiques
```powershell
python manage.py collectstatic
```

### Créer un dump de la base de données
```powershell
python manage.py dumpdata > backup.json
```

### Restaurer les données
```powershell
python manage.py loaddata backup.json
```

## 📝 Notes Importantes

1. **Sécurité** : Changez `SECRET_KEY` dans `settings.py` pour la production
2. **Debug** : Mettez `DEBUG = False` en production
3. **Allowed Hosts** : Configurez `ALLOWED_HOSTS` pour votre domaine
4. **Media Files** : Configurez un stockage approprié (S3, etc.) pour la production
5. **Base de données** : Sauvegardez régulièrement votre base de données

## 🎨 Personnalisation

Le design utilise Bootstrap 5 et Bootstrap Icons. Vous pouvez personnaliser :
- Les couleurs dans `templates/admin_panel/base.html`
- Les styles dans la section `<style>` du template de base
- Ajouter votre propre CSS dans `static/css/`

## 📞 Support

Pour toute question ou problème, créez une issue dans le repository.

## 📄 Licence

Ce projet est sous licence MIT.

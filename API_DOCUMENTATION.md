# Structure de l'API - PC Store Admin Panel

Ce document décrit la structure de l'application et les URLs disponibles.

## 🔐 Authentification

### URLs d'authentification
- **POST** `/admin-panel/login/` - Connexion admin
- **GET** `/admin-panel/logout/` - Déconnexion admin

**Note:** Seuls les utilisateurs avec `is_staff=True` peuvent se connecter.

---

## 📊 Dashboard

### URLs du dashboard
- **GET** `/admin-panel/dashboard/` - Vue d'ensemble avec statistiques

**Statistiques affichées:**
- Total des produits
- Total des commandes
- Commandes en attente
- Revenu total
- Dernières commandes (10)
- Best sellers (5)

---

## 🗂️ Gestion des Catégories

### URLs des catégories
- **GET** `/admin-panel/categories/` - Liste toutes les catégories
- **GET** `/admin-panel/categories/add/` - Formulaire d'ajout
- **POST** `/admin-panel/categories/add/` - Créer une catégorie
- **GET** `/admin-panel/categories/<id>/edit/` - Formulaire d'édition
- **POST** `/admin-panel/categories/<id>/edit/` - Modifier une catégorie
- **GET** `/admin-panel/categories/<id>/delete/` - Confirmation de suppression
- **POST** `/admin-panel/categories/<id>/delete/` - Supprimer une catégorie

**Modèle Category:**
```python
{
    "id": int,
    "name": str,
    "slug": str,
    "image": ImageField,
    "description": str,
    "order": int,
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## 📑 Gestion des Sous-catégories

### URLs des sous-catégories
- **GET** `/admin-panel/subcategories/` - Liste toutes les sous-catégories
- **GET** `/admin-panel/subcategories/add/` - Formulaire d'ajout
- **POST** `/admin-panel/subcategories/add/` - Créer une sous-catégorie
- **GET** `/admin-panel/subcategories/<id>/edit/` - Formulaire d'édition
- **POST** `/admin-panel/subcategories/<id>/edit/` - Modifier une sous-catégorie
- **GET** `/admin-panel/subcategories/<id>/delete/` - Confirmation
- **POST** `/admin-panel/subcategories/<id>/delete/` - Supprimer

**Modèle SubCategory:**
```python
{
    "id": int,
    "category": ForeignKey(Category),
    "name": str,
    "slug": str,
    "image": ImageField,
    "description": str,
    "order": int,
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## 🏷️ Gestion des Types

### URLs des types
- **GET** `/admin-panel/types/` - Liste tous les types
- **GET** `/admin-panel/types/add/` - Formulaire d'ajout
- **POST** `/admin-panel/types/add/` - Créer un type
- **GET** `/admin-panel/types/<id>/edit/` - Formulaire d'édition
- **POST** `/admin-panel/types/<id>/edit/` - Modifier un type
- **GET** `/admin-panel/types/<id>/delete/` - Confirmation
- **POST** `/admin-panel/types/<id>/delete/` - Supprimer

**Modèle Type:**
```python
{
    "id": int,
    "subcategory": ForeignKey(SubCategory),
    "name": str,
    "slug": str,
    "description": str,
    "order": int,
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## 📦 Gestion des Produits

### URLs des produits
- **GET** `/admin-panel/products/` - Liste tous les produits
  - Paramètres de requête:
    - `?search=terme` - Recherche dans nom/référence/description
    - `?category=id` - Filtrer par catégorie
    - `?subcategory=id` - Filtrer par sous-catégorie
- **GET** `/admin-panel/products/add/` - Formulaire d'ajout
- **POST** `/admin-panel/products/add/` - Créer un produit
- **GET** `/admin-panel/products/<id>/edit/` - Formulaire d'édition
- **POST** `/admin-panel/products/<id>/edit/` - Modifier un produit
- **GET** `/admin-panel/products/<id>/delete/` - Confirmation
- **POST** `/admin-panel/products/<id>/delete/` - Supprimer

**Modèle Product:**
```python
{
    "id": int,
    "reference": str (unique),
    "name": str,
    "slug": str,
    "meta_title": str,
    "meta_description": str,
    "description": str,
    "caracteristiques": str,
    "category": ForeignKey(Category),
    "subcategory": ForeignKey(SubCategory),
    "type": ForeignKey(Type, optional),
    "collection": ForeignKey(Collection, optional),
    "price": Decimal,
    "discount_price": Decimal (optional),
    "quantity": int,
    "status": str,  # in_stock, out_of_stock, preorder, discontinued
    "is_bestseller": bool,
    "is_featured": bool,
    "is_new": bool,
    "main_image": ImageField,
    "brand": str,
    "warranty": str,
    "weight": Decimal,
    "views_count": int,
    "created_at": datetime,
    "updated_at": datetime
}
```

**Propriétés calculées:**
- `final_price` - Prix final (avec ou sans promo)
- `discount_percentage` - Pourcentage de réduction

---

## 🛒 Gestion des Commandes

### URLs des commandes
- **GET** `/admin-panel/orders/` - Liste toutes les commandes
  - Paramètres de requête:
    - `?status=pending|confirmed|preparing|shipped|delivered|cancelled`
- **GET** `/admin-panel/orders/<id>/` - Détails d'une commande
- **GET** `/admin-panel/orders/<id>/confirm/` - Confirmation
- **POST** `/admin-panel/orders/<id>/confirm/` - Confirmer une commande
- **GET** `/admin-panel/orders/<id>/cancel/` - Confirmation
- **POST** `/admin-panel/orders/<id>/cancel/` - Annuler une commande

**Modèle Order:**
```python
{
    "id": int,
    "order_number": str (unique),
    "customer": ForeignKey(Customer),
    "status": str,  # pending, confirmed, preparing, ready, shipped, delivered, cancelled
    "payment_method": str,  # cod (Cash On Delivery)
    "subtotal": Decimal,
    "shipping_cost": Decimal,
    "total": Decimal,
    "customer_notes": str,
    "admin_notes": str,
    "created_at": datetime,
    "updated_at": datetime,
    "confirmed_at": datetime (optional)
}
```

**Modèle Customer:**
```python
{
    "id": int,
    "first_name": str,
    "last_name": str,
    "phone": str,
    "email": str (optional),
    "address": str,
    "city": str,
    "postal_code": str (optional),
    "notes": str,
    "created_at": datetime
}
```

**Modèle OrderItem:**
```python
{
    "id": int,
    "order": ForeignKey(Order),
    "product": ForeignKey(Product),
    "product_name": str,
    "product_reference": str,
    "unit_price": Decimal,
    "quantity": int,
    "total_price": Decimal
}
```

---

## 🚚 Gestion des Livraisons

### URLs des livraisons
- **GET** `/admin-panel/deliveries/` - Liste toutes les livraisons
  - Paramètres de requête:
    - `?status=pending|in_transit|delivered|failed|returned`
- **GET** `/admin-panel/deliveries/<id>/` - Détails d'une livraison
- **GET** `/admin-panel/deliveries/<id>/update/` - Formulaire de modification
- **POST** `/admin-panel/deliveries/<id>/update/` - Mettre à jour une livraison

**Modèle Delivery:**
```python
{
    "id": int,
    "order": OneToOneField(Order),
    "tracking_number": str,
    "status": str,  # pending, in_transit, delivered, failed, returned
    "shipped_at": datetime (optional),
    "delivered_at": datetime (optional),
    "package_count": int,
    "carrier": str,
    "notes": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

**Modèle DeliveryHistory:**
```python
{
    "id": int,
    "delivery": ForeignKey(Delivery),
    "status": str,
    "description": str,
    "created_at": datetime
}
```

---

## 📝 Formulaires

Tous les formulaires utilisent Bootstrap 5 avec les classes CSS appropriées.

### Validation des formulaires
- Les champs requis sont marqués avec `*`
- Les erreurs sont affichées en rouge sous chaque champ
- Les messages de succès/erreur sont affichés en haut de la page

---

## 🔒 Permissions

Toutes les vues nécessitent:
- Authentification (`@login_required`)
- Statut staff (`user.is_staff = True`)

---

## 📊 Messages Flash

L'application utilise le système de messages de Django:
- **success** - Opération réussie (vert)
- **error** - Erreur (rouge)
- **warning** - Avertissement (jaune)
- **info** - Information (bleu)

---

## 🎨 Templates

### Structure des templates
```
templates/
└── admin_panel/
    ├── base.html                    # Template de base
    ├── login.html                   # Page de connexion
    ├── dashboard.html               # Dashboard
    ├── category_list.html           # Liste des catégories
    ├── category_form.html           # Formulaire catégorie
    ├── category_confirm_delete.html # Confirmation suppression
    ├── subcategory_list.html        # Liste des sous-catégories
    ├── subcategory_form.html        # Formulaire sous-catégorie
    ├── subcategory_confirm_delete.html
    ├── type_list.html               # Liste des types
    ├── type_form.html               # Formulaire type
    ├── type_confirm_delete.html
    ├── product_list.html            # Liste des produits
    ├── product_form.html            # Formulaire produit
    ├── product_confirm_delete.html
    ├── order_list.html              # Liste des commandes
    ├── order_detail.html            # Détails commande
    ├── order_confirm.html           # Confirmation commande
    ├── order_cancel.html            # Annulation commande
    ├── delivery_list.html           # Liste des livraisons
    ├── delivery_detail.html         # Détails livraison
    └── delivery_form.html           # Formulaire livraison
```

### Blocs disponibles dans base.html
- `title` - Titre de la page
- `content` - Contenu principal
- `extra_js` - JavaScript supplémentaire

---

## 🎨 Design et UI

### Framework CSS
- Bootstrap 5.3.0
- Bootstrap Icons 1.11.0

### Couleurs principales
- Primaire: `#0d6efd` (bleu Bootstrap)
- Succès: `#28a745` (vert)
- Avertissement: `#ffc107` (jaune)
- Danger: `#dc3545` (rouge)
- Info: `#17a2b8` (cyan)

### Navigation
- Sidebar fixe à gauche
- Largeur: 3 colonnes (col-md-3)
- Contenu: 9 colonnes (col-md-9)

---

## 🔧 Personnalisation

### Ajouter un nouveau champ à Product
1. Modifier `shop/models.py`
2. Créer une migration: `python manage.py makemigrations`
3. Appliquer: `python manage.py migrate`
4. Mettre à jour `admin_panel/forms.py`
5. Mettre à jour le template `product_form.html`

### Ajouter un nouveau statut
Modifier les `CHOICES` dans le modèle:
```python
STATUS_CHOICES = [
    ('in_stock', 'En Stock'),
    ('nouveau_statut', 'Nouveau Statut'),
    # ...
]
```

---

## 📱 Responsive Design

L'interface est responsive et s'adapte aux différentes tailles d'écran:
- Desktop: Navigation sidebar + contenu
- Tablet: Navigation collapsible
- Mobile: Menu hamburger

---

## ⚡ Performance

### Optimisations implémentées
- `select_related()` pour les relations ForeignKey
- `prefetch_related()` pour les relations Many-to-Many
- Pagination (à implémenter si nécessaire)
- Cache des templates

### Recommandations
- Utiliser Redis pour le cache en production
- Compresser les images avant upload
- Utiliser un CDN pour les fichiers statiques
- Activer la compression Gzip

---

## 🐛 Debugging

### Mode DEBUG
En développement (`DEBUG=True`):
- Barre d'outils Django Debug Toolbar (optionnel)
- Messages d'erreur détaillés
- Fichiers statiques servis automatiquement

### Logs
Configurer les logs dans `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

---

## 📞 Support

Pour toute question sur l'API interne, consultez:
- Le code source dans `admin_panel/views.py`
- Les modèles dans `shop/models.py` et `orders/models.py`
- Les formulaires dans `admin_panel/forms.py`

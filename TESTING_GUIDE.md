# Guide de Test - PC Store

Ce guide vous aide à tester toutes les fonctionnalités du système.

---

## 🧪 Tests Manuels

### 1. Installation et Configuration

#### Test 1.1 : Installation
```powershell
# Exécuter le script d'installation
.\setup.ps1
```
**Résultat attendu** :
- ✅ Environnement virtuel créé
- ✅ Dépendances installées
- ✅ Dossiers média créés
- ✅ Migrations appliquées
- ✅ Superutilisateur créé

#### Test 1.2 : Lancement du serveur
```powershell
python manage.py runserver
```
**Résultat attendu** :
- ✅ Serveur démarre sur http://127.0.0.1:8000
- ✅ Aucune erreur dans la console

---

### 2. Authentification

#### Test 2.1 : Page de connexion
1. Accéder à `http://127.0.0.1:8000/admin-panel/login/`
2. Vérifier l'affichage de la page

**Résultat attendu** :
- ✅ Page de login s'affiche correctement
- ✅ Formulaire avec username et password
- ✅ Design moderne

#### Test 2.2 : Connexion réussie
1. Entrer les identifiants du superutilisateur
2. Cliquer sur "Se connecter"

**Résultat attendu** :
- ✅ Redirection vers le dashboard
- ✅ Message de bienvenue (optionnel)
- ✅ Sidebar visible

#### Test 2.3 : Connexion échouée
1. Entrer des identifiants incorrects
2. Cliquer sur "Se connecter"

**Résultat attendu** :
- ✅ Message d'erreur affiché
- ✅ Reste sur la page de login
- ✅ Pas de redirection

#### Test 2.4 : Protection des pages
1. Se déconnecter
2. Essayer d'accéder à `/admin-panel/dashboard/`

**Résultat attendu** :
- ✅ Redirection vers la page de login
- ✅ Pas d'accès au dashboard

---

### 3. Dashboard

#### Test 3.1 : Affichage des statistiques
1. Se connecter
2. Observer le dashboard

**Résultat attendu** :
- ✅ 4 cartes de statistiques affichées
- ✅ Nombres corrects (0 au début)
- ✅ Design cohérent

#### Test 3.2 : Dernières commandes
**Résultat attendu** :
- ✅ Section "Dernières commandes" visible
- ✅ Message "Aucune commande" si vide
- ✅ Table responsive

---

### 4. Gestion des Catégories

#### Test 4.1 : Liste vide
1. Aller sur "Catégories"

**Résultat attendu** :
- ✅ Message "Aucune catégorie"
- ✅ Bouton "Ajouter" visible

#### Test 4.2 : Ajouter une catégorie
1. Cliquer sur "Ajouter une catégorie"
2. Remplir le formulaire :
   - Nom : "Composants"
   - Description : "Tous les composants PC"
   - Ordre : 1
   - Cocher "Actif"
3. (Optionnel) Ajouter une image
4. Cliquer sur "Enregistrer"

**Résultat attendu** :
- ✅ Message de succès affiché
- ✅ Redirection vers la liste
- ✅ Catégorie visible dans la liste
- ✅ Image affichée si uploadée

#### Test 4.3 : Validation du formulaire
1. Essayer de créer une catégorie sans nom
2. Cliquer sur "Enregistrer"

**Résultat attendu** :
- ✅ Message d'erreur "Ce champ est requis"
- ✅ Formulaire non soumis

#### Test 4.4 : Modifier une catégorie
1. Cliquer sur l'icône "Modifier"
2. Changer le nom
3. Enregistrer

**Résultat attendu** :
- ✅ Message de succès
- ✅ Modifications enregistrées
- ✅ Changements visibles dans la liste

#### Test 4.5 : Supprimer une catégorie
1. Cliquer sur l'icône "Supprimer"
2. Confirmer la suppression

**Résultat attendu** :
- ✅ Page de confirmation affichée
- ✅ Message d'avertissement
- ✅ Catégorie supprimée après confirmation

---

### 5. Gestion des Sous-catégories

#### Test 5.1 : Ajouter une sous-catégorie
1. Créer une catégorie "Composants" si nécessaire
2. Aller sur "Sous-catégories"
3. Cliquer sur "Ajouter"
4. Remplir :
   - Catégorie : Sélectionner "Composants"
   - Nom : "Cartes Mères"
   - Ajouter une image
5. Enregistrer

**Résultat attendu** :
- ✅ Sous-catégorie créée
- ✅ Liée à la bonne catégorie
- ✅ Image affichée

#### Test 5.2 : Vérifier la hiérarchie
1. Observer la liste des sous-catégories

**Résultat attendu** :
- ✅ Catégorie parente affichée
- ✅ Tri par catégorie puis ordre

---

### 6. Gestion des Types

#### Test 6.1 : Ajouter un type
1. Créer sous-catégorie "Cartes Mères" si nécessaire
2. Aller sur "Types"
3. Ajouter :
   - Sous-catégorie : "Cartes Mères"
   - Nom : "Carte Mère AMD"
4. Enregistrer

**Résultat attendu** :
- ✅ Type créé
- ✅ Hiérarchie correcte affichée

---

### 7. Gestion des Produits

#### Test 7.1 : Ajouter un produit complet
1. Aller sur "Produits"
2. Cliquer sur "Ajouter"
3. Remplir tous les champs :
   - **Référence** : "CM-AMD-001"
   - **Nom** : "ASUS ROG STRIX B550-F GAMING"
   - **Image principale** : Upload une image
   - **Meta titre** : "Carte Mère AMD B550"
   - **Description** : Texte descriptif
   - **Caractéristiques** : Liste des specs
   - **Catégorie** : Composants
   - **Sous-catégorie** : Cartes Mères
   - **Type** : Carte Mère AMD
   - **Prix** : 2499.00
   - **Prix promo** : 2199.00
   - **Quantité** : 15
   - **Statut** : En Stock
   - **Cocher Best Seller**
   - **Marque** : ASUS
   - **Garantie** : 2 ans
4. Enregistrer

**Résultat attendu** :
- ✅ Produit créé avec succès
- ✅ Tous les champs sauvegardés
- ✅ Image affichée
- ✅ Badge "Best Seller" visible

#### Test 7.2 : Validation référence unique
1. Essayer de créer un produit avec la même référence

**Résultat attendu** :
- ✅ Erreur "Cette référence existe déjà"

#### Test 7.3 : Calcul du prix final
1. Observer le produit avec promo

**Résultat attendu** :
- ✅ Prix barré visible
- ✅ Prix promo en rouge
- ✅ Calcul correct

#### Test 7.4 : Recherche de produits
1. Utiliser le champ de recherche
2. Chercher "ASUS"

**Résultat attendu** :
- ✅ Résultats filtrés
- ✅ Seuls les produits correspondants affichés

#### Test 7.5 : Filtres par catégorie
1. Utiliser le filtre "Catégorie"
2. Sélectionner "Composants"

**Résultat attendu** :
- ✅ Seuls les produits de cette catégorie affichés

---

### 8. Gestion des Commandes

#### Test 8.1 : Créer une commande (via shell Django)
```python
python manage.py shell

from shop.models import Product
from orders.models import Customer, Order, OrderItem

# Créer un client
customer = Customer.objects.create(
    first_name="Ahmed",
    last_name="Bennani",
    phone="0612345678",
    address="123 Rue Mohammed V",
    city="Casablanca"
)

# Créer une commande
product = Product.objects.first()
order = Order.objects.create(
    customer=customer,
    subtotal=product.price,
    shipping_cost=50.00,
    total=product.price + 50,
    status='pending'
)

# Ajouter un article
OrderItem.objects.create(
    order=order,
    product=product,
    product_name=product.name,
    product_reference=product.reference,
    unit_price=product.price,
    quantity=1
)
```

#### Test 8.2 : Afficher les commandes
1. Aller sur "Commandes"

**Résultat attendu** :
- ✅ Commande visible dans la liste
- ✅ Numéro auto-généré
- ✅ Informations client affichées
- ✅ Statut correct

#### Test 8.3 : Détails de commande
1. Cliquer sur "Voir" pour une commande

**Résultat attendu** :
- ✅ Toutes les infos client affichées
- ✅ Liste des articles
- ✅ Calculs corrects (sous-total, frais, total)
- ✅ Boutons "Confirmer" et "Annuler" visibles

#### Test 8.4 : Confirmer une commande
1. Cliquer sur "Confirmer"
2. Confirmer l'action

**Résultat attendu** :
- ✅ Statut change à "Confirmée"
- ✅ Date de confirmation enregistrée
- ✅ Livraison créée automatiquement
- ✅ Message de succès

#### Test 8.5 : Annuler une commande
1. Créer une nouvelle commande
2. L'annuler

**Résultat attendu** :
- ✅ Statut change à "Annulée"
- ✅ Badge rouge affiché

#### Test 8.6 : Filtrer par statut
1. Utiliser le filtre de statut
2. Sélectionner "En attente"

**Résultat attendu** :
- ✅ Seules les commandes en attente affichées

---

### 9. Gestion des Livraisons

#### Test 9.1 : Voir les livraisons
1. Confirmer une commande d'abord
2. Aller sur "Livraisons"

**Résultat attendu** :
- ✅ Livraison automatiquement créée visible
- ✅ Statut "En attente"
- ✅ Lien avec la commande

#### Test 9.2 : Modifier une livraison
1. Cliquer sur "Gérer"
2. Cliquer sur "Modifier"
3. Remplir :
   - Numéro de suivi : "TRK123456789"
   - Statut : "En cours de livraison"
   - Transporteur : "Amana"
   - Date d'expédition : Sélectionner date
4. Enregistrer

**Résultat attendu** :
- ✅ Modifications enregistrées
- ✅ Statut mis à jour
- ✅ Informations visibles dans la liste

#### Test 9.3 : Marquer comme livrée
1. Modifier une livraison
2. Statut : "Livré"
3. Date de livraison : Date actuelle
4. Enregistrer

**Résultat attendu** :
- ✅ Statut "Livré" visible
- ✅ Badge vert affiché
- ✅ Date de livraison enregistrée

---

### 10. Tests d'Interface

#### Test 10.1 : Responsive Design
1. Réduire la fenêtre du navigateur
2. Tester sur mobile (F12 → Toggle device toolbar)

**Résultat attendu** :
- ✅ Interface s'adapte
- ✅ Navigation accessible
- ✅ Tables scrollables
- ✅ Formulaires utilisables

#### Test 10.2 : Navigation
1. Utiliser tous les liens de la sidebar

**Résultat attendu** :
- ✅ Tous les liens fonctionnent
- ✅ Lien actif surligné
- ✅ Pas d'erreurs 404

#### Test 10.3 : Messages Flash
1. Effectuer diverses actions

**Résultat attendu** :
- ✅ Messages de succès en vert
- ✅ Messages d'erreur en rouge
- ✅ Possibilité de fermer les messages

---

### 11. Tests de Performance

#### Test 11.1 : Temps de chargement
1. Observer le temps de chargement des pages

**Résultat attendu** :
- ✅ Pages chargent en moins de 2 secondes
- ✅ Images optimisées

#### Test 11.2 : Gestion de grands volumes
1. Créer 100+ produits (via script)
2. Tester la liste

**Résultat attendu** :
- ✅ Pas de ralentissement significatif
- ✅ Filtres fonctionnent bien

---

## 🤖 Tests Automatisés (Suggestion)

Pour ajouter des tests automatisés à l'avenir :

```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from shop.models import Category, Product

class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='admin',
            password='password',
            email='admin@test.com'
        )
    
    def test_login_required(self):
        response = self.client.get('/admin-panel/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get('/admin-panel/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_category(self):
        self.client.login(username='admin', password='password')
        response = self.client.post('/admin-panel/categories/add/', {
            'name': 'Test Category',
            'order': 1,
            'is_active': True
        })
        self.assertEqual(Category.objects.count(), 1)
```

Lancer les tests :
```powershell
python manage.py test
```

---

## ✅ Checklist Complète

### Installation
- [ ] Setup.ps1 exécuté avec succès
- [ ] Base de données créée
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Serveur démarre

### Authentification
- [ ] Login fonctionnel
- [ ] Logout fonctionnel
- [ ] Protection des pages OK

### Catégories
- [ ] Création OK
- [ ] Modification OK
- [ ] Suppression OK
- [ ] Upload image OK

### Sous-catégories
- [ ] Création OK
- [ ] Hiérarchie correcte
- [ ] Upload image OK

### Types
- [ ] Création OK
- [ ] Lien avec sous-catégorie OK

### Produits
- [ ] Création complète OK
- [ ] Images OK
- [ ] Prix/Promo OK
- [ ] Recherche OK
- [ ] Filtres OK

### Commandes
- [ ] Création OK
- [ ] Détails OK
- [ ] Confirmation OK
- [ ] Annulation OK
- [ ] Filtres OK

### Livraisons
- [ ] Création automatique OK
- [ ] Modification OK
- [ ] Suivi OK
- [ ] Statuts OK

### Interface
- [ ] Design cohérent
- [ ] Responsive OK
- [ ] Messages flash OK
- [ ] Navigation OK

---

## 🐛 Signaler un Bug

Si vous trouvez un bug :
1. Noter les étapes exactes pour le reproduire
2. Noter le message d'erreur
3. Vérifier les logs : `tail -f debug.log`
4. Documenter le comportement attendu vs réel

---

**Tous les tests passent ?** Félicitations, votre système est prêt! 🎉

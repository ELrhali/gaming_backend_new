# Exemples d'utilisation - Script Python pour gérer les produits
# À exécuter dans le shell Django: python manage.py shell

"""
Ce fichier contient des exemples de code pour manipuler les modèles.
Copiez et collez dans le shell Django pour tester.
"""

# ==================== EXEMPLES CATÉGORIES ====================

# Créer une catégorie
from shop.models import Category, SubCategory, Type, Product, Collection

category = Category.objects.create(
    name="Composants",
    description="Tous les composants PC",
    order=1,
    is_active=True
)

# Lister toutes les catégories
categories = Category.objects.all()
for cat in categories:
    print(f"{cat.name} - {cat.subcategories.count()} sous-catégories")

# ==================== EXEMPLES SOUS-CATÉGORIES ====================

# Créer une sous-catégorie
composants = Category.objects.get(name="Composants")
subcategory = SubCategory.objects.create(
    category=composants,
    name="Cartes Mères",
    description="Toutes les cartes mères",
    order=1,
    is_active=True
)

# ==================== EXEMPLES TYPES ====================

# Créer un type
cartes_meres = SubCategory.objects.get(name="Cartes Mères")
type_amd = Type.objects.create(
    subcategory=cartes_meres,
    name="Carte Mère AMD",
    order=1,
    is_active=True
)

# ==================== EXEMPLES PRODUITS ====================

# Créer un produit complet
product = Product.objects.create(
    reference="CM-AMD-001",
    name="Carte Mère ASUS ROG STRIX B550-F GAMING",
    meta_title="Carte Mère AMD B550 - ASUS ROG STRIX",
    meta_description="Carte mère gaming AMD B550, Socket AM4, ATX",
    description="Carte mère gaming haute performance pour processeurs AMD Ryzen",
    caracteristiques="""
    - Socket: AM4
    - Chipset: AMD B550
    - Format: ATX
    - Mémoire: 4x DDR4, Max 128GB
    - PCIe 4.0
    - RGB Aura Sync
    """,
    category=composants,
    subcategory=cartes_meres,
    type=type_amd,
    price=2499.00,
    discount_price=2199.00,
    quantity=15,
    status='in_stock',
    is_bestseller=True,
    brand="ASUS",
    warranty="2 ans"
)

# Créer un produit avec collection
collection = Collection.objects.create(
    name="Gaming Pro",
    description="Collection pour gamers professionnels"
)

product2 = Product.objects.create(
    reference="CG-RTX-001",
    name="NVIDIA GeForce RTX 4070 Ti",
    description="Carte graphique gaming haut de gamme",
    category=composants,
    subcategory=SubCategory.objects.get(name="Cartes Graphiques"),
    collection=collection,
    price=7999.00,
    quantity=8,
    status='in_stock',
    is_featured=True,
    is_new=True,
    brand="NVIDIA"
)

# ==================== RECHERCHE ET FILTRES ====================

# Trouver tous les best sellers
bestsellers = Product.objects.filter(is_bestseller=True)

# Trouver tous les produits en stock
in_stock = Product.objects.filter(status='in_stock', quantity__gt=0)

# Trouver produits par catégorie
composants_products = Product.objects.filter(category__name="Composants")

# Trouver produits avec promo
promo_products = Product.objects.filter(discount_price__isnull=False)

# Recherche par nom ou référence
search_results = Product.objects.filter(
    name__icontains="AMD"
) | Product.objects.filter(
    reference__icontains="AMD"
)

# ==================== COMMANDES ====================

from orders.models import Customer, Order, OrderItem

# Créer un client
customer = Customer.objects.create(
    first_name="Ahmed",
    last_name="Bennani",
    phone="0612345678",
    email="ahmed@example.com",
    address="123 Rue Mohammed V",
    city="Casablanca",
    postal_code="20000"
)

# Créer une commande
order = Order.objects.create(
    customer=customer,
    payment_method='cod',
    subtotal=2199.00,
    shipping_cost=50.00,
    total=2249.00,
    status='pending'
)

# Ajouter des articles à la commande
product = Product.objects.get(reference="CM-AMD-001")
order_item = OrderItem.objects.create(
    order=order,
    product=product,
    product_name=product.name,
    product_reference=product.reference,
    unit_price=product.discount_price or product.price,
    quantity=1
)

# Confirmer une commande
order.status = 'confirmed'
order.save()

# ==================== LIVRAISONS ====================

from orders.models import Delivery
from django.utils import timezone

# Créer une livraison
delivery = Delivery.objects.create(
    order=order,
    tracking_number="TRK123456789",
    status='pending',
    carrier="Amana"
)

# Marquer comme expédiée
delivery.status = 'in_transit'
delivery.shipped_at = timezone.now()
delivery.save()

# Marquer comme livrée
delivery.status = 'delivered'
delivery.delivered_at = timezone.now()
delivery.save()

# Mettre à jour la commande
order.status = 'delivered'
order.save()

# ==================== STATISTIQUES ====================

from django.db.models import Sum, Count, Avg

# Total des ventes
total_sales = Order.objects.filter(
    status__in=['confirmed', 'delivered']
).aggregate(total=Sum('total'))

# Nombre de commandes par statut
orders_by_status = Order.objects.values('status').annotate(
    count=Count('id')
)

# Produits les plus vendus
from django.db.models import Count
top_products = Product.objects.annotate(
    order_count=Count('orderitem')
).order_by('-order_count')[:10]

# Valeur moyenne des commandes
avg_order_value = Order.objects.aggregate(
    avg=Avg('total')
)

# Produits en rupture de stock
out_of_stock = Product.objects.filter(
    quantity=0
) | Product.objects.filter(
    status='out_of_stock'
)

# ==================== UTILITAIRES ====================

# Bulk create - créer plusieurs produits à la fois
products_to_create = [
    Product(
        reference=f"PROD-{i:03d}",
        name=f"Produit Test {i}",
        description="Description test",
        category=composants,
        subcategory=cartes_meres,
        price=999.00 + i,
        quantity=10,
        status='in_stock'
    ) for i in range(1, 11)
]
Product.objects.bulk_create(products_to_create)

# Mettre à jour plusieurs produits
Product.objects.filter(
    category=composants,
    quantity__lt=5
).update(status='out_of_stock')

# Supprimer les produits inactifs
Product.objects.filter(
    quantity=0,
    status='discontinued'
).delete()

# ==================== EXPORT / IMPORT ====================

# Exporter tous les produits en JSON
import json
from django.core.serializers import serialize

products_json = serialize('json', Product.objects.all())
with open('products_export.json', 'w', encoding='utf-8') as f:
    f.write(products_json)

# Compter les éléments
print(f"Catégories: {Category.objects.count()}")
print(f"Sous-catégories: {SubCategory.objects.count()}")
print(f"Types: {Type.objects.count()}")
print(f"Produits: {Product.objects.count()}")
print(f"Commandes: {Order.objects.count()}")
print(f"Clients: {Customer.objects.count()}")

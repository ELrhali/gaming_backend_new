"""
Rapport final de l'importation
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, SubCategory, Brand

print("\n" + "="*80)
print("📊 RAPPORT FINAL D'IMPORTATION - GOBAG.MA")
print("="*80)

# Marques
brands = Brand.objects.all().order_by('name')
print(f"\n📦 MARQUES ({brands.count()}):")
print("-"*80)
for brand in brands:
    product_count = brand.products.count()
    print(f"  • {brand.name}: {product_count} produits")

# Catégories
categories = Category.objects.all().order_by('name')
print(f"\n📁 CATÉGORIES ({categories.count()}):")
print("-"*80)
for category in categories:
    subcats = category.subcategories.all()
    products = Product.objects.filter(category=category)
    print(f"  • {category.name}")
    print(f"    - {subcats.count()} sous-catégories")
    print(f"    - {products.count()} produits")

# Sous-catégories avec produits
subcategories = SubCategory.objects.all().order_by('category__name', 'name')
print(f"\n📂 SOUS-CATÉGORIES ({subcategories.count()}):")
print("-"*80)
current_category = None
for subcat in subcategories:
    if subcat.category.name != current_category:
        current_category = subcat.category.name
        print(f"\n  {current_category}:")
    product_count = subcat.products.count()
    print(f"    - {subcat.name}: {product_count} produits")

# Produits par prix
print(f"\n💰 PRODUITS PAR GAMME DE PRIX:")
print("-"*80)
from django.db.models import Count
from decimal import Decimal

ranges = [
    ("0-100 DH", 0, 100),
    ("100-200 DH", 100, 200),
    ("200-300 DH", 200, 300),
    ("300-500 DH", 300, 500),
    ("500+ DH", 500, 10000)
]

for label, min_price, max_price in ranges:
    count = Product.objects.filter(
        price__gte=Decimal(min_price),
        price__lt=Decimal(max_price)
    ).count()
    print(f"  • {label}: {count} produits")

# Statistiques générales
print(f"\n📊 STATISTIQUES GÉNÉRALES:")
print("-"*80)
total_products = Product.objects.count()
in_stock = Product.objects.filter(status='in_stock').count()
out_of_stock = Product.objects.filter(status='out_of_stock').count()
with_discount = Product.objects.exclude(discount_price__isnull=True).count()

print(f"  • Total de produits: {total_products}")
print(f"  • En stock: {in_stock}")
print(f"  • Rupture de stock: {out_of_stock}")
print(f"  • Produits en promotion: {with_discount}")

# Prix moyens
from django.db.models import Avg
avg_price = Product.objects.aggregate(Avg('price'))['price__avg']
print(f"  • Prix moyen: {float(avg_price):.2f} DH")

# Top 10 produits les plus chers
print(f"\n💎 TOP 10 PRODUITS LES PLUS CHERS:")
print("-"*80)
top_products = Product.objects.order_by('-price')[:10]
for i, product in enumerate(top_products, 1):
    print(f"  {i}. {product.name[:60]}")
    print(f"     {float(product.price):.2f} DH - {product.subcategory.name}")

print("\n" + "="*80)
print("✅ IMPORTATION TERMINÉE AVEC SUCCÈS!")
print("="*80)
print("\n🌐 PROCHAINES ÉTAPES:")
print("  1. Visitez l'admin: http://localhost:8000/admin")
print("  2. Vérifiez le site: http://localhost:3000")
print("  3. Ajoutez des images de produits si nécessaire")
print("  4. Configurez les mises en avant et promotions")
print("\n✨ Votre boutique Gobag.ma est prête!")

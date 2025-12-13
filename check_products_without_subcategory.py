#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vérifier les produits sans sous-catégorie
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, SubCategory

print("="*80)
print("ANALYSE DES PRODUITS SANS SOUS-CATEGORIE")
print("="*80)

# Tous les produits
total_products = Product.objects.count()
print(f"\n[+] Total produits: {total_products}")

# Produits sans sous-catégorie
products_without_subcategory = Product.objects.filter(subcategory__isnull=True)
count = products_without_subcategory.count()
print(f"[!] Produits SANS sous-catégorie: {count}")

if count > 0:
    print(f"\n{'='*80}")
    print("LISTE DES PRODUITS SANS SOUS-CATEGORIE:")
    print(f"{'='*80}\n")
    
    for product in products_without_subcategory[:50]:  # Afficher les 50 premiers
        collection_name = product.collection.name if product.collection else "N/A"
        category_name = product.category.name if product.category else "N/A"
        print(f"[{product.reference}] {product.name[:50]}")
        print(f"  Collection: {collection_name}")
        print(f"  Catégorie: {category_name}")
        print(f"  Sous-catégorie: AUCUNE ❌")
        print()

# Produits avec sous-catégorie
products_with_subcategory = Product.objects.filter(subcategory__isnull=False)
print(f"\n[+] Produits AVEC sous-catégorie: {products_with_subcategory.count()}")

print("\n" + "="*80)
print("STATISTIQUES PAR CATEGORIE")
print("="*80)

categories = Category.objects.all()
for category in categories:
    products_in_cat = Product.objects.filter(category=category)
    without_sub = products_in_cat.filter(subcategory__isnull=True).count()
    with_sub = products_in_cat.filter(subcategory__isnull=False).count()
    
    print(f"\n[{category.name}]")
    print(f"  Total produits: {products_in_cat.count()}")
    print(f"  Avec sous-cat: {with_sub}")
    print(f"  Sans sous-cat: {without_sub}")
    
    # Afficher les sous-catégories disponibles
    subcategories = SubCategory.objects.filter(category=category)
    if subcategories.exists():
        print(f"  Sous-catégories disponibles: {', '.join([s.name for s in subcategories])}")

print("\n" + "="*80)

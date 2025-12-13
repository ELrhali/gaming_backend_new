#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Créer des sous-catégories pour produits orphelins
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, SubCategory
from django.utils.text import slugify

print("="*80)
print("CRÉATION DE SOUS-CATÉGORIES POUR PRODUITS ORPHELINS")
print("="*80)

# Produits sans sous-catégorie
products = Product.objects.filter(subcategory__isnull=True)
print(f"\n[!] Produits à traiter: {products.count()}\n")

# Grouper par catégorie
from collections import defaultdict
by_category = defaultdict(list)

for product in products:
    category_name = product.category.name if product.category else "SANS CATEGORIE"
    by_category[category_name].append(product)

print(f"Catégories concernées: {len(by_category)}\n")

# Mapping de sous-catégories à créer
subcategory_mapping = {
    "IDEES CADEAUX": "Coffrets et accessoires",
    "ACCESSOIRE DE VOYAGE": "Accessoires divers",
}

fixed_count = 0

for category_name, products_list in by_category.items():
    print(f"\n[{category_name}] - {len(products_list)} produits")
    
    if not products_list[0].category:
        print("  ❌ Pas de catégorie associée, impossible de créer sous-catégorie")
        continue
    
    # Déterminer le nom de la sous-catégorie
    subcategory_name = subcategory_mapping.get(category_name, "Autres")
    
    # Créer ou récupérer la sous-catégorie
    try:
        subcategory, created = SubCategory.objects.get_or_create(
            name=subcategory_name,
            category=products_list[0].category,
            defaults={
                'slug': slugify(f"{category_name}-{subcategory_name}"),
                'description': f'{subcategory_name} - {category_name}'
            }
        )
        
        if created:
            print(f"  [+] Sous-catégorie créée: {subcategory_name}")
        else:
            print(f"  [✓] Sous-catégorie existante: {subcategory_name}")
        
        # Associer tous les produits
        for product in products_list:
            product.subcategory = subcategory
            product.save()
            print(f"    ✅ [{product.reference}] {product.name[:50]}")
            fixed_count += 1
            
    except Exception as e:
        print(f"  ❌ Erreur: {str(e)}")

print(f"\n{'='*80}")
print(f"RÉSUMÉ")
print(f"{'='*80}")
print(f"[+] Produits corrigés: {fixed_count}")

# Vérification finale
remaining = Product.objects.filter(subcategory__isnull=True).count()
total = Product.objects.count()
with_sub = Product.objects.filter(subcategory__isnull=False).count()

print(f"\n[✓] Total produits: {total}")
print(f"[✓] Avec sous-catégorie: {with_sub}")
print(f"[!] Sans sous-catégorie: {remaining}")

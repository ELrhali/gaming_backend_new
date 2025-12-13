#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Corriger les produits sans sous-catégorie
"""
import os
import sys
import django
import pandas as pd

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, SubCategory
from django.utils.text import slugify

print("="*80)
print("CORRECTION DES PRODUITS SANS SOUS-CATEGORIE")
print("="*80)

# Charger le fichier Excel
excel_file = "C:/Users/MSI/Desktop/goback/old_data.xlsx"
df = pd.read_excel(excel_file)

# Produits sans sous-catégorie
products_without_subcategory = Product.objects.filter(subcategory__isnull=True)
print(f"\n[!] Produits à corriger: {products_without_subcategory.count()}\n")

fixed_count = 0
errors = []

for product in products_without_subcategory:
    print(f"\n[{product.reference}] {product.name[:60]}")
    
    # Chercher dans Excel
    row = df[df['reference'].astype(str).str.strip() == str(product.reference).strip()]
    
    if row.empty:
        print(f"  ❌ Référence non trouvée dans Excel")
        errors.append(product.reference)
        continue
    
    category_col = row.iloc[0].get('Category', '').strip() if pd.notna(row.iloc[0].get('Category')) else None
    deuxieme_niveau = row.iloc[0].get('2eme niveau', '').strip() if pd.notna(row.iloc[0].get('2eme niveau')) else None
    
    if not category_col:
        print(f"  ❌ Pas de 'Category' dans Excel")
        errors.append(product.reference)
        continue
    
    if not product.category:
        print(f"  ❌ Produit n'a pas de catégorie associée")
        errors.append(product.reference)
        continue
    
    # Chercher ou créer la sous-catégorie
    subcategory_name = category_col
    subcategory_key = f"{deuxieme_niveau}_{subcategory_name}"
    
    try:
        subcategory, created = SubCategory.objects.get_or_create(
            name=subcategory_name,
            category=product.category,
            defaults={
                'slug': slugify(f"{deuxieme_niveau}-{subcategory_name}"),
                'description': f'Sous-catégorie {subcategory_name}'
            }
        )
        
        if created:
            print(f"  [+] Sous-catégorie créée: {subcategory_name}")
        else:
            print(f"  [✓] Sous-catégorie trouvée: {subcategory_name}")
        
        # Associer au produit
        product.subcategory = subcategory
        product.save()
        
        print(f"  ✅ Produit corrigé!")
        fixed_count += 1
        
    except Exception as e:
        print(f"  ❌ Erreur: {str(e)}")
        errors.append(product.reference)

print(f"\n{'='*80}")
print(f"RÉSUMÉ")
print(f"{'='*80}")
print(f"[+] Produits corrigés: {fixed_count}")
print(f"[!] Erreurs: {len(errors)}")

if errors:
    print(f"\nRéférences avec erreurs:")
    for ref in errors:
        print(f"  - {ref}")

# Vérification finale
remaining = Product.objects.filter(subcategory__isnull=True).count()
print(f"\n[!] Produits restants sans sous-catégorie: {remaining}")

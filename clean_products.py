"""
Script de nettoyage et réimportation complète
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, SubCategory, Brand

print("🧹 NETTOYAGE DE LA BASE DE DONNÉES...")
print("="*80)

# Supprimer tous les produits existants
product_count = Product.objects.count()
Product.objects.all().delete()
print(f"✓ {product_count} produits supprimés")

print("\n✅ Base de données prête pour la réimportation!")
print("\nExécutez maintenant: python import_from_old_sql.py")

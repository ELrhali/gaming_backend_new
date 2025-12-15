"""
Script pour vérifier les produits de l'Excel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

refs = ['AL000001', 'AL000002', 'AL000003', 'AL000005', 'AL000006', 'AL000007']

print("=" * 80)
print("VÉRIFICATION DES PRODUITS DE L'EXCEL")
print("=" * 80)

for ref in refs:
    prod = Product.objects.filter(reference=ref).first()
    if prod:
        print(f"\n✅ {ref}: EXISTE")
        print(f"   Nom: {prod.name}")
        print(f"   Catégorie: {prod.category.name}")
        print(f"   Sous-catégorie: {prod.subcategory.name}")
        if prod.brand:
            print(f"   Marque: {prod.brand.name}")
    else:
        print(f"\n❌ {ref}: N'EXISTE PAS")

print("\n" + "=" * 80)

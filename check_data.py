"""
Script pour vérifier les données importées
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Brand, Type, Product

print("=" * 80)
print("VÉRIFICATION DES DONNÉES IMPORTÉES")
print("=" * 80)

print("\n=== CATEGORIES ===")
for cat in Category.objects.all():
    print(f"  • {cat.name}")

print("\n=== SOUS-CATEGORIES ===")
for sub in SubCategory.objects.all():
    print(f"  • {sub.name} (Catégorie: {sub.category.name})")

print("\n=== MARQUES ===")
for brand in Brand.objects.all():
    print(f"  • {brand.name}")

print("\n=== TYPES ===")
for type_obj in Type.objects.all():
    brand_name = type_obj.brand.name if type_obj.brand else "Sans marque"
    print(f"  • {type_obj.name} (Marque: {brand_name})")

print("\n=== PRODUITS ===")
for prod in Product.objects.all()[:10]:  # Afficher les 10 premiers
    print(f"  • {prod.reference} - {prod.name}")
    print(f"    Catégorie: {prod.category.name}")
    print(f"    Sous-catégorie: {prod.subcategory.name}")
    if prod.brand:
        print(f"    Marque: {prod.brand.name}")
    if prod.type:
        print(f"    Type: {prod.type.name}")
    print()

print("=" * 80)

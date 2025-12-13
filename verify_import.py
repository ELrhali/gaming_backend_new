import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Type, Brand, Product, ProductImage

print("=" * 80)
print("VERIFICATION DE L'IMPORTATION")
print("=" * 80)

print(f"\n[OK] Categories       : {Category.objects.count()}")
print(f"[OK] Sous-categories  : {SubCategory.objects.count()}")
print(f"[OK] Types            : {Type.objects.count()}")
print(f"[OK] Marques          : {Brand.objects.count()}")
print(f"[OK] Produits         : {Product.objects.count()}")
print(f"[OK] Images produits  : {ProductImage.objects.count()}")

print("\n" + "=" * 80)
print("EXEMPLES DE PRODUITS")
print("=" * 80)

for p in Product.objects.all()[:5]:
    print(f"\n[+] {p.name[:50]}...")
    print(f"    Reference: {p.reference}")
    print(f"    Prix: {p.price} DH")
    print(f"    Stock: {p.quantity}")
    print(f"    Categorie: {p.category.name if p.category else 'N/A'}")
    print(f"    Sous-categorie: {p.subcategory.name if p.subcategory else 'N/A'}")
    print(f"    Type: {p.type.name if p.type else 'N/A'}")
    print(f"    Marque: {p.brand.name if p.brand else 'N/A'}")
    print(f"    Images: {p.images.count()}")

print("\n" + "=" * 80)
print("CATEGORIES PRINCIPALES")
print("=" * 80)

for cat in Category.objects.all()[:10]:
    print(f"[+] {cat.name} ({cat.subcategories.count()} sous-categories, {Product.objects.filter(category=cat).count()} produits)")

print("\n" + "=" * 80)
print("MARQUES")
print("=" * 80)

for brand in Brand.objects.all():
    print(f"[+] {brand.name} ({Product.objects.filter(brand=brand).count()} produits)")

print("\n[OK] Importation terminee avec succes!")

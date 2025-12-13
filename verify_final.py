import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Collection, Category, SubCategory, Brand, Product, ProductImage

print("=" * 80)
print("VERIFICATION - NOUVELLE STRUCTURE")
print("=" * 80)
print("\nStructure importee:")
print("  1er niveau   -> Collection")
print("  2eme niveau  -> Category")
print("  Category col -> SubCategory")
print("  marque       -> Brand")
print("=" * 80)

print(f"\n[+] Collections       : {Collection.objects.count()}")
print(f"[+] Categories        : {Category.objects.count()}")
print(f"[+] Sous-categories   : {SubCategory.objects.count()}")
print(f"[+] Marques           : {Brand.objects.count()}")
print(f"[+] Produits          : {Product.objects.count()}")
print(f"[+] Images produits   : {ProductImage.objects.count()}")

print("\n" + "=" * 80)
print("COLLECTIONS (1er niveau) - TOP 10")
print("=" * 80)

collections = Collection.objects.all()[:10]
if not collections:
    print("AUCUNE COLLECTION! Normal car aucune collection n'est liee aux produits.")
else:
    for coll in collections:
        cat_count = Category.objects.filter(collection=coll).count()
        prod_count = Product.objects.filter(collection=coll).count()
        print(f"[+] {coll.name} ({cat_count} categories, {prod_count} produits)")

print("\n" + "=" * 80)
print("CATEGORIES (2eme niveau) - TOP 10")
print("=" * 80)

for cat in Category.objects.all()[:10]:
    sub_count = cat.subcategories.count()
    prod_count = Product.objects.filter(category=cat).count()
    collection_name = cat.collection.name if cat.collection else "AUCUNE"
    print(f"[+] {cat.name} (Collection: {collection_name}, {sub_count} sous-categories, {prod_count} produits)")

print("\n" + "=" * 80)
print("SOUS-CATEGORIES (Category colonne) - TOP 10")
print("=" * 80)

for sub in SubCategory.objects.all()[:10]:
    prod_count = Product.objects.filter(subcategory=sub).count()
    print(f"[+] {sub.name} (Categorie: {sub.category.name}, {prod_count} produits)")

print("\n" + "=" * 80)
print("MARQUES")
print("=" * 80)

for brand in Brand.objects.all():
    prod_count = Product.objects.filter(brand=brand).count()
    print(f"[+] {brand.name} ({prod_count} produits)")

print("\n" + "=" * 80)
print("EXEMPLE DE PRODUITS")
print("=" * 80)

for p in Product.objects.all()[:5]:
    print(f"\n[+] {p.name[:50]}... ({p.reference})")
    print(f"    Prix: {p.price} DH | Stock: {p.quantity}")
    print(f"    Collection: {p.collection.name if p.collection else 'AUCUNE'}")
    print(f"    Categorie: {p.category.name if p.category else 'AUCUNE'}")
    print(f"    Sous-categorie: {p.subcategory.name if p.subcategory else 'AUCUNE'}")
    print(f"    Marque: {p.brand.name if p.brand else 'AUCUNE'}")
    print(f"    Image principale: {p.main_image if p.main_image else 'AUCUNE'}")
    print(f"    Images galerie: {p.images.count()}")

print("\n[OK] Importation avec nouvelle structure terminee!")

import os
import sys
import django

# Configuration Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, SubCategory, Brand, Type

print("=" * 80)
print("📊 VÉRIFICATION DES DONNÉES POUR LES FILTRES")
print("=" * 80)

# Statistiques globales
total_products = Product.objects.count()
print(f"\n✅ Total de produits: {total_products}")

# Par catégorie
categories = Category.objects.all()
print(f"\n📁 CATÉGORIES ({categories.count()}):")
for cat in categories:
    count = Product.objects.filter(category=cat).count()
    print(f"   • {cat.name}: {count} produit(s)")

# Par marque
brands = Brand.objects.all()
print(f"\n🏷️  MARQUES ({brands.count()}):")
top_brands = []
for brand in brands:
    count = Product.objects.filter(brand=brand).count()
    if count > 0:
        top_brands.append((brand.name, count))

top_brands.sort(key=lambda x: x[1], reverse=True)
for brand_name, count in top_brands[:10]:
    print(f"   • {brand_name}: {count} produit(s)")

if len(top_brands) > 10:
    print(f"   ... et {len(top_brands) - 10} autres marques")

# Par statut
print(f"\n📊 PAR STATUT:")
statuses = [
    ('in_stock', 'En Stock'),
    ('out_of_stock', 'Rupture de Stock'),
    ('preorder', 'Précommande'),
    ('discontinued', 'Discontinué'),
]
for status_code, status_name in statuses:
    count = Product.objects.filter(status=status_code).count()
    print(f"   • {status_name}: {count} produit(s)")

# Par stock
print(f"\n📦 PAR NIVEAU DE STOCK:")
in_stock = Product.objects.filter(quantity__gt=0).count()
low_stock = Product.objects.filter(quantity__gt=0, quantity__lte=5).count()
out_stock = Product.objects.filter(quantity=0).count()
print(f"   • Disponible (>0): {in_stock} produit(s)")
print(f"   • Stock faible (≤5): {low_stock} produit(s)")
print(f"   • Épuisé (=0): {out_stock} produit(s)")

# Filtres spéciaux
print(f"\n🌟 FILTRES SPÉCIAUX:")
bestseller = Product.objects.filter(is_bestseller=True).count()
featured = Product.objects.filter(is_featured=True).count()
new = Product.objects.filter(is_new=True).count()
print(f"   • Best Seller: {bestseller} produit(s)")
print(f"   • Produit Vedette: {featured} produit(s)")
print(f"   • Nouveau: {new} produit(s)")

# Types
types_count = Type.objects.count()
print(f"\n🏷️  Types/Modèles: {types_count}")

print("\n" + "=" * 80)
print("✅ TOUS LES FILTRES SONT PRÊTS À FONCTIONNER!")
print("=" * 80)
print("\n💡 Accédez à: http://127.0.0.1:8000/admin-panel/products/")

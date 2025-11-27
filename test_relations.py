"""
Script de test pour vérifier les relations de filtrage
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Type, Brand, Product

print("=" * 60)
print("TEST DES RELATIONS - FILTRAGE DYNAMIQUE")
print("=" * 60)

# Test 1: Categories → SubCategories
print("\n1. CATEGORIES ET SOUS-CATEGORIES:")
print("-" * 60)
for cat in Category.objects.all()[:3]:
    subs = SubCategory.objects.filter(category=cat)
    print(f"📁 {cat.name}")
    for sub in subs:
        print(f"   ├── {sub.name}")
    if not subs.exists():
        print(f"   └── (aucune sous-catégorie)")

# Test 2: SubCategories → Types
print("\n2. SOUS-CATEGORIES ET MODELES:")
print("-" * 60)
for sub in SubCategory.objects.all()[:3]:
    types = Type.objects.filter(subcategory=sub)
    print(f"📂 {sub.name}")
    for t in types:
        print(f"   ├── {t.name}")
    if not types.exists():
        print(f"   └── (aucun modèle)")

# Test 3: Brands et produits
print("\n3. MARQUES ET PRODUITS:")
print("-" * 60)
for brand in Brand.objects.all()[:5]:
    products = Product.objects.filter(brand=brand)
    print(f"🏢 {brand.name}: {products.count()} produit(s)")

# Test 4: Statistiques
print("\n4. STATISTIQUES:")
print("-" * 60)
print(f"Catégories:      {Category.objects.count()}")
print(f"Sous-catégories: {SubCategory.objects.count()}")
print(f"Modèles (Types): {Type.objects.count()}")
print(f"Marques:         {Brand.objects.count()}")
print(f"Produits:        {Product.objects.count()}")

# Test 5: Exemple de filtrage
print("\n5. EXEMPLE DE FILTRAGE:")
print("-" * 60)
cat = Category.objects.first()
if cat:
    print(f"Catégorie sélectionnée: {cat.name}")
    subs = SubCategory.objects.filter(category=cat)
    print(f"→ {subs.count()} sous-catégorie(s) disponible(s)")
    
    if subs.exists():
        sub = subs.first()
        print(f"\nSous-catégorie sélectionnée: {sub.name}")
        types = Type.objects.filter(subcategory=sub)
        print(f"→ {types.count()} modèle(s) disponible(s)")
        
        if types.exists():
            for t in types[:3]:
                print(f"   • {t.name}")

print("\n" + "=" * 60)
print("✓ Test terminé!")
print("=" * 60)

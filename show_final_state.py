"""
Script pour afficher l'état final de la base de données
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Brand, Type
from collections import defaultdict

print("\n📊 ÉTAT FINAL DE LA BASE DE DONNÉES")
print("="*60)

# Catégories
print(f"\n✅ CATEGORIES ({Category.objects.count()}):\n")
for cat in Category.objects.all().order_by('name'):
    img_status = "✅" if cat.image else "❌"
    print(f"   - {cat.name} (Image: {img_status})")

# Sous-catégories groupées par catégorie
print(f"\n✅ SOUS-CATEGORIES ({SubCategory.objects.count()}):\n")
cats_dict = defaultdict(list)
for subcat in SubCategory.objects.all():
    cats_dict[subcat.category.name].append(subcat)

for cat_name in sorted(cats_dict.keys()):
    print(f"\n   📁 {cat_name}:")
    for subcat in sorted(cats_dict[cat_name], key=lambda x: x.name):
        img_status = "✅" if subcat.image else "❌"
        print(f"      - {subcat.name} (Image: {img_status})")

# Marques
print(f"\n✅ MARQUES ({Brand.objects.count()}):")
for brand in Brand.objects.all().order_by('name')[:20]:
    print(f"   - {brand.name}")
if Brand.objects.count() > 20:
    print(f"   ... et {Brand.objects.count() - 20} autres")

# Types
print(f"\n✅ TYPES ({Type.objects.count()})")

print("\n" + "="*60)
print("✅ NETTOYAGE TERMINÉ - BASE DE DONNÉES PROPRE")
print("="*60)

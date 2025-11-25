import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.serializers import TypeSerializer
from shop.models import Type, SubCategory

print("=" * 60)
print("Structure de l'API Types")
print("=" * 60)

# Prendre quelques types
types = Type.objects.all()[:3]

print("\n📦 Types dans la base de données:")
for t in types:
    print(f"\nType: {t.name}")
    print(f"  - ID: {t.id}")
    print(f"  - Slug: {t.slug}")
    print(f"  - Subcategory ID: {t.subcategory.id}")
    print(f"  - Subcategory Name: {t.subcategory.name}")

print("\n" + "=" * 60)
print("Structure retournée par le serializer:")
print("=" * 60)

# Sérialiser un type
serializer = TypeSerializer(types.first())
print("\n", serializer.data)

print("\n" + "=" * 60)
print("Vérification des sous-catégories:")
print("=" * 60)

subs = SubCategory.objects.all()[:3]
for sub in subs:
    print(f"\n{sub.name} (ID: {sub.id})")
    types_count = Type.objects.filter(subcategory=sub).count()
    print(f"  - Types liés: {types_count}")
    if types_count > 0:
        for t in Type.objects.filter(subcategory=sub):
            print(f"    • {t.name}")

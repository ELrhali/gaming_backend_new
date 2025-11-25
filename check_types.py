import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import SubCategory, Type

print("=" * 60)
print("Types par sous-catégorie")
print("=" * 60)

subcats = SubCategory.objects.all().prefetch_related('types')

for sc in subcats:
    types = sc.types.all()
    print(f"\n{sc.name} ({sc.slug}) - Catégorie: {sc.category.name}")
    if types:
        for t in types:
            print(f"  ✓ {t.name} -> {t.slug}")
    else:
        print(f"  ✗ Aucun type disponible")

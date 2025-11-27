import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import HeroSlide

slides = HeroSlide.objects.filter(is_active=True).order_by('order', '-created_at')

print("Slides actifs:")
print("-" * 80)
for s in slides:
    print(f"ID {s.id}: {s.title or '(sans titre)'}")
    print(f"  Type: {s.slide_type}")
    print(f"  Category ID: {s.category_id}")
    print(f"  SubCategory ID: {s.subcategory_id}")
    print(f"  Product ID: {s.product_id}")
    print(f"  Link généré: {s.get_link()}")
    print("-" * 80)

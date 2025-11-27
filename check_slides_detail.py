import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import HeroSlide, Category, SubCategory, Product

slides = HeroSlide.objects.filter(is_active=True).order_by('order', '-created_at')

print("Vérification détaillée des slides:")
print("=" * 80)
for s in slides:
    print(f"\nID {s.id}: {s.title or '(sans titre)'}")
    print(f"  Type: {s.slide_type}")
    
    if s.slide_type == 'category' and s.category:
        print(f"  Catégorie: {s.category.name} (slug: {s.category.slug})")
        print(f"  Link attendu: /categorie/{s.category.slug}")
    elif s.slide_type == 'subcategory' and s.subcategory:
        print(f"  Sous-catégorie: {s.subcategory.name} (slug: {s.subcategory.slug})")
        print(f"  Link attendu: /sous-categorie/{s.subcategory.slug}")
    elif s.slide_type == 'product' and s.product:
        print(f"  Produit: {s.product.name} (slug: {s.product.slug})")
        print(f"  Link attendu: /produit/{s.product.slug}")
    
    print(f"  Link généré: {s.get_link()}")
    print("-" * 80)

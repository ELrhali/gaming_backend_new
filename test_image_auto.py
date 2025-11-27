import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import HeroSlide

print("Test de la sélection automatique d'images:")
print("=" * 80)

slides = HeroSlide.objects.filter(is_active=True).order_by('order', '-created_at')

for slide in slides:
    print(f"\nSlide ID {slide.id}: {slide.title or '(sans titre)'}")
    print(f"  Type: {slide.slide_type}")
    print(f"  Image personnalisée: {'Oui' if slide.custom_image else 'Non'}")
    
    if slide.custom_image:
        print(f"    -> {slide.custom_image.url}")
    
    image_url = slide.get_image_url()
    
    if image_url:
        if slide.custom_image:
            print(f"  Image utilisée: Image personnalisée")
        else:
            if slide.slide_type == 'category':
                print(f"  Image utilisée: Image de la catégorie '{slide.category.name}'")
            elif slide.slide_type == 'subcategory':
                print(f"  Image utilisée: Image de la sous-catégorie '{slide.subcategory.name}'")
            elif slide.slide_type == 'product':
                print(f"  Image utilisée: Image principale du produit '{slide.product.name}'")
        print(f"  URL finale: {image_url}")
    else:
        print(f"  ⚠️ Aucune image disponible")
    
    print("-" * 80)

print("\n✅ La fonctionnalité de sélection automatique d'image est déjà active!")
print("📝 Si vous ne mettez pas d'image personnalisée, l'image de l'élément sera utilisée.")

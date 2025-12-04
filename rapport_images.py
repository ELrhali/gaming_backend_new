import os
import sys
import django

# Configuration Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, ProductImage

print("=" * 80)
print("📊 RAPPORT DES PRODUITS AVEC IMAGES")
print("=" * 80)

# Statistiques globales
total_products = Product.objects.count()
products_with_images = Product.objects.filter(images__isnull=False).distinct().count()
total_images = ProductImage.objects.count()

print(f"\n📈 Statistiques globales:")
print(f"   • Total de produits: {total_products}")
print(f"   • Produits avec images: {products_with_images}")
print(f"   • Total d'images: {total_images}")
print(f"   • Moyenne: {total_images / products_with_images if products_with_images > 0 else 0:.1f} images/produit")

# Afficher quelques exemples
print(f"\n📦 Exemples de produits avec images:")
print("━" * 80)

products_sample = Product.objects.filter(images__isnull=False).distinct()[:10]

for idx, product in enumerate(products_sample, 1):
    images_count = product.images.count()
    main_image = product.images.filter(is_main=True).first()
    
    print(f"\n{idx}. {product.name[:50]}...")
    print(f"   Référence: {product.reference}")
    print(f"   Nombre d'images: {images_count}")
    
    if main_image:
        main_filename = os.path.basename(main_image.image.name)
        print(f"   Image principale: {main_filename}")
    
    # Afficher quelques autres images
    other_images = product.images.filter(is_main=False)[:2]
    if other_images:
        print(f"   Autres images:")
        for img in other_images:
            filename = os.path.basename(img.image.name)
            print(f"      - {filename}")

print("\n" + "=" * 80)
print("✅ Si vous réimportez maintenant, toutes ces images seront ignorées!")
print("=" * 80)

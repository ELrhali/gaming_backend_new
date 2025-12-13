import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

print("=" * 80)
print("VERIFICATION DES IMAGES")
print("=" * 80)

for p in Product.objects.all()[:10]:
    print(f"\n[+] {p.name[:40]}... ({p.reference})")
    print(f"    Image principale: {p.main_image if p.main_image else 'AUCUNE'}")
    print(f"    Images galerie: {p.images.count()}")
    if p.images.exists():
        for img in p.images.all()[:3]:
            print(f"      - {img.image}")

print("\n" + "=" * 80)
print("STATISTIQUES")
print("=" * 80)

total = Product.objects.count()
with_main = Product.objects.exclude(main_image='').count()
with_gallery = Product.objects.filter(images__isnull=False).distinct().count()

print(f"[OK] Total produits: {total}")
print(f"[OK] Avec image principale: {with_main}")
print(f"[OK] Avec galerie d'images: {with_gallery}")

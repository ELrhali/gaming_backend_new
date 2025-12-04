import os
import sys
import django

# Configuration Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, ProductImage

# Prendre un produit qui a des images
product = Product.objects.filter(images__isnull=False).first()

if product:
    print(f"🔍 Test de duplication pour: {product.name} ({product.reference})")
    print(f"━" * 60)
    
    images = product.images.all()
    print(f"📊 Nombre d'images actuelles: {images.count()}")
    print(f"\n📸 Liste des images:")
    
    for idx, img in enumerate(images[:5], 1):
        print(f"   {idx}. {os.path.basename(img.image.name)} {'[PRINCIPALE]' if img.is_main else ''}")
    
    if images.count() > 5:
        print(f"   ... et {images.count() - 5} autres images")
    
    print(f"\n━" * 60)
    print("✅ La protection anti-duplication vérifiera:")
    print(f"   - Si le nom du fichier existe déjà pour ce produit")
    print(f"   - Si oui, l'image sera ignorée avec le message: '⏭️  Image déjà existante (ignorée)'")
    print(f"\n💡 Conseil: Lancez import_product_images.py pour voir la protection en action")
    
else:
    print("❌ Aucun produit avec images trouvé dans la base de données")

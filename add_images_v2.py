"""
Script pour ajouter des images aux catégories, sous-catégories et produits
Usage: python add_images_v2.py
"""
import os
import django
import urllib.request
import tempfile
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from shop.models import Category, SubCategory, Product, ProductImage

# Images placeholder de haute qualité (via Unsplash)
PLACEHOLDER_IMAGES = {
    'categories': {
        'COMPOSANT PC': 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=600&fit=crop',
        'PÉRIPHÉRIQUES PC': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&h=600&fit=crop',
        'Accessoires PC': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800&h=600&fit=crop',
    },
    'subcategories': {
        'Processeurs': 'https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=600&fit=crop',
        'Cartes Graphiques': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=600&fit=crop',
        'Cartes Mères': 'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=600&fit=crop',
        'Mémoire RAM': 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=600&fit=crop',
        'Disques SSD': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=600&fit=crop',
        'Disques Durs': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=600&fit=crop',
        'Alimentations': 'https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=600&fit=crop',
        'Boîtiers PC': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&h=600&fit=crop',
        'Écrans PC': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=600&fit=crop',
        'Claviers Gaming': 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=600&fit=crop',
        'Souris Gaming': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=600&fit=crop',
        'Casques Audio': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop',
        'Webcams': 'https://images.unsplash.com/photo-1593642532400-2682810df593?w=800&h=600&fit=crop',
        'Refroidissement': 'https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=600&fit=crop',
        'Câbles et Adaptateurs': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop',
        'Tapis de Souris': 'https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=600&fit=crop',
        'Supports et Stands': 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=600&fit=crop',
    },
    'products': {
        'CPU-001': [
            'https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=600&fit=crop'
        ],
        'CPU-002': [
            'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=600&fit=crop'
        ],
        'CPU-003': ['https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=600&fit=crop'],
        'CPU-004': ['https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=600&fit=crop'],
        'GPU-001': [
            'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=600&fit=crop'
        ],
        'GPU-002': [
            'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=600&fit=crop'
        ],
        'GPU-003': ['https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop'],
        'GPU-004': ['https://images.unsplash.com/photo-1593642532400-2682810df593?w=800&h=600&fit=crop'],
        'MB-001': [
            'https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop'
        ],
        'MB-002': ['https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=600&fit=crop'],
        'RAM-001': [
            'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=600&fit=crop'
        ],
        'RAM-002': ['https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=600&fit=crop'],
        'SSD-001': [
            'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=600&fit=crop'
        ],
        'SSD-002': ['https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&h=600&fit=crop'],
        'PSU-001': ['https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=600&fit=crop'],
        'MON-001': [
            'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=600&fit=crop'
        ],
        'MON-002': ['https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=600&fit=crop'],
        'MON-003': ['https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop'],
        'KB-001': [
            'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop'
        ],
        'KB-002': ['https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=600&fit=crop'],
        'MS-001': [
            'https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop'
        ],
        'MS-002': ['https://images.unsplash.com/photo-1593642532400-2682810df593?w=800&h=600&fit=crop'],
        'HS-001': [
            'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=600&fit=crop'
        ],
        'HS-002': ['https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop'],
        'COOL-001': [
            'https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=600&fit=crop'
        ],
        'COOL-002': ['https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=600&fit=crop'],
        'PAD-001': ['https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=600&fit=crop'],
    }
}

def download_image(url, filename):
    """Télécharge une image et la sauvegarde temporairement"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        # Créer un fichier temporaire
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_path = temp_file.name
        temp_file.close()
        
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(temp_path, 'wb') as f:
                f.write(response.read())
        
        return temp_path
    except Exception as e:
        print(f"    ⚠️  Erreur téléchargement {filename}: {e}")
        return None

def add_category_images():
    """Ajoute des images aux catégories"""
    print("\n📸 Ajout des images aux catégories...")
    count = 0
    
    for cat_name, img_url in PLACEHOLDER_IMAGES['categories'].items():
        try:
            category = Category.objects.get(name=cat_name)
            if not category.image:
                filename = f"cat_{category.slug}.jpg"
                temp_path = download_image(img_url, filename)
                if temp_path:
                    with open(temp_path, 'rb') as f:
                        category.image.save(filename, File(f), save=True)
                    os.remove(temp_path)
                    count += 1
                    print(f"  ✓ {cat_name}")
        except Exception as e:
            print(f"  ✗ Erreur {cat_name}: {e}")
    
    return count

def add_subcategory_images():
    """Ajoute des images aux sous-catégories"""
    print("\n📸 Ajout des images aux sous-catégories...")
    count = 0
    
    for subcat_name, img_url in PLACEHOLDER_IMAGES['subcategories'].items():
        try:
            subcategory = SubCategory.objects.get(name=subcat_name)
            if not subcategory.image:
                filename = f"subcat_{subcategory.slug}.jpg"
                temp_path = download_image(img_url, filename)
                if temp_path:
                    with open(temp_path, 'rb') as f:
                        subcategory.image.save(filename, File(f), save=True)
                    os.remove(temp_path)
                    count += 1
                    print(f"  ✓ {subcat_name}")
        except Exception as e:
            print(f"  ✗ Erreur {subcat_name}: {e}")
    
    return count

def add_product_images():
    """Ajoute des images aux produits"""
    print("\n📸 Ajout des images aux produits...")
    product_count = 0
    image_count = 0
    
    for product_ref, img_urls in PLACEHOLDER_IMAGES['products'].items():
        try:
            product = Product.objects.get(reference=product_ref)
            
            # Supprimer les anciennes images
            ProductImage.objects.filter(product=product).delete()
            
            # Ajouter les nouvelles images
            for idx, img_url in enumerate(img_urls, 1):
                filename = f"prod_{product.slug}_{idx}.jpg"
                temp_path = download_image(img_url, filename)
                if temp_path:
                    with open(temp_path, 'rb') as f:
                        product_image = ProductImage.objects.create(
                            product=product,
                            is_main=(idx == 1)
                        )
                        product_image.image.save(filename, File(f), save=True)
                    os.remove(temp_path)
                    image_count += 1
            
            product_count += 1
            print(f"  ✓ {product_ref} ({len(img_urls)} images)")
        except Exception as e:
            print(f"  ✗ Erreur {product_ref}: {e}")
    
    return product_count, image_count

def main():
    print("=" * 70)
    print("📸 AJOUT DES IMAGES")
    print("=" * 70)
    print("\n⚠️  Note: Ce script utilise des images de Unsplash.")
    print("Pour de meilleures performances, ajoutez vos propres images via l'admin.")
    
    response = input("\nContinuer? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("Annulé.")
        return
    
    # Ajouter les images
    cat_count = add_category_images()
    subcat_count = add_subcategory_images()
    prod_count, prod_img_count = add_product_images()
    
    # Statistiques finales
    print("\n" + "=" * 70)
    print("✅ IMAGES AJOUTÉES AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\n📊 Statistiques:")
    print(f"  • Catégories avec images: {cat_count}/3")
    print(f"  • Sous-catégories avec images: {subcat_count}/17")
    print(f"  • Produits avec images: {prod_count}/27")
    print(f"  • Total images produits: {prod_img_count}")
    print(f"\n📝 Accédez à http://localhost:8000/admin-panel/ pour voir les images")
    print("=" * 70)

if __name__ == '__main__':
    main()

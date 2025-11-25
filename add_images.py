"""
Script pour ajouter des images aux catégories, sous-catégories et produits
Usage: python add_images.py
"""
import os
import django
import urllib.request
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from shop.models import Category, SubCategory, Product, ProductImage

# Images placeholder de haute qualité (via placeholder services)
PLACEHOLDER_IMAGES = {
    'categories': {
        'COMPOSANT PC': 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=600&fit=crop',  # PC components
        'PÉRIPHÉRIQUES PC': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&h=600&fit=crop',  # Gaming peripherals
        'Accessoires PC': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800&h=600&fit=crop',  # Accessories
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
        'Supports et Stands': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&h=600&fit=crop',
    },
    'products': {
        # Processeurs
        'CPU-001': ['https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=800&fit=crop', 
                    'https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=800&fit=crop'],
        'CPU-002': ['https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=800&fit=crop'],
        'CPU-003': ['https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=800&fit=crop'],
        'CPU-004': ['https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&h=800&fit=crop'],
        
        # Cartes Graphiques
        'GPU-001': ['https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=800&fit=crop'],
        'GPU-002': ['https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=800&fit=crop'],
        'GPU-003': ['https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=800&fit=crop'],
        'GPU-004': ['https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&h=800&fit=crop'],
        
        # Cartes Mères
        'MB-001': ['https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=800&fit=crop',
                   'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=800&fit=crop'],
        'MB-002': ['https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&h=800&fit=crop'],
        
        # RAM
        'RAM-001': ['https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=800&fit=crop'],
        'RAM-002': ['https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&h=800&fit=crop'],
        
        # SSD
        'SSD-001': ['https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=800&fit=crop'],
        'SSD-002': ['https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&h=800&fit=crop'],
        
        # Alimentations
        'PSU-001': ['https://images.unsplash.com/photo-1591799265444-d66432b91588?w=800&h=800&fit=crop'],
        
        # Écrans
        'MON-001': ['https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800&h=800&fit=crop'],
        'MON-002': ['https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=800&fit=crop'],
        'MON-003': ['https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=800&fit=crop'],
        
        # Claviers
        'KB-001': ['https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=800&fit=crop',
                   'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&h=800&fit=crop'],
        'KB-002': ['https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&h=800&fit=crop'],
        
        # Souris
        'MS-001': ['https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=800&fit=crop',
                   'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&h=800&fit=crop'],
        'MS-002': ['https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&h=800&fit=crop'],
        
        # Casques
        'HS-001': ['https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=800&fit=crop',
                   'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800&h=800&fit=crop'],
        'HS-002': ['https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=800&fit=crop'],
        
        # Refroidissement
        'COOL-001': ['https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=800&fit=crop',
                     'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&h=800&fit=crop'],
        'COOL-002': ['https://images.unsplash.com/photo-1587202372583-49330a15584d?w=800&h=800&fit=crop'],
        
        # Tapis de souris
        'PAD-001': ['https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=800&h=800&fit=crop'],
    }
}

def download_image(url, name):
    """Télécharge une image depuis une URL"""
    try:
        img_temp = NamedTemporaryFile(delete=True)
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            img_temp.write(response.read())
            img_temp.flush()
        
        return img_temp, f"{name}.jpg"
    except Exception as e:
        print(f"    ⚠️  Erreur téléchargement {name}: {e}")
        return None, None

def add_category_images():
    """Ajoute des images aux catégories"""
    print("\n📸 Ajout des images aux catégories...")
    
    for cat_name, img_url in PLACEHOLDER_IMAGES['categories'].items():
        try:
            category = Category.objects.get(name=cat_name)
            if not category.image:
                img_temp, img_name = download_image(img_url, f"cat_{category.slug}")
                if img_temp:
                    category.image.save(img_name, File(img_temp))
                    print(f"  ✓ {cat_name}")
        except Exception as e:
            print(f"  ✗ Erreur {cat_name}: {e}")

def add_subcategory_images():
    """Ajoute des images aux sous-catégories"""
    print("\n📸 Ajout des images aux sous-catégories...")
    
    for subcat_name, img_url in PLACEHOLDER_IMAGES['subcategories'].items():
        try:
            subcategory = SubCategory.objects.get(name=subcat_name)
            if not subcategory.image:
                img_temp, img_name = download_image(img_url, f"subcat_{subcategory.slug}")
                if img_temp:
                    subcategory.image.save(img_name, File(img_temp))
                    print(f"  ✓ {subcat_name}")
        except Exception as e:
            print(f"  ✗ Erreur {subcat_name}: {e}")

def add_product_images():
    """Ajoute des images aux produits"""
    print("\n📸 Ajout des images aux produits...")
    
    for product_ref, img_urls in PLACEHOLDER_IMAGES['products'].items():
        try:
            product = Product.objects.get(reference=product_ref)
            
            # Supprimer les anciennes images
            product.images.all().delete()
            
            # Ajouter les nouvelles images
            for idx, img_url in enumerate(img_urls):
                img_temp, img_name = download_image(img_url, f"prod_{product.slug}_{idx+1}")
                if img_temp:
                    ProductImage.objects.create(
                        product=product,
                        image=File(img_temp, name=img_name),
                        is_main=(idx == 0),  # Première image = image principale
                        order=idx
                    )
            
            img_count = len(img_urls)
            print(f"  ✓ {product_ref} ({img_count} image{'s' if img_count > 1 else ''})")
            
        except Exception as e:
            print(f"  ✗ Erreur {product_ref}: {e}")

def main():
    print("=" * 70)
    print("📸 AJOUT DES IMAGES")
    print("=" * 70)
    print("\n⚠️  Note: Ce script utilise des images de Unsplash.")
    print("Pour de meilleures performances, ajoutez vos propres images via l'admin.")
    
    response = input("\nContinuer? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("❌ Annulé")
        return
    
    add_category_images()
    add_subcategory_images()
    add_product_images()
    
    print("\n" + "=" * 70)
    print("✅ IMAGES AJOUTÉES AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\n📊 Statistiques:")
    print(f"  • Catégories avec images: {Category.objects.exclude(image='').count()}/{Category.objects.count()}")
    print(f"  • Sous-catégories avec images: {SubCategory.objects.exclude(image='').count()}/{SubCategory.objects.count()}")
    print(f"  • Produits avec images: {Product.objects.filter(images__isnull=False).distinct().count()}/{Product.objects.count()}")
    print(f"  • Total images produits: {ProductImage.objects.count()}")
    print("\n📝 Accédez à http://localhost:8000/admin-panel/ pour voir les images")
    print("=" * 70)

if __name__ == '__main__':
    main()

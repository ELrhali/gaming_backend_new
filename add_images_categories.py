"""
Script pour ajouter des images aux catégories et sous-catégories
"""
import os
import sys
import django
import requests
from pathlib import Path
from django.core.files.base import ContentFile

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory

# Images pour les catégories (URLs d'images gaming de haute qualité)
CATEGORY_IMAGES = {
    'Composants': 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&q=80',
    'Périphériques': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&q=80',
    'Accessoires': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800&q=80',
}

# Images pour les sous-catégories
SUBCATEGORY_IMAGES = {
    'CARTE GRAPHIQUE': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&q=80',
    'PROCESSEUR': 'https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&q=80',
    'Processeurs': 'https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800&q=80',
    'CARTE MERE': 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800&q=80',
    'MEMOIRE RAM': 'https://images.unsplash.com/photo-1541746972996-4e0b0f43e02a?w=800&q=80',
    'STOCKAGE': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&q=80',
    'ALIMENTATION': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80',
    'BOITIER': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&q=80',
    'REFROIDISSEMENT': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&q=80',
    'VENTILATEUR': 'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800&q=80',
    'CLAVIER': 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800&q=80',
    'SOURIS': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
    'CASQUE': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80',
    'Auricular': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80',
    'ECRAN': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80',
    'WEBCAM': 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=80',
    'MICROPHONE': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80',
    'TAPIS': 'https://images.unsplash.com/photo-1616763355548-1b606f439f86?w=800&q=80',
    'JOYSTICK': 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&q=80',
    'STREAMING': 'https://images.unsplash.com/photo-1614294148960-9aa740632a87?w=800&q=80',
    'PATE THERMIQUE': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&q=80',
    'MODDING': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800&q=80',
}

def download_image(url, filename):
    """Télécharge une image depuis une URL"""
    try:
        print(f"  📥 Téléchargement: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return ContentFile(response.content, name=filename)
    except Exception as e:
        print(f"  ❌ Erreur lors du téléchargement: {e}")
        return None

def add_category_images():
    """Ajoute des images aux catégories"""
    print("\n=== AJOUT DES IMAGES DE CATEGORIES ===")
    
    updated_count = 0
    for category in Category.objects.all():
        if category.image:
            print(f"ℹ️  {category.name} a déjà une image")
            continue
        
        image_url = CATEGORY_IMAGES.get(category.name)
        if not image_url:
            print(f"⚠️  Pas d'image configurée pour: {category.name}")
            continue
        
        print(f"\n📂 Traitement de la catégorie: {category.name}")
        filename = f"{category.slug}.jpg"
        image_file = download_image(image_url, filename)
        
        if image_file:
            category.image.save(filename, image_file, save=True)
            updated_count += 1
            print(f"  ✅ Image ajoutée à {category.name}")
    
    print(f"\n📊 Total: {updated_count} images de catégories ajoutées")
    return updated_count

def add_subcategory_images():
    """Ajoute des images aux sous-catégories"""
    print("\n=== AJOUT DES IMAGES DE SOUS-CATEGORIES ===")
    
    updated_count = 0
    for subcategory in SubCategory.objects.all():
        if subcategory.image:
            print(f"ℹ️  {subcategory.name} a déjà une image")
            continue
        
        image_url = SUBCATEGORY_IMAGES.get(subcategory.name)
        if not image_url:
            print(f"⚠️  Pas d'image configurée pour: {subcategory.name}")
            continue
        
        print(f"\n📂 Traitement de la sous-catégorie: {subcategory.name}")
        filename = f"{subcategory.slug}.jpg"
        image_file = download_image(image_url, filename)
        
        if image_file:
            subcategory.image.save(filename, image_file, save=True)
            updated_count += 1
            print(f"  ✅ Image ajoutée à {subcategory.name}")
    
    print(f"\n📊 Total: {updated_count} images de sous-catégories ajoutées")
    return updated_count

def main():
    print("🖼️  AJOUT DES IMAGES AUX CATEGORIES ET SOUS-CATEGORIES")
    print("="*60)
    
    cat_count = add_category_images()
    subcat_count = add_subcategory_images()
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ AJOUT DES IMAGES TERMINE")
    print("="*60)
    print(f"Images de catégories ajoutées: {cat_count}")
    print(f"Images de sous-catégories ajoutées: {subcat_count}")
    print("="*60)

if __name__ == '__main__':
    main()

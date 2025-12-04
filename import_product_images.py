import os
import sys
import django
from pathlib import Path
from PIL import Image
import shutil

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, ProductImage
from django.core.files import File
from django.db.models.functions import Lower

# Chemin du dossier contenant les images
IMAGES_ROOT = r"C:\Users\MSI\Desktop\all-image-produits\Produits Mustang\Produits Mustang"

# Extensions d'images autorisées
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

def normalize_name(name):
    """Normalise un nom pour la comparaison (minuscules, espaces supprimés)"""
    return name.lower().strip()

def find_product_by_name(product_name):
    """Trouve un produit par son nom (insensible à la casse)"""
    normalized_search = normalize_name(product_name)
    
    # Chercher le produit avec une correspondance exacte (insensible à la casse)
    products = Product.objects.annotate(name_lower=Lower('name'))
    
    for product in products:
        if normalize_name(product.name) == normalized_search:
            return product
    
    return None

def get_image_files(directory):
    """Récupère tous les fichiers images d'un dossier"""
    if not os.path.exists(directory):
        return []
    
    image_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in IMAGE_EXTENSIONS:
                image_files.append(file_path)
    
    return sorted(image_files)  # Trier pour avoir un ordre cohérent

def copy_image_to_media(source_path, product, is_main=False):
    """Copie une image vers le dossier media et crée l'entrée en base"""
    try:
        # Vérifier que le fichier existe
        if not os.path.exists(source_path):
            print(f"   ⚠️  Fichier introuvable: {source_path}")
            return False
        
        # Générer le nom du fichier de destination
        filename = os.path.basename(source_path)
        destination_subdir = 'products/gallery/'
        
        # Chemin relatif pour Django (depuis media/)
        relative_path = os.path.join(destination_subdir, filename)
        
        # Vérifier si cette image existe déjà pour ce produit (basé sur le nom du fichier)
        existing_image = ProductImage.objects.filter(
            product=product,
            image__icontains=filename
        ).first()
        
        if existing_image:
            print(f"   ⏭️  Image déjà existante (ignorée): {filename}")
            return False
        
        # Ouvrir et vérifier l'image
        try:
            with Image.open(source_path) as img:
                img.verify()
        except Exception as e:
            print(f"   ⚠️  Image corrompue {os.path.basename(source_path)}: {e}")
            return False
        
        # Créer le dossier de destination s'il n'existe pas
        media_root = os.path.join(BASE_DIR, 'media', destination_subdir)
        os.makedirs(media_root, exist_ok=True)
        
        # Chemin absolu pour la copie
        destination_path = os.path.join(BASE_DIR, 'media', relative_path)
        
        # Copier le fichier seulement s'il n'existe pas déjà
        if not os.path.exists(destination_path):
            shutil.copy2(source_path, destination_path)
        
        # Si c'est l'image principale et qu'une image principale existe déjà, la remplacer
        if is_main:
            # Supprimer l'ancienne image principale si elle existe
            ProductImage.objects.filter(product=product, is_main=True).delete()
        
        # Créer l'entrée dans la base de données
        product_image = ProductImage.objects.create(
            product=product,
            image=relative_path,
            is_main=is_main,
            order=0 if is_main else ProductImage.objects.filter(product=product).count()
        )
        
        print(f"   ✅ Image {'principale' if is_main else 'ajoutée'}: {filename}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'import de {os.path.basename(source_path)}: {e}")
        return False

def process_product_folder(product_folder_path):
    """Traite un dossier de produit"""
    product_name = os.path.basename(product_folder_path)
    print(f"\n📦 Traitement: {product_name}")
    
    # Trouver le produit dans la base
    product = find_product_by_name(product_name)
    
    if not product:
        print(f"   ⚠️  Produit non trouvé dans la base de données: {product_name}")
        return {
            'status': 'not_found',
            'name': product_name
        }
    
    print(f"   ✓ Produit trouvé: {product.reference} - {product.name}")
    
    # Chercher le dossier de référence (premier sous-dossier)
    reference_folders = [d for d in os.listdir(product_folder_path) 
                        if os.path.isdir(os.path.join(product_folder_path, d))]
    
    if not reference_folders:
        print(f"   ⚠️  Aucun dossier de référence trouvé")
        return {
            'status': 'no_reference_folder',
            'name': product_name,
            'product': product
        }
    
    # Prendre le premier dossier de référence
    reference_folder = reference_folders[0]
    reference_path = os.path.join(product_folder_path, reference_folder)
    print(f"   📁 Dossier référence: {reference_folder}")
    
    # Chercher les dossiers Image et Menu (insensible à la casse)
    image_folder = None
    menu_folder = None
    
    for item in os.listdir(reference_path):
        item_path = os.path.join(reference_path, item)
        if os.path.isdir(item_path):
            item_lower = item.lower()
            if item_lower == 'image':
                image_folder = item_path
            elif item_lower == 'menu':
                menu_folder = item_path
    
    images_added = 0
    
    # Traiter l'image principale (dossier Image)
    if image_folder:
        print(f"   📸 Traitement de l'image principale...")
        image_files = get_image_files(image_folder)
        if image_files:
            # Prendre la première image comme image principale
            if copy_image_to_media(image_files[0], product, is_main=True):
                images_added += 1
        else:
            print(f"   ⚠️  Aucune image trouvée dans le dossier Image")
    else:
        print(f"   ⚠️  Dossier 'Image' non trouvé")
    
    # Traiter les images supplémentaires (dossier Menu)
    if menu_folder:
        print(f"   🖼️  Traitement des images supplémentaires...")
        menu_images = get_image_files(menu_folder)
        for image_path in menu_images:
            if copy_image_to_media(image_path, product, is_main=False):
                images_added += 1
    else:
        print(f"   ⚠️  Dossier 'Menu' non trouvé")
    
    return {
        'status': 'success',
        'name': product_name,
        'product': product,
        'images_count': images_added
    }

def main():
    """Fonction principale"""
    print("=" * 80)
    print("🚀 IMPORTATION DES IMAGES DE PRODUITS")
    print("=" * 80)
    
    if not os.path.exists(IMAGES_ROOT):
        print(f"❌ Erreur: Le dossier {IMAGES_ROOT} n'existe pas!")
        return
    
    print(f"\n📂 Dossier source: {IMAGES_ROOT}")
    
    # Lister tous les dossiers de produits
    product_folders = [
        os.path.join(IMAGES_ROOT, d) 
        for d in os.listdir(IMAGES_ROOT) 
        if os.path.isdir(os.path.join(IMAGES_ROOT, d))
    ]
    
    print(f"📊 Nombre de dossiers de produits trouvés: {len(product_folders)}")
    
    # Statistiques
    stats = {
        'total': len(product_folders),
        'success': 0,
        'not_found': 0,
        'errors': 0,
        'total_images': 0
    }
    
    not_found_products = []
    
    # Traiter chaque dossier
    for product_folder in product_folders:
        try:
            result = process_product_folder(product_folder)
            
            if result['status'] == 'success':
                stats['success'] += 1
                stats['total_images'] += result['images_count']
            elif result['status'] == 'not_found':
                stats['not_found'] += 1
                not_found_products.append(result['name'])
            else:
                stats['errors'] += 1
                
        except Exception as e:
            print(f"   ❌ Erreur inattendue: {e}")
            stats['errors'] += 1
    
    # Afficher les statistiques finales
    print("\n" + "=" * 80)
    print("📊 STATISTIQUES FINALES")
    print("=" * 80)
    print(f"✅ Produits traités avec succès: {stats['success']}/{stats['total']}")
    print(f"🖼️  Total d'images importées: {stats['total_images']}")
    print(f"⚠️  Produits non trouvés en base: {stats['not_found']}")
    print(f"❌ Erreurs: {stats['errors']}")
    
    if not_found_products:
        print(f"\n⚠️  Liste des produits non trouvés en base de données:")
        for product_name in not_found_products[:20]:  # Limiter à 20
            print(f"   - {product_name}")
        if len(not_found_products) > 20:
            print(f"   ... et {len(not_found_products) - 20} autres")
    
    print("\n✅ Importation terminée!")

if __name__ == "__main__":
    main()

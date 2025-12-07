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

def extract_reference_from_folder_name(folder_name):
    """Extrait le numéro de référence du nom du dossier
    
    Exemples:
    - "Carte mère ASUS ROG STRIX Z690-A GAMING WIFI D4" -> "Z690-A"
    - "Processeur Intel Core i7-12700K" -> "i7-12700K"
    - "MSI RTX 4090 GAMING X TRIO 24G" -> "RTX 4090" ou "4090"
    
    La fonction cherche les patterns courants de références:
    - Références avec tirets (ex: i7-12700K, RTX-4090)
    - Références alphanumériques (ex: Z690A, RTX4090)
    - Nombres seuls si précédés d'une marque connue
    """
    import re
    
    # Patterns de références courants
    patterns = [
        r'\b([A-Z0-9]+-[A-Z0-9-]+)\b',  # Format avec tirets: i7-12700K, RTX-4090
        r'\b(RTX\s*\d{4}\s*[A-Z]*|GTX\s*\d{4}\s*[A-Z]*)\b',  # Cartes graphiques NVIDIA
        r'\b(RX\s*\d{4}\s*[A-Z]*)\b',  # Cartes graphiques AMD
        r'\b([iI][3579]-\d{4,5}[A-Z]{0,2})\b',  # Processeurs Intel
        r'\b(Ryzen\s*[3579]\s*\d{4}[A-Z]{0,2})\b',  # Processeurs AMD Ryzen
        r'\b([A-Z]\d{3,4}[A-Z]*-[A-Z0-9]+)\b',  # Format type Z690-A, B550-F
        r'\b([A-Z]{2,}\d{3,})\b',  # Format alphanumérique: RTX4090, Z690A
    ]
    
    for pattern in patterns:
        match = re.search(pattern, folder_name, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def find_product_by_reference(folder_name):
    """Trouve un produit par son numéro de référence extrait du nom du dossier
    
    1. Extrait la référence du nom du dossier
    2. Cherche dans la base de données en comparant avec le champ 'reference'
    3. Si pas trouvé, cherche dans le nom du produit
    """
    # Extraire la référence du nom du dossier
    reference = extract_reference_from_folder_name(folder_name)
    
    if not reference:
        print(f"   ⚠️  Aucune référence trouvée dans: {folder_name}")
        # Fallback: chercher par nom complet
        normalized_search = normalize_name(folder_name)
        products = Product.objects.annotate(name_lower=Lower('name'))
        for product in products:
            if normalize_name(product.name) == normalized_search:
                return product
        return None
    
    # Nettoyer la référence
    reference_clean = reference.upper().strip()
    
    # 1. Chercher d'abord dans le champ reference (correspondance exacte)
    product = Product.objects.filter(reference__iexact=reference_clean).first()
    if product:
        return product
    
    # 2. Chercher dans le champ reference (contient)
    product = Product.objects.filter(reference__icontains=reference_clean).first()
    if product:
        return product
    
    # 3. Chercher dans le nom du produit (contient la référence)
    product = Product.objects.filter(name__icontains=reference).first()
    if product:
        return product
    
    # 4. Fallback: chercher par nom complet du dossier
    normalized_search = normalize_name(folder_name)
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
            print(f"   ERREUR: Fichier introuvable: {source_path}")
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
            print(f"   IGNORE: Image deja existante: {filename}")
            return False
        
        # Ouvrir et vérifier l'image
        try:
            with Image.open(source_path) as img:
                img.verify()
        except Exception as e:
            print(f"   ERREUR: Image corrompue {os.path.basename(source_path)}: {e}")
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
        
        print(f"   OK: Image {'principale' if is_main else 'ajoutee'}: {filename}")
        return True
        
    except Exception as e:
        print(f"   ERREUR lors de l'import de {os.path.basename(source_path)}: {e}")
        return False

def process_product_folder(product_folder_path):
    """Traite un dossier de produit
    Structure attendue:
    - Dossier produit (nom du produit)
      - Sous-dossier référence (numéro de référence du produit)
        - Image/ (contient l'image principale)
        - Menu/ (contient les images de la galerie)
    """
    folder_name = os.path.basename(product_folder_path)
    print(f"\nTraitement: {folder_name}")
    
    # Chercher le sous-dossier de référence (premier sous-dossier)
    reference_folders = [d for d in os.listdir(product_folder_path) 
                        if os.path.isdir(os.path.join(product_folder_path, d))]
    
    if not reference_folders:
        print(f"   ERREUR: Aucun sous-dossier trouve")
        return {
            'status': 'no_reference_folder',
            'name': folder_name
        }
    
    # Prendre le premier sous-dossier (qui contient le numéro de référence)
    reference_folder = reference_folders[0]
    reference_path = os.path.join(product_folder_path, reference_folder)
    print(f"   Sous-dossier reference: {reference_folder}")
    
    # Extraire la référence du NOM DU SOUS-DOSSIER
    detected_ref = extract_reference_from_folder_name(reference_folder)
    if detected_ref:
        print(f"   Reference detectee: {detected_ref}")
    else:
        print(f"   ATTENTION: Aucune reference detectee dans '{reference_folder}'")
    
    # Trouver le produit en utilisant le nom du sous-dossier de référence
    product = find_product_by_reference(reference_folder)
    
    if not product:
        print(f"   ERREUR: Produit non trouve")
        print(f"   Dossier: {folder_name}")
        print(f"   Reference recherchee: {reference_folder}")
        return {
            'status': 'not_found',
            'name': folder_name
        }
    
    print(f"   TROUVE: [{product.reference}] {product.name}")
    
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
        print(f"   Traitement image principale...")
        image_files = get_image_files(image_folder)
        if image_files:
            # Prendre la première image comme image principale
            if copy_image_to_media(image_files[0], product, is_main=True):
                images_added += 1
        else:
            print(f"   ATTENTION: Aucune image dans le dossier Image")
    else:
        print(f"   ATTENTION: Dossier 'Image' non trouve")
    
    # Traiter les images supplémentaires (dossier Menu)
    if menu_folder:
        print(f"   Traitement images supplementaires...")
        menu_images = get_image_files(menu_folder)
        for image_path in menu_images:
            if copy_image_to_media(image_path, product, is_main=False):
                images_added += 1
    else:
        print(f"   ATTENTION: Dossier 'Menu' non trouve")
    
    return {
        'status': 'success',
        'name': folder_name,
        'product': product,
        'images_count': images_added
    }

def main():
    """Fonction principale"""
    print("=" * 80)
    print("IMPORTATION DES IMAGES DE PRODUITS")
    print("=" * 80)
    
    if not os.path.exists(IMAGES_ROOT):
        print(f"ERREUR: Le dossier {IMAGES_ROOT} n'existe pas!")
        return
    
    print(f"\nDossier source: {IMAGES_ROOT}")
    
    # Lister tous les dossiers de produits
    product_folders = [
        os.path.join(IMAGES_ROOT, d) 
        for d in os.listdir(IMAGES_ROOT) 
        if os.path.isdir(os.path.join(IMAGES_ROOT, d))
    ]
    
    print(f"Nombre de dossiers de produits trouves: {len(product_folders)}")
    
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
            print(f"   ERREUR inattendue: {e}")
            stats['errors'] += 1
    
    # Afficher les statistiques finales
    print("\n" + "=" * 80)
    print("STATISTIQUES FINALES")
    print("=" * 80)
    print(f"OK: Produits traites avec succes: {stats['success']}/{stats['total']}")
    print(f"Images: Total d'images importees: {stats['total_images']}")
    print(f"ATTENTION: Produits non trouves en base: {stats['not_found']}")
    print(f"ERREUR: Erreurs: {stats['errors']}")
    
    if not_found_products:
        print(f"\nListe des produits non trouves en base de donnees:")
        for product_name in not_found_products[:20]:  # Limiter à 20
            print(f"   - {product_name}")
        if len(not_found_products) > 20:
            print(f"   ... et {len(not_found_products) - 20} autres")
    
    print("\nImportation terminee!")

if __name__ == "__main__":
    main()

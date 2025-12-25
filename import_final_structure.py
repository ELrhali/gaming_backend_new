import os
import sys
import django
import pandas as pd
from pathlib import Path
import shutil
from django.utils.text import slugify
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Collection, Category, SubCategory, Brand, Product, ProductImage

# Configuration
EXCEL_FILE = r'C:\Users\MSI\Desktop\gaming\old_data.xlsx'
MEDIA_ROOT = Path(r'C:\Users\MSI\Desktop\gaming\gaming_backend\media')

def parse_description(description):
    """Extrait les specifications depuis la description"""
    if pd.isna(description) or not description:
        return {}
    
    specs = {}
    lines = str(description).split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            specs[key.strip()] = value.strip()
    return specs

def copy_product_images(directory_path, reference):
    """Copie les images depuis directory_path vers media/products/reference/"""
    if pd.isna(directory_path) or not directory_path:
        return None, []
    
    source_dir = Path(directory_path)
    dest_dir = MEDIA_ROOT / 'products' / str(reference)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    main_image = None
    gallery_images = []
    
    # Chercher dans pic/ pour l'image principale
    pic_dir = source_dir / 'pic'
    if pic_dir.exists():
        images = list(pic_dir.glob('*'))
        images = [img for img in images if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        if images:
            main_src = images[0]
            main_dest = dest_dir / f'main{main_src.suffix}'
            try:
                shutil.copy2(main_src, main_dest)
                main_image = f'products/{reference}/main{main_src.suffix}'
                print(f"  [IMG] Image principale: {main_src.name}")
            except Exception as e:
                print(f"  [ERR] Erreur copie image principale: {e}")
    
    # Chercher dans pics/ pour la galerie
    pics_dir = source_dir / 'pics'
    if pics_dir.exists():
        images = list(pics_dir.glob('*'))
        images = [img for img in images if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        for idx, img_src in enumerate(images, 1):
            img_dest = dest_dir / f'gallery_{idx}{img_src.suffix}'
            try:
                shutil.copy2(img_src, img_dest)
                gallery_images.append(f'products/{reference}/gallery_{idx}{img_src.suffix}')
                print(f"  [IMG] Image {idx}: {img_src.name}")
            except Exception as e:
                print(f"  [ERR] Erreur copie image {idx}: {e}")
    
    # Si pas d'image dans pic/, chercher dans la racine
    if not main_image and source_dir.exists():
        images = list(source_dir.glob('*'))
        images = [img for img in images if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        if images:
            main_src = images[0]
            main_dest = dest_dir / f'main{main_src.suffix}'
            try:
                shutil.copy2(main_src, main_dest)
                main_image = f'products/{reference}/main{main_src.suffix}'
                print(f"  [IMG] Image principale (racine): {main_src.name}")
            except Exception as e:
                print(f"  [ERR] Erreur copie: {e}")
    
    return main_image, gallery_images

def generate_random_price():
    """Génère un prix aléatoire entre 50 et 2000 DH"""
    return round(random.uniform(50, 2000), 2)

def generate_random_quantity():
    """Génère une quantité aléatoire entre 0 et 100"""
    return random.randint(0, 100)

def main():
    print("\n" + "=" * 80)
    print("IMPORTATION AVEC NOUVELLE STRUCTURE")
    print("=" * 80)
    print("\nStructure:")
    print("  - 1er niveau     -> Collection")
    print("  - 2eme niveau    -> Category")
    print("  - Category       -> SubCategory")
    print("  - marque         -> Brand")
    print("=" * 80 + "\n")
    
    # Lire Excel
    df = pd.read_excel(EXCEL_FILE)
    print(f"[OK] Fichier charge: {len(df)} lignes\n")
    
    # Caches pour éviter les doublons
    collections_cache = {}
    categories_cache = {}
    subcategories_cache = {}
    brands_cache = {}
    
    # Stats
    stats = {
        'collections': 0,
        'categories': 0,
        'subcategories': 0,
        'brands': 0,
        'products': 0,
        'main_images': 0,
        'gallery_images': 0,
        'errors': 0
    }
    
    # Colonnes Excel (index 0-based)
    COL_1ER_NIVEAU = 0    # Collection
    COL_2EME_NIVEAU = 1   # Category
    COL_CATEGORY = 2      # SubCategory
    COL_MARQUE = 3        # Brand
    COL_REFERENCE = 4
    COL_NOM = 5
    COL_DESCRIPTION = 6
    COL_PRIX = 7
    COL_PRIX_REGULIER = 8
    COL_QTE = 9
    COL_DIRECTORY = 10
    COL_COLORIS = 11
    
    # Traiter chaque ligne
    for index, row in df.iterrows():
        line_num = index + 2  # Excel line number (header = 1)
        
        try:
            # Récupérer les valeurs
            premier_niveau = row.iloc[COL_1ER_NIVEAU] if not pd.isna(row.iloc[COL_1ER_NIVEAU]) else None
            deuxieme_niveau = row.iloc[COL_2EME_NIVEAU] if not pd.isna(row.iloc[COL_2EME_NIVEAU]) else None
            category_col = row.iloc[COL_CATEGORY] if not pd.isna(row.iloc[COL_CATEGORY]) else None
            marque = row.iloc[COL_MARQUE] if not pd.isna(row.iloc[COL_MARQUE]) else None
            reference = row.iloc[COL_REFERENCE] if not pd.isna(row.iloc[COL_REFERENCE]) else None
            nom = row.iloc[COL_NOM] if not pd.isna(row.iloc[COL_NOM]) else None
            description = row.iloc[COL_DESCRIPTION] if not pd.isna(row.iloc[COL_DESCRIPTION]) else ""
            prix = row.iloc[COL_PRIX] if not pd.isna(row.iloc[COL_PRIX]) else None
            prix_regulier = row.iloc[COL_PRIX_REGULIER] if not pd.isna(row.iloc[COL_PRIX_REGULIER]) else None
            qte = row.iloc[COL_QTE] if not pd.isna(row.iloc[COL_QTE]) else None
            directory_path = row.iloc[COL_DIRECTORY] if not pd.isna(row.iloc[COL_DIRECTORY]) else None
            
            # Vérifier les champs obligatoires
            if not reference or not nom:
                print(f"[{index+1}/{len(df)}] Ligne ignoree (pas de reference/nom)")
                continue
            
            print(f"\n[{index+1}/{len(df)}] {nom[:50]}... (Ref: {reference})")
            
            # 1. Créer/Récupérer la COLLECTION (1er niveau)
            collection = None
            if premier_niveau:
                collection_name = str(premier_niveau).strip()
                if collection_name not in collections_cache:
                    collection, created = Collection.objects.get_or_create(
                        name=collection_name,
                        defaults={
                            'slug': slugify(collection_name),
                            'description': f'Collection {collection_name}'
                        }
                    )
                    collections_cache[collection_name] = collection
                    if created:
                        stats['collections'] += 1
                        print(f"  [+] Collection: {collection_name}")
                else:
                    collection = collections_cache[collection_name]
            
            # 2. Créer/Récupérer la CATEGORY (2eme niveau)
            category = None
            if deuxieme_niveau:
                category_name = str(deuxieme_niveau).strip()
                category_key = category_name  # Clé unique par nom seulement
                
                if category_key not in categories_cache:
                    category, created = Category.objects.get_or_create(
                        name=category_name,
                        defaults={
                            'slug': slugify(category_name),
                            'description': f'Catégorie {category_name}',
                            'order': len(categories_cache) + 1
                        }
                    )
                    # Associer la collection si elle existe
                    if collection and not category.collection:
                        category.collection = collection
                        category.save()
                    
                    categories_cache[category_key] = category
                    if created:
                        stats['categories'] += 1
                        print(f"  [+] Categorie: {category_name}")
                else:
                    category = categories_cache[category_key]
            
            # 3. Créer/Récupérer la SUBCATEGORY (colonne Category)
            subcategory = None
            if category_col and category:
                subcategory_name = str(category_col).strip()
                # Clé unique par catégorie + nom (une sous-catégorie peut avoir le même nom dans différentes catégories)
                subcategory_key = f"{deuxieme_niveau}_{subcategory_name}"
                
                if subcategory_key not in subcategories_cache:
                    subcategory, created = SubCategory.objects.get_or_create(
                        name=subcategory_name,
                        category=category,
                        defaults={
                            'slug': slugify(f"{deuxieme_niveau}-{subcategory_name}"),
                            'description': f'Sous-catégorie {subcategory_name}',
                            'order': len(subcategories_cache) + 1
                        }
                    )
                    subcategories_cache[subcategory_key] = subcategory
                    if created:
                        stats['subcategories'] += 1
                        print(f"  [+] Sous-categorie: {subcategory_name}")
                else:
                    subcategory = subcategories_cache[subcategory_key]
            
            # 4. Créer/Récupérer la MARQUE
            brand = None
            if marque:
                if marque not in brands_cache:
                    brand, created = Brand.objects.get_or_create(
                        name=str(marque).strip(),
                        defaults={
                            'slug': slugify(marque),
                            'description': f'Marque {marque}'
                        }
                    )
                    brands_cache[marque] = brand
                    if created:
                        stats['brands'] += 1
                        print(f"  [+] Marque: {marque}")
                else:
                    brand = brands_cache[marque]
            
            # 5. Préparer les données du produit
            # Prix
            if prix:
                try:
                    product_price = float(prix)
                except:
                    product_price = generate_random_price()
            else:
                product_price = generate_random_price()
            
            # Prix régulier
            if prix_regulier:
                try:
                    regular_price = float(prix_regulier)
                except:
                    regular_price = None
            else:
                regular_price = None
            
            # Quantité
            if qte:
                try:
                    quantity = int(qte)
                except:
                    quantity = generate_random_quantity()
            else:
                quantity = generate_random_quantity()
            
            # Extraire les caractéristiques de la description
            caracteristiques = parse_description(description)
            caracteristiques_text = '\n'.join([f"{k}: {v}" for k, v in caracteristiques.items()])
            
            # 6. Copier les images
            main_image, gallery_images = copy_product_images(directory_path, reference)
            if main_image:
                stats['main_images'] += 1
            stats['gallery_images'] += len(gallery_images)
            
            # 7. Créer le PRODUIT
            product = Product.objects.create(
                reference=str(reference),
                name=str(nom),
                slug=slugify(f"{reference}-{nom}"),
                description=str(description) if description else "",
                caracteristiques=caracteristiques_text,
                price=product_price,
                discount_price=regular_price,
                quantity=quantity,
                collection=collection,
                category=category,
                subcategory=subcategory,
                brand=brand,
                main_image=main_image or '',
                status='published'
            )
            
            stats['products'] += 1
            print(f"  [OK] Produit cree | Prix: {product_price} DH | Stock: {quantity}")
            
            # 8. Créer les images de galerie
            for img_path in gallery_images:
                ProductImage.objects.create(
                    product=product,
                    image=img_path,
                    order=len(gallery_images)
                )
        
        except Exception as e:
            stats['errors'] += 1
            print(f"  [ERR] Erreur ligne {line_num}: {e}")
            continue
    
    # Résumé
    print("\n" + "=" * 80)
    print("RESUME DE L'IMPORTATION")
    print("=" * 80)
    print(f"[+] Collections creees      : {stats['collections']}")
    print(f"[+] Categories creees       : {stats['categories']}")
    print(f"[+] Sous-categories creees  : {stats['subcategories']}")
    print(f"[+] Marques creees          : {stats['brands']}")
    print(f"[+] Produits crees          : {stats['products']}")
    print(f"[IMG] Images principales    : {stats['main_images']}")
    print(f"[IMG] Images galerie        : {stats['gallery_images']}")
    print(f"[ERR] Erreurs               : {stats['errors']}")
    print("=" * 80)

if __name__ == '__main__':
    main()

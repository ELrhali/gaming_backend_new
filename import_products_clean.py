"""
Script pour importer tous les produits depuis le fichier Excel
avec leurs relations (catégorie, sous-catégorie, marque, type) et caractéristiques
"""
import os
import sys
import django
import pandas as pd
import re
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import (
    Category, SubCategory, Brand, Type, Product, 
    ProductSpecification, Collection
)
from django.utils.text import slugify
from django.db import transaction

def clean_data(value):
    """Nettoie les données du fichier Excel"""
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value.lower() in ['nan', '', 'none'] or value.startswith('Ex:'):
        return None
    return value

def parse_characteristics(text):
    """Parse les caractéristiques d'un texte formaté
    
    Formats supportés:
    -  Puissance: 850 Watts
    - Certification: 80 Plus Gold
    - - Ventilateur: 135mm
    """
    if not text or pd.isna(text):
        return []
    
    characteristics = []
    
    # Split par lignes
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Enlever les puces (, -, *, etc.)
        line = re.sub(r'^[\-\*\+]\s*', '', line)
        
        # Chercher le pattern "Clé: Valeur"
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            if key and value:
                characteristics.append((key, value))
    
    return characteristics

def normalize_name(name):
    """Normalise un nom pour la recherche (insensible à la casse)"""
    if not name:
        return None
    return name.strip().upper()

def get_or_create_category(name):
    """Récupère ou crée une catégorie"""
    if not name:
        return None
    
    name = clean_data(name)
    if not name:
        return None
    
    # Chercher par nom (case-insensitive)
    category = Category.objects.filter(name__iexact=name).first()
    
    if not category:
        print(f"  Catégorie non trouvée: {name}")
        return None
    
    return category

def get_or_create_subcategory(name, category):
    """Récupère ou crée une sous-catégorie"""
    if not name or not category:
        return None
    
    name = clean_data(name)
    if not name:
        return None
    
    # Mapping des noms pour correspondre avec la base
    name_mapping = {
        'ALIMENTATION': 'Alimentations',
        'ALIMENTATIONS': 'Alimentations',
        'BOITIER': 'Boîtiers PC',
        'BOÎTIER': 'Boîtiers PC',
        'BOITIERS': 'Boîtiers PC',
        'WEBCAM': 'Webcams',
        'WEBCAMS': 'Webcams',
        'PROCESSEUR': 'Processeurs',
        'PROCESSEURS': 'Processeurs',
        'AURICULAR': 'Casques Audio',
        'CASQUE': 'Casques Audio',
        'CASQUES': 'Casques Audio',
        'ECRAN': 'Écrans',
        'ÉCRAN': 'Écrans',
        'ECRANS': 'Écrans',
        'ÉCRANS': 'Écrans',
        'ECRAN PC': 'Écrans',
        'ÉCRAN PC': 'Écrans',
        'CARTE GRAPHIQUE': 'Cartes Graphiques',
        'CARTES GRAPHIQUES': 'Cartes Graphiques',
        'JOYSTICK': 'Joysticks',
        'JOYSTICKS': 'Joysticks',
        'CLAVIER': 'Claviers Gaming',
        'CLAVIERS': 'Claviers Gaming',
        'CLAVIERS GAMING': 'Claviers Gaming',
        'CARTE MERE': 'Cartes Mères',
        'CARTES MÈRES': 'Cartes Mères',
        'CARTES MERES': 'Cartes Mères',
        'MICROPHONE': 'Microphones',
        'MICROPHONES': 'Microphones',
        'MODDING': 'Modding',
        'MEMOIRE RAM': 'Mémoire RAM',
        'MÉMOIRE RAM': 'Mémoire RAM',
        'PATE THERMIQUE': 'Pâte Thermique',
        'PÂTE THERMIQUE': 'Pâte Thermique',
        'SOURIS': 'Souris Gaming',
        'STREAMING': 'Streaming',
        'TAPIS': 'Tapis de Souris',
        'TAPIS DE SOURIS': 'Tapis de Souris',
        'VENTILATEUR': 'Ventilateurs',
        'VENTILATEURS': 'Ventilateurs',
        'REFROIDISSEMENT': 'Refroidissement',
        'STOCKAGE': 'Stockage',
    }
    
    # Appliquer le mapping
    normalized_name = name_mapping.get(name.upper(), name)
    
    # Chercher par nom et catégorie (case-insensitive)
    subcategory = SubCategory.objects.filter(
        name__iexact=normalized_name,
        category=category
    ).first()
    
    if not subcategory:
        print(f"  Sous-catégorie non trouvée: {name} -> {normalized_name} dans {category.name}")
        return None
    
    return subcategory

def get_or_create_brand(name):
    """Récupère ou crée une marque"""
    if not name:
        return None
    
    name = clean_data(name)
    if not name:
        return None
    
    # Ignorer les exemples avec plusieurs marques séparées par des virgules
    if ',' in name:
        return None
    
    # Chercher par nom (case-insensitive)
    brand = Brand.objects.filter(name__iexact=name).first()
    
    if not brand:
        # Créer la marque si elle n'existe pas
        brand = Brand.objects.create(
            name=name,
            slug=slugify(name),
            is_active=True
        )
        print(f"    Marque créée: {name}")
    
    return brand

def get_or_create_type(name, subcategory, brand):
    """Récupère ou crée un type"""
    if not name or not subcategory:
        return None
    
    name = clean_data(name)
    if not name:
        return None
    
    # Ignorer les exemples
    if ',' in name:
        return None
    
    # Chercher le type existant
    type_obj = Type.objects.filter(
        name__iexact=name,
        subcategory=subcategory,
        brand=brand
    ).first()
    
    if not type_obj:
        # Créer le type
        slug = slugify(f"{brand.name if brand else ''}-{name}")
        counter = 1
        original_slug = slug
        
        while Type.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        type_obj = Type.objects.create(
            name=name,
            subcategory=subcategory,
            brand=brand,
            slug=slug,
            is_active=True
        )
        print(f"    Type créé: {name}")
    
    return type_obj

def get_or_create_collection(name):
    """Récupère ou crée une collection"""
    if not name:
        return None
    
    name = clean_data(name)
    if not name:
        return None
    
    collection = Collection.objects.filter(name__iexact=name).first()
    
    if not collection:
        collection = Collection.objects.create(
            name=name,
            slug=slugify(name),
            is_active=True
        )
        print(f"    Collection créée: {name}")
    
    return collection

def parse_status(status_text):
    """Parse le statut du produit"""
    if not status_text:
        return 'in_stock'
    
    status_text = clean_data(status_text)
    if not status_text:
        return 'in_stock'
    
    status_map = {
        'en stock': 'in_stock',
        'in_stock': 'in_stock',
        'rupture': 'out_of_stock',
        'out_of_stock': 'out_of_stock',
        'rupture de stock': 'out_of_stock',
        'précommande': 'preorder',
        'preorder': 'preorder',
        'discontinué': 'discontinued',
        'discontinued': 'discontinued',
    }
    
    return status_map.get(status_text.lower(), 'in_stock')

def parse_boolean(value):
    """Parse une valeur booléenne"""
    if pd.isna(value):
        return False
    
    if isinstance(value, bool):
        return value
    
    value = str(value).strip().lower()
    return value in ['oui', 'yes', 'true', '1', 'vrai']

def import_products(excel_file):
    """Importe tous les produits depuis le fichier Excel"""
    
    print(f"\nLecture du fichier: {excel_file}")
    df = pd.read_excel(excel_file)
    
    print(f"Nombre total de lignes: {len(df)}")
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            # Vérifier les champs obligatoires
            reference = clean_data(row.get('Référence *'))
            name = clean_data(row.get('Nom du produit *'))
            cat_name = clean_data(row.get('Catégorie *'))
            subcat_name = clean_data(row.get('Sous-catégorie *'))
            price = row.get('Prix (DH) *')
            quantity = row.get('Quantité *')
            description = clean_data(row.get('Description *'))
            
            # Vérifier que les champs obligatoires sont présents
            if not reference or not name or not cat_name or not subcat_name:
                print(f"\n  Ligne {index + 2}: Données obligatoires manquantes - IGNORÉE")
                skipped_count += 1
                continue
            
            # Vérifier et nettoyer le prix et la quantité
            if pd.isna(price) or str(price).strip() in ['-', '', 'nan']:
                print(f"\n  Ligne {index + 2}: Prix invalide - IGNORÉE")
                skipped_count += 1
                continue
            
            if pd.isna(quantity) or str(quantity).strip() in ['-', '', 'nan']:
                print(f"\n  Ligne {index + 2}: Quantité invalide - IGNORÉE")
                skipped_count += 1
                continue
            
            # Convertir en nombres
            try:
                price = float(price)
                quantity = int(float(quantity))
            except (ValueError, TypeError):
                print(f"\n  Ligne {index + 2}: Prix ou quantité invalide - IGNORÉE")
                skipped_count += 1
                continue
            
            print(f"\nTraitement: {reference} - {name}")
            
            # Vérifier si le produit existe déjà
            existing_product = Product.objects.filter(reference=reference).first()
            
            if existing_product:
                print(f"     Produit existe déjà: {reference} - IGNORÉ")
                skipped_count += 1
                continue
            
            # Récupérer les relations
            category = get_or_create_category(cat_name)
            if not category:
                print(f"    Catégorie invalide - IGNORÉ")
                skipped_count += 1
                continue
            
            subcategory = get_or_create_subcategory(subcat_name, category)
            if not subcategory:
                print(f"    Sous-catégorie invalide - IGNORÉ")
                skipped_count += 1
                continue
            
            brand_name = clean_data(row.get('Marque'))
            brand = get_or_create_brand(brand_name) if brand_name else None
            
            type_name = clean_data(row.get('Type'))
            type_obj = get_or_create_type(type_name, subcategory, brand) if type_name else None
            
            collection_name = clean_data(row.get('Collection'))
            collection = get_or_create_collection(collection_name) if collection_name else None
            
            # Créer le produit
            with transaction.atomic():
                # Créer le slug unique
                slug = slugify(f"{reference}-{name}")
                counter = 1
                original_slug = slug
                
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                # Préparer les données du produit
                product_data = {
                    'reference': reference,
                    'name': name,
                    'slug': slug,
                    'category': category,
                    'subcategory': subcategory,
                    'type': type_obj,
                    'collection': collection,
                    'price': price,
                    'quantity': quantity,
                    'description': description or '',
                    'status': parse_status(row.get('Statut')),
                    'brand_text': brand_name or '',
                }
                
                # Ajouter brand_id pour la relation FK
                if brand:
                    product_data['brand_id'] = brand.id
                
                # Champs optionnels
                discount_price = row.get('Prix Promo (DH)')
                if not pd.isna(discount_price) and discount_price:
                    product_data['discount_price'] = float(discount_price)
                
                caracteristiques = clean_data(row.get('Caractéristiques'))
                if caracteristiques:
                    product_data['caracteristiques'] = caracteristiques
                
                warranty = clean_data(row.get('Garantie'))
                if warranty:
                    product_data['warranty'] = warranty
                
                weight = row.get('Poids (kg)')
                if not pd.isna(weight) and weight:
                    product_data['weight'] = float(weight)
                
                meta_title = clean_data(row.get('Meta Titre SEO'))
                if meta_title:
                    product_data['meta_title'] = meta_title
                
                meta_description = clean_data(row.get('Meta Description SEO'))
                if meta_description:
                    product_data['meta_description'] = meta_description
                
                # Flags booléens
                product_data['is_bestseller'] = parse_boolean(row.get('Best Seller'))
                product_data['is_featured'] = parse_boolean(row.get('En vedette'))
                product_data['is_new'] = parse_boolean(row.get('Nouveau'))
                
                # Créer le produit directement avec SQL brut pour éviter le conflit des champs brand
                from django.db import connection
                cursor = connection.cursor()
                
                sql = """
                    INSERT INTO shop_product (
                        reference, name, slug, category_id, subcategory_id, type_id, collection_id,
                        brand, brand_text, brand_id, price, discount_price, quantity, status,
                        description, caracteristiques, warranty, weight, meta_title, meta_description,
                        is_bestseller, is_featured, is_new, show_in_ad_slider, views_count,
                        created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        NOW(), NOW()
                    )
                """
                
                cursor.execute(sql, [
                    reference, name, slug, category.id, subcategory.id,
                    type_obj.id if type_obj else None, collection.id if collection else None,
                    brand_name or '', brand_name or '', brand.id if brand else None,
                    price, product_data.get('discount_price'), quantity, product_data['status'],
                    description or '', product_data.get('caracteristiques') or '', product_data.get('warranty') or '',
                    product_data.get('weight'), product_data.get('meta_title') or '', product_data.get('meta_description') or '',
                    product_data['is_bestseller'], product_data['is_featured'], product_data['is_new'],
                    False, 0
                ])
                
                product_id = cursor.lastrowid
                product = Product.objects.get(id=product_id)
                
                # Ajouter les caractéristiques détaillées
                characteristics_text = clean_data(row.get('Caractéristiques'))
                if characteristics_text:
                    characteristics = parse_characteristics(characteristics_text)
                    
                    for order, (key, value) in enumerate(characteristics, 1):
                        ProductSpecification.objects.create(
                            product=product,
                            key=key,
                            value=value,
                            order=order
                        )
                    
                    if characteristics:
                        print(f"    {len(characteristics)} caractéristiques ajoutées")
                
                created_count += 1
                print(f"    Produit créé: {reference}")
        
        except Exception as e:
            error_msg = f"Ligne {index + 2}: {str(e)}"
            errors.append(error_msg)
            print(f"    ERREUR: {error_msg}")
            skipped_count += 1
    
    # Résumé final
    print("\n" + "="*70)
    print("IMPORTATION TERMINEE")
    print("="*70)
    print(f"Produits créés: {created_count}")
    print(f"Produits ignorés (doublons ou incomplets): {skipped_count}")
    print(f"Erreurs: {len(errors)}")
    
    if errors:
        print("\nERREURS DETAILLEES:")
        for error in errors[:10]:  # Afficher les 10 premières erreurs
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... et {len(errors) - 10} autres erreurs")
    
    print("="*70)
    
    # Statistiques finales
    print("\nSTATISTIQUES FINALES:")
    print(f"    Total produits en base: {Product.objects.count()}")
    print(f"    Total catégories: {Category.objects.count()}")
    print(f"    Total sous-catégories: {SubCategory.objects.count()}")
    print(f"    Total marques: {Brand.objects.count()}")
    print(f"    Total types: {Type.objects.count()}")
    print(f"    Total collections: {Collection.objects.count()}")
    print("="*70)

def main():
    # Chemin du fichier Excel
    excel_file = Path(__file__).parent.parent / 'e-commece' / 'public' / 'data_product.xlsx'
    
    if not excel_file.exists():
        print(f"Fichier non trouve: {excel_file}")
        return
    
    print("IMPORTATION DES PRODUITS DEPUIS EXCEL")
    print("="*70)
    
    import_products(excel_file)

if __name__ == '__main__':
    main()


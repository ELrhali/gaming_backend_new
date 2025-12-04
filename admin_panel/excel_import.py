"""
Module pour l'importation de produits depuis Excel via l'interface admin
"""
import pandas as pd
import re
from django.db import transaction, connection
from django.utils.text import slugify
from shop.models import (
    Category, SubCategory, Brand, Type, Product, 
    ProductSpecification, Collection
)

def clean_data(value):
    """Nettoie les données du fichier Excel"""
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value.lower() in ['nan', '', 'none'] or value.startswith('Ex:'):
        return None
    return value

def parse_characteristics(text):
    """Parse les caractéristiques d'un texte formaté"""
    if not text or pd.isna(text):
        return []
    
    characteristics = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Enlever les puces
        line = re.sub(r'^[•\-\*\+]\s*', '', line)
        
        # Chercher le pattern "Clé: Valeur"
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            if key and value:
                characteristics.append((key, value))
    
    return characteristics

def normalize_subcategory_name(name):
    """Normalise le nom d'une sous-catégorie pour correspondre à la base"""
    if not name:
        return None
    
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
        'CARTE GRAPHIQUE': 'Cartes Graphiques',
        'CARTES GRAPHIQUES': 'Cartes Graphiques',
        'JOYSTICK': 'Joysticks',
        'JOYSTICKS': 'Joysticks',
        'CLAVIER': 'Claviers Gaming',
        'CLAVIERS': 'Claviers Gaming',
        'CARTE MERE': 'Cartes Mères',
        'CARTES MÈRES': 'Cartes Mères',
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
    
    return name_mapping.get(name.upper(), name)

def parse_status(status_text):
    """Parse le statut du produit"""
    if not status_text:
        return 'in_stock'
    
    status_text = clean_data(status_text)
    if not status_text:
        return 'in_stock'
    
    status_map = {
        'en stock': 'in_stock',
        'rupture': 'out_of_stock',
        'rupture de stock': 'out_of_stock',
        'précommande': 'preorder',
        'discontinué': 'discontinued',
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

class ExcelImporter:
    """Classe pour gérer l'importation de produits depuis Excel"""
    
    def __init__(self):
        self.created_products = 0
        self.updated_products = 0
        self.skipped_products = 0
        self.errors = []
        self.created_brands = []
        self.created_types = []
        self.created_collections = []
    
    def get_or_create_category(self, name):
        """Récupère une catégorie"""
        if not name:
            return None
        
        name = clean_data(name)
        if not name:
            return None
        
        category = Category.objects.filter(name__iexact=name).first()
        if not category:
            self.errors.append(f"Catégorie '{name}' non trouvée")
            return None
        
        return category
    
    def get_or_create_subcategory(self, name, category):
        """Récupère une sous-catégorie"""
        if not name or not category:
            return None
        
        name = clean_data(name)
        if not name:
            return None
        
        normalized_name = normalize_subcategory_name(name)
        
        subcategory = SubCategory.objects.filter(
            name__iexact=normalized_name,
            category=category
        ).first()
        
        if not subcategory:
            self.errors.append(f"Sous-catégorie '{name}' -> '{normalized_name}' non trouvée dans {category.name}")
            return None
        
        return subcategory
    
    def get_or_create_brand(self, name):
        """Récupère ou crée une marque"""
        if not name:
            return None
        
        name = clean_data(name)
        if not name or ',' in name:
            return None
        
        brand = Brand.objects.filter(name__iexact=name).first()
        
        if not brand:
            brand = Brand.objects.create(
                name=name,
                slug=slugify(name),
                is_active=True
            )
            self.created_brands.append(name)
        
        return brand
    
    def get_or_create_type(self, name, subcategory, brand):
        """Récupère ou crée un type"""
        if not name or not subcategory:
            return None
        
        name = clean_data(name)
        if not name or ',' in name:
            return None
        
        type_obj = Type.objects.filter(
            name__iexact=name,
            subcategory=subcategory,
            brand=brand
        ).first()
        
        if not type_obj:
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
            self.created_types.append(f"{name} ({brand.name if brand else 'Sans marque'})")
        
        return type_obj
    
    def get_or_create_collection(self, name):
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
            self.created_collections.append(name)
        
        return collection
    
    def import_from_excel(self, file_path):
        """Importe tous les produits depuis un fichier Excel"""
        
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            return {
                'success': False,
                'error': f"Erreur de lecture du fichier: {str(e)}"
            }
        
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
                
                # Vérifier données obligatoires
                if not reference or not name or not cat_name or not subcat_name:
                    self.skipped_products += 1
                    continue
                
                # Vérifier prix et quantité
                if pd.isna(price) or str(price).strip() in ['-', '', 'nan']:
                    self.skipped_products += 1
                    continue
                
                if pd.isna(quantity) or str(quantity).strip() in ['-', '', 'nan']:
                    self.skipped_products += 1
                    continue
                
                try:
                    price = float(price)
                    quantity = int(float(quantity))
                except (ValueError, TypeError):
                    self.skipped_products += 1
                    continue
                
                # Vérifier si le produit existe déjà
                existing_product = Product.objects.filter(reference=reference).first()
                if existing_product:
                    self.skipped_products += 1
                    continue
                
                # Récupérer les relations
                category = self.get_or_create_category(cat_name)
                if not category:
                    self.skipped_products += 1
                    continue
                
                subcategory = self.get_or_create_subcategory(subcat_name, category)
                if not subcategory:
                    self.skipped_products += 1
                    continue
                
                brand_name = clean_data(row.get('Marque'))
                brand = self.get_or_create_brand(brand_name) if brand_name else None
                
                type_name = clean_data(row.get('Type'))
                type_obj = self.get_or_create_type(type_name, subcategory, brand) if type_name else None
                
                collection_name = clean_data(row.get('Collection'))
                collection = self.get_or_create_collection(collection_name) if collection_name else None
                
                # Créer le slug unique
                slug = slugify(f"{reference}-{name}")
                counter = 1
                original_slug = slug
                
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                # Préparer les données
                discount_price = row.get('Prix Promo (DH)')
                if not pd.isna(discount_price) and discount_price:
                    try:
                        discount_price = float(discount_price)
                    except:
                        discount_price = None
                else:
                    discount_price = None
                
                caracteristiques = clean_data(row.get('Caractéristiques'))
                warranty = clean_data(row.get('Garantie'))
                
                weight = row.get('Poids (kg)')
                if not pd.isna(weight) and weight:
                    try:
                        weight = float(weight)
                    except:
                        weight = None
                else:
                    weight = None
                
                meta_title = clean_data(row.get('Meta Titre SEO'))
                meta_description = clean_data(row.get('Meta Description SEO'))
                
                is_bestseller = parse_boolean(row.get('Best Seller'))
                is_featured = parse_boolean(row.get('En vedette'))
                is_new = parse_boolean(row.get('Nouveau'))
                status = parse_status(row.get('Statut'))
                
                # Créer le produit avec SQL brut pour éviter les conflits
                with transaction.atomic():
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
                        price, discount_price, quantity, status,
                        description or '', caracteristiques or '', warranty or '',
                        weight, meta_title or '', meta_description or '',
                        is_bestseller, is_featured, is_new,
                        False, 0
                    ])
                    
                    product_id = cursor.lastrowid
                    product = Product.objects.get(id=product_id)
                    
                    # Ajouter les caractéristiques détaillées
                    if caracteristiques:
                        characteristics = parse_characteristics(caracteristiques)
                        
                        for order, (key, value) in enumerate(characteristics, 1):
                            ProductSpecification.objects.create(
                                product=product,
                                key=key,
                                value=value,
                                order=order
                            )
                    
                    self.created_products += 1
            
            except Exception as e:
                error_msg = f"Ligne {index + 2}: {str(e)}"
                self.errors.append(error_msg)
                self.skipped_products += 1
        
        return {
            'success': True,
            'created': self.created_products,
            'skipped': self.skipped_products,
            'errors': self.errors,
            'created_brands': self.created_brands,
            'created_types': self.created_types,
            'created_collections': self.created_collections
        }

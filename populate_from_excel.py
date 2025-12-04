"""
Script pour peupler la base de données avec les catégories, sous-catégories, marques et types
depuis le fichier Excel data_product.xlsx
"""
import os
import sys
import django
import pandas as pd
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Brand, Type
from django.utils.text import slugify

# Images par défaut pour les catégories
CATEGORY_IMAGES = {
    'Composants': 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800',  # PC Components
    'Périphériques': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800',  # Gaming peripherals
    'Accessoires': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800',  # Gaming accessories
}

# Images par défaut pour les sous-catégories
SUBCATEGORY_IMAGES = {
    'CARTE GRAPHIQUE': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800',
    'PROCESSEUR': 'https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=800',
    'CARTE MERE': 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=800',
    'MEMOIRE RAM': 'https://images.unsplash.com/photo-1541746972996-4e0b0f43e02a?w=800',
    'STOCKAGE': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800',
    'ALIMENTATION': 'https://images.unsplash.com/photo-1585438166269-3f082d1a40c7?w=800',
    'BOITIER': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800',
    'REFROIDISSEMENT': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800',
    'VENTILATEUR': 'https://images.unsplash.com/photo-1587202372616-b43abea06c2a?w=800',
    'CLAVIER': 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=800',
    'SOURIS': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800',
    'CASQUE': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800',
    'ECRAN': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800',
    'WEBCAM': 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800',
    'MICROPHONE': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800',
    'TAPIS': 'https://images.unsplash.com/photo-1616763355548-1b606f439f86?w=800',
    'JOYSTICK': 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800',
    'STREAMING': 'https://images.unsplash.com/photo-1614294148960-9aa740632a87?w=800',
    'PATE THERMIQUE': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800',
    'MODDING': 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=800',
}

def clean_data(value):
    """Nettoie les données du fichier Excel"""
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value.startswith('Ex:') or value == 'nan':
        return None
    return value

def populate_categories(df):
    """Ajoute toutes les catégories uniques"""
    print("\n=== AJOUT DES CATEGORIES ===")
    categories = df['Catégorie *'].dropna().unique()
    
    created_count = 0
    for idx, cat_name in enumerate(categories, 1):
        cat_name = clean_data(cat_name)
        if not cat_name:
            continue
            
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={
                'slug': slugify(cat_name),
                'description': f'Découvrez notre gamme de {cat_name.lower()}',
                'order': idx,
                'is_active': True,
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Catégorie créée: {cat_name}")
        else:
            print(f"ℹ️  Catégorie existe déjà: {cat_name}")
    
    print(f"\n📊 Total: {created_count} catégories créées")
    return created_count

def populate_subcategories(df):
    """Ajoute toutes les sous-catégories uniques"""
    print("\n=== AJOUT DES SOUS-CATEGORIES ===")
    
    created_count = 0
    processed = set()  # Pour éviter les doublons
    
    # Grouper par catégorie et sous-catégorie
    for _, row in df.iterrows():
        cat_name = clean_data(row['Catégorie *'])
        subcat_name = clean_data(row['Sous-catégorie *'])
        
        if not cat_name or not subcat_name:
            continue
        
        # Éviter de traiter la même combinaison deux fois
        combo_key = f"{cat_name}|{subcat_name}"
        if combo_key in processed:
            continue
        processed.add(combo_key)
        
        try:
            category = Category.objects.get(name=cat_name)
        except Category.DoesNotExist:
            print(f"⚠️  Catégorie '{cat_name}' non trouvée pour sous-catégorie '{subcat_name}'")
            continue
        
        # Vérifier si la sous-catégorie existe déjà pour cette catégorie
        subcategory = SubCategory.objects.filter(
            name=subcat_name,
            category=category
        ).first()
        
        if subcategory:
            print(f"ℹ️  Sous-catégorie existe déjà: {subcat_name} (Catégorie: {cat_name})")
            continue
        
        # Créer un slug unique en incluant la catégorie si nécessaire
        base_slug = slugify(subcat_name)
        slug = base_slug
        counter = 1
        
        # S'assurer que le slug est unique
        while SubCategory.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        subcategory = SubCategory.objects.create(
            name=subcat_name,
            category=category,
            slug=slug,
            description=f'Découvrez nos {subcat_name.lower()}',
            order=0,
            is_active=True,
        )
        
        created_count += 1
        print(f"✅ Sous-catégorie créée: {subcat_name} (Catégorie: {cat_name}, Slug: {slug})")
    
    print(f"\n📊 Total: {created_count} sous-catégories créées")
    return created_count

def populate_brands(df):
    """Ajoute toutes les marques uniques"""
    print("\n=== AJOUT DES MARQUES ===")
    brands = df['Marque'].dropna().unique()
    
    created_count = 0
    for idx, brand_name in enumerate(brands, 1):
        brand_name = clean_data(brand_name)
        if not brand_name or ',' in brand_name:  # Ignorer les exemples avec plusieurs marques
            continue
            
        brand, created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={
                'slug': slugify(brand_name),
                'description': f'Produits de la marque {brand_name}',
                'order': idx,
                'is_active': True,
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Marque créée: {brand_name}")
        else:
            print(f"ℹ️  Marque existe déjà: {brand_name}")
    
    print(f"\n📊 Total: {created_count} marques créées")
    return created_count

def populate_types(df):
    """Ajoute tous les types uniques"""
    print("\n=== AJOUT DES TYPES ===")
    
    created_count = 0
    processed = set()  # Pour éviter les doublons
    
    # Grouper par sous-catégorie, marque et type
    for _, row in df.iterrows():
        cat_name = clean_data(row['Catégorie *'])
        subcat_name = clean_data(row['Sous-catégorie *'])
        brand_name = clean_data(row['Marque'])
        type_name = clean_data(row['Type'])
        
        if not subcat_name or not type_name or ',' in str(type_name):
            continue
        
        # Éviter de traiter la même combinaison deux fois
        combo_key = f"{cat_name}|{subcat_name}|{brand_name}|{type_name}"
        if combo_key in processed:
            continue
        processed.add(combo_key)
        
        try:
            subcategory = SubCategory.objects.filter(
                name=subcat_name,
                category__name=cat_name
            ).first()
            
            if not subcategory:
                print(f"⚠️  Sous-catégorie '{subcat_name}' non trouvée pour type '{type_name}'")
                continue
        except Exception as e:
            print(f"⚠️  Erreur lors de la recherche de sous-catégorie '{subcat_name}': {e}")
            continue
        
        brand = None
        if brand_name and ',' not in brand_name:
            try:
                brand = Brand.objects.get(name=brand_name)
            except Brand.DoesNotExist:
                pass
        
        # Vérifier si le type existe déjà
        existing_type = Type.objects.filter(
            name=type_name,
            subcategory=subcategory,
            brand=brand
        ).first()
        
        if existing_type:
            brand_info = f" (Marque: {brand_name})" if brand_name else ""
            print(f"ℹ️  Type existe déjà: {type_name}{brand_info} - Sous-catégorie: {subcat_name}")
            continue
        
        # Créer un slug unique
        base_slug = slugify(f"{brand_name}-{type_name}" if brand_name else type_name)
        slug = base_slug
        counter = 1
        
        # S'assurer que le slug est unique
        while Type.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        type_obj = Type.objects.create(
            name=type_name,
            subcategory=subcategory,
            brand=brand,
            slug=slug,
            description=f'Type {type_name}',
            order=0,
            is_active=True,
        )
        
        created_count += 1
        brand_info = f" (Marque: {brand_name})" if brand_name else ""
        print(f"✅ Type créé: {type_name}{brand_info} - Sous-catégorie: {subcat_name} (Slug: {slug})")
    
    print(f"\n📊 Total: {created_count} types créés")
    return created_count

def main():
    # Chemin du fichier Excel
    excel_file = Path(__file__).parent.parent / 'e-commece' / 'public' / 'data_product.xlsx'
    
    if not excel_file.exists():
        print(f"❌ Fichier non trouvé: {excel_file}")
        return
    
    print(f"📁 Lecture du fichier: {excel_file}")
    df = pd.read_excel(excel_file)
    
    print(f"📊 Nombre total de lignes: {len(df)}")
    
    # Afficher les colonnes disponibles
    print(f"\n📋 Colonnes disponibles: {list(df.columns)}")
    
    # Peupler la base de données
    cat_count = populate_categories(df)
    subcat_count = populate_subcategories(df)
    brand_count = populate_brands(df)
    type_count = populate_types(df)
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ IMPORTATION TERMINEE")
    print("="*60)
    print(f"Catégories créées: {cat_count}")
    print(f"Sous-catégories créées: {subcat_count}")
    print(f"Marques créées: {brand_count}")
    print(f"Types créés: {type_count}")
    print("="*60)

if __name__ == '__main__':
    main()

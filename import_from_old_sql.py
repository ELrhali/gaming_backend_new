"""
Script d'importation et adaptation des données SQL vers la structure Django Gobag.ma

Mapping:
- Table SQL 'types' → Model Django 'Category'
- Table SQL 'categories' → Model Django 'SubCategory'  
- Table SQL 'produits' + 'produit_categories' → Model Django 'Product'
- Table SQL 'category_images' → Images des SubCategory
- Table SQL 'marques' → Model Django 'Brand'
"""

import os
import django
import pymysql
from datetime import datetime
from django.utils.text import slugify

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Type, Brand, Product, ProductImage

# Connexion à la base de données source
def connect_source_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='gobagma_boutique_valises_maroc',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def import_brands():
    """Importer les marques"""
    print("\n📦 IMPORTATION DES MARQUES...")
    print("="*80)
    
    conn = connect_source_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nom, description, image, is_active
        FROM marques
        WHERE deleted_at IS NULL
    """)
    
    marques = cursor.fetchall()
    brand_mapping = {}
    
    for marque in marques:
        try:
            # Créer ou récupérer la marque
            brand, created = Brand.objects.get_or_create(
                name=marque['nom'],
                defaults={
                    'description': marque['description'] or '',
                    'is_active': bool(marque['is_active'])
                }
            )
            brand_mapping[marque['id']] = brand.id
            
            status = "✓ Créée" if created else "→ Existe déjà"
            print(f"  {status}: {brand.name}")
            
        except Exception as e:
            print(f"  ✗ Erreur avec marque {marque['nom']}: {e}")
    
    cursor.close()
    conn.close()
    
    print(f"\n✓ {len(brand_mapping)} marques importées")
    return brand_mapping

def import_categories():
    """Importer types → Categories"""
    print("\n📁 IMPORTATION DES CATÉGORIES (types)...")
    print("="*80)
    
    conn = connect_source_db()
    cursor = conn.cursor()
    
    # Récupérer les types
    cursor.execute("""
        SELECT id, nom, description, image, is_show_home, is_active
        FROM types
        WHERE deleted_at IS NULL AND is_active = 1
        ORDER BY id
    """)
    
    types = cursor.fetchall()
    category_mapping = {}
    
    for type_data in types:
        try:
            # Créer la catégorie
            category, created = Category.objects.get_or_create(
                name=type_data['nom'],
                defaults={
                    'description': type_data['description'] or '',
                    'slug': slugify(type_data['nom']),
                    'is_active': bool(type_data['is_active'])
                }
            )
            
            category_mapping[type_data['id']] = category.id
            
            status = "✓ Créée" if created else "→ Existe déjà"
            print(f"  {status}: {category.name}")
            
        except Exception as e:
            print(f"  ✗ Erreur avec type {type_data['nom']}: {e}")
    
    cursor.close()
    conn.close()
    
    print(f"\n✓ {len(category_mapping)} catégories importées")
    return category_mapping

def import_subcategories(category_mapping):
    """Importer categories → SubCategories"""
    print("\n📂 IMPORTATION DES SOUS-CATÉGORIES (categories)...")
    print("="*80)
    
    conn = connect_source_db()
    cursor = conn.cursor()
    
    # Récupérer les catégories (qui deviennent des sous-catégories)
    cursor.execute("""
        SELECT c.id, c.nom, c.description, c.type_id, c.slug, 
               c.image_public, c.is_show_menu, c.is_active
        FROM categories c
        WHERE c.deleted_at IS NULL AND c.is_active = 1
        ORDER BY c.id
    """)
    
    categories = cursor.fetchall()
    subcategory_mapping = {}
    
    for cat_data in categories:
        try:
            # Trouver la catégorie parente
            if cat_data['type_id'] not in category_mapping:
                print(f"  ⚠ Type ID {cat_data['type_id']} non trouvé pour: {cat_data['nom']}")
                continue
            
            category_id = category_mapping[cat_data['type_id']]
            category = Category.objects.get(id=category_id)
            
            # Créer la sous-catégorie
            subcategory, created = SubCategory.objects.get_or_create(
                name=cat_data['nom'],
                category=category,
                defaults={
                    'description': cat_data['description'] or '',
                    'slug': cat_data['slug'] or slugify(cat_data['nom']),
                    'show_on_homepage': bool(cat_data['is_show_menu']),
                    'is_active': bool(cat_data['is_active'])
                }
            )
            
            subcategory_mapping[cat_data['id']] = subcategory.id
            
            status = "✓ Créée" if created else "→ Existe déjà"
            print(f"  {status}: {category.name} → {subcategory.name}")
            
            # Importer les images de la sous-catégorie
            import_subcategory_images(cursor, cat_data['id'], subcategory)
            
        except Exception as e:
            print(f"  ✗ Erreur avec catégorie {cat_data['nom']}: {e}")
    
    cursor.close()
    conn.close()
    
    print(f"\n✓ {len(subcategory_mapping)} sous-catégories importées")
    return subcategory_mapping

def import_subcategory_images(cursor, category_id, subcategory):
    """Importer les images d'une sous-catégorie"""
    cursor.execute("""
        SELECT image_path
        FROM category_images
        WHERE category_id = %s AND deleted_at IS NULL
        LIMIT 1
    """, (category_id,))
    
    images = cursor.fetchall()
    
    if images and images[0]['image_path']:
        # Pour simplifier, on ne garde que la première image
        # Vous pourrez adapter selon vos besoins
        image_path = images[0]['image_path']
        print(f"    → Image: {image_path}")

def import_products(category_mapping, subcategory_mapping, brand_mapping):
    """Importer les produits"""
    print("\n📦 IMPORTATION DES PRODUITS...")
    print("="*80)
    
    conn = connect_source_db()
    cursor = conn.cursor()
    
    # Récupérer tous les produits actifs
    cursor.execute("""
        SELECT DISTINCT p.id, p.nom, p.description, p.prix, p.prix_regulier,
               p.qte, p.image, p.marque_id, p.slug, p.is_active, p.reference_id
        FROM produits p
        WHERE p.deleted_at IS NULL AND p.is_active = 1
        ORDER BY p.id
    """)
    
    produits = cursor.fetchall()
    product_count = 0
    
    for prod in produits:
        try:
            # Récupérer toutes les catégories associées à ce produit
            cursor.execute("""
                SELECT categorie_id
                FROM produit_categories
                WHERE produit_id = %s AND deleted_at IS NULL
                LIMIT 1
            """, (prod['id'],))
            
            prod_categories = cursor.fetchall()
            
            if not prod_categories:
                print(f"  ⚠ Aucune catégorie trouvée pour: {prod['nom']}")
                continue
            
            # Utiliser la première catégorie trouvée
            categorie_id = prod_categories[0]['categorie_id']
            
            if categorie_id not in subcategory_mapping:
                print(f"  ⚠ Sous-catégorie ID {categorie_id} non trouvée pour: {prod['nom']}")
                continue
            
            subcategory_id = subcategory_mapping[categorie_id]
            subcategory = SubCategory.objects.get(id=subcategory_id)
            
            # Trouver la marque si elle existe
            brand = None
            if prod['marque_id'] and prod['marque_id'] in brand_mapping:
                brand = Brand.objects.get(id=brand_mapping[prod['marque_id']])
            
            # Créer le produit
            price = float(prod['prix']) if prod['prix'] else 0
            regular_price = float(prod['prix_regulier']) if prod['prix_regulier'] else price
            
            # Générer une référence unique si manquante
            reference = prod['reference_id'] or f"REF-{prod['id']}"
            
            product, created = Product.objects.get_or_create(
                reference=reference,
                defaults={
                    'name': prod['nom'],
                    'description': prod['description'] or '',
                    'price': str(regular_price),
                    'discount_price': str(price) if price < regular_price else None,
                    'quantity': prod['qte'] or 0,
                    'slug': prod['slug'] or slugify(prod['nom']),
                    'brand': brand,
                    'subcategory': subcategory,
                    'category': subcategory.category,
                    'status': 'in_stock' if prod['qte'] > 0 else 'out_of_stock',
                }
            )
            
            if created:
                product_count += 1
                status = "✓ Créé"
            else:
                status = "→ Existe"
            
            print(f"  {status}: {product.name} ({product.final_price} DH)")
            
        except Exception as e:
            print(f"  ✗ Erreur avec produit {prod['nom']}: {e}")
    
    cursor.close()
    conn.close()
    
    print(f"\n✓ {product_count} produits importés")

def main():
    """Fonction principale d'importation"""
    print("\n" + "="*80)
    print("🚀 IMPORTATION DES DONNÉES SQL VERS DJANGO GOBAG.MA")
    print("="*80)
    print("\nCe script va importer:")
    print("  • Marques → Brand")
    print("  • Types → Category")
    print("  • Categories → SubCategory")
    print("  • Produits → Product")
    print("\n" + "="*80)
    
    try:
        # Étape 1: Importer les marques
        brand_mapping = import_brands()
        
        # Étape 2: Importer les catégories (types)
        category_mapping = import_categories()
        
        # Étape 3: Importer les sous-catégories (categories)
        subcategory_mapping = import_subcategories(category_mapping)
        
        # Étape 4: Importer les produits
        import_products(category_mapping, subcategory_mapping, brand_mapping)
        
        print("\n" + "="*80)
        print("✅ IMPORTATION TERMINÉE AVEC SUCCÈS!")
        print("="*80)
        print("\nRésumé:")
        print(f"  • {len(brand_mapping)} marques")
        print(f"  • {len(category_mapping)} catégories")
        print(f"  • {len(subcategory_mapping)} sous-catégories")
        print("\nVous pouvez maintenant:")
        print("  1. Vérifier les données dans l'admin: http://localhost:8000/admin")
        print("  2. Visualiser le site: http://localhost:3000")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

import os
import sys
import django
import pandas as pd
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Collection, Category, SubCategory, Brand, Product

# Configuration
EXCEL_FILE = r'C:\Users\MSI\Desktop\goback\old_data.xlsx'

def main():
    print("\n" + "=" * 80)
    print("NETTOYAGE DE LA BASE DE DONNÉES")
    print("=" * 80)
    print("\nSupprimer les éléments qui ne sont PAS dans le fichier Excel")
    print("=" * 80 + "\n")
    
    # Lire Excel
    df = pd.read_excel(EXCEL_FILE)
    print(f"[OK] Fichier chargé: {len(df)} lignes\n")
    
    # Colonnes Excel
    COL_1ER_NIVEAU = 0    # Collection
    COL_2EME_NIVEAU = 1   # Category
    COL_CATEGORY = 2      # SubCategory
    COL_MARQUE = 3        # Brand
    
    # Extraire les valeurs uniques du fichier Excel
    excel_collections = set(df.iloc[:, COL_1ER_NIVEAU].dropna().astype(str).str.strip().unique())
    excel_categories = set(df.iloc[:, COL_2EME_NIVEAU].dropna().astype(str).str.strip().unique())
    excel_subcategories = set(df.iloc[:, COL_CATEGORY].dropna().astype(str).str.strip().unique())
    excel_brands = set(df.iloc[:, COL_MARQUE].dropna().astype(str).str.strip().unique())
    
    print("Éléments dans le fichier Excel:")
    print(f"  - Collections: {len(excel_collections)}")
    print(f"  - Catégories: {len(excel_categories)}")
    print(f"  - Sous-catégories: {len(excel_subcategories)}")
    print(f"  - Marques: {len(excel_brands)}")
    print()
    
    stats = {
        'collections_deleted': 0,
        'categories_deleted': 0,
        'subcategories_deleted': 0,
        'brands_deleted': 0,
        'products_deleted': 0
    }
    
    # 1. SUPPRIMER LES COLLECTIONS non présentes dans Excel
    print("\n" + "-" * 80)
    print("1. NETTOYAGE DES COLLECTIONS")
    print("-" * 80)
    
    db_collections = Collection.objects.all()
    print(f"\nCollections dans la BD: {db_collections.count()}")
    
    for collection in db_collections:
        if collection.name not in excel_collections:
            # Compter les produits avant suppression
            products_count = collection.products.count()
            print(f"  [X] Suppression: {collection.name} ({products_count} produits)")
            collection.delete()
            stats['collections_deleted'] += 1
            stats['products_deleted'] += products_count
        else:
            print(f"  [✓] Conservation: {collection.name}")
    
    # 2. SUPPRIMER LES CATÉGORIES non présentes dans Excel
    print("\n" + "-" * 80)
    print("2. NETTOYAGE DES CATÉGORIES")
    print("-" * 80)
    
    db_categories = Category.objects.all()
    print(f"\nCatégories dans la BD: {db_categories.count()}")
    
    for category in db_categories:
        if category.name not in excel_categories:
            # Compter les sous-catégories et produits
            subcats_count = category.subcategories.count()
            products_count = category.products.count()
            print(f"  [X] Suppression: {category.name} ({subcats_count} sous-cat, {products_count} produits)")
            category.delete()
            stats['categories_deleted'] += 1
            stats['products_deleted'] += products_count
        else:
            print(f"  [✓] Conservation: {category.name}")
    
    # 3. SUPPRIMER LES SOUS-CATÉGORIES non présentes dans Excel
    print("\n" + "-" * 80)
    print("3. NETTOYAGE DES SOUS-CATÉGORIES")
    print("-" * 80)
    
    db_subcategories = SubCategory.objects.all()
    print(f"\nSous-catégories dans la BD: {db_subcategories.count()}")
    
    for subcategory in db_subcategories:
        if subcategory.name not in excel_subcategories:
            products_count = subcategory.products.count()
            print(f"  [X] Suppression: {subcategory.name} ({products_count} produits)")
            subcategory.delete()
            stats['subcategories_deleted'] += 1
            stats['products_deleted'] += products_count
        else:
            print(f"  [✓] Conservation: {subcategory.name}")
    
    # 4. SUPPRIMER LES MARQUES non présentes dans Excel
    print("\n" + "-" * 80)
    print("4. NETTOYAGE DES MARQUES")
    print("-" * 80)
    
    db_brands = Brand.objects.all()
    print(f"\nMarques dans la BD: {db_brands.count()}")
    
    for brand in db_brands:
        if brand.name not in excel_brands:
            products_count = brand.products.count()
            print(f"  [X] Suppression: {brand.name} ({products_count} produits)")
            brand.delete()
            stats['brands_deleted'] += 1
            stats['products_deleted'] += products_count
        else:
            print(f"  [✓] Conservation: {brand.name}")
    
    # 5. SUPPRIMER LES PRODUITS ORPHELINS (sans catégorie ou sous-catégorie)
    print("\n" + "-" * 80)
    print("5. NETTOYAGE DES PRODUITS ORPHELINS")
    print("-" * 80)
    
    orphan_products = Product.objects.filter(category__isnull=True) | Product.objects.filter(subcategory__isnull=True)
    orphan_count = orphan_products.count()
    
    if orphan_count > 0:
        print(f"\n[X] Suppression de {orphan_count} produits orphelins...")
        orphan_products.delete()
        stats['products_deleted'] += orphan_count
    else:
        print("\n[✓] Aucun produit orphelin trouvé")
    
    # RÉSUMÉ
    print("\n" + "=" * 80)
    print("RÉSUMÉ DU NETTOYAGE")
    print("=" * 80)
    print(f"[X] Collections supprimées      : {stats['collections_deleted']}")
    print(f"[X] Catégories supprimées       : {stats['categories_deleted']}")
    print(f"[X] Sous-catégories supprimées  : {stats['subcategories_deleted']}")
    print(f"[X] Marques supprimées          : {stats['brands_deleted']}")
    print(f"[X] Total produits supprimés    : {stats['products_deleted']}")
    print("\n" + "=" * 80)
    print("État final de la base de données:")
    print("=" * 80)
    print(f"[✓] Collections restantes       : {Collection.objects.count()}")
    print(f"[✓] Catégories restantes        : {Category.objects.count()}")
    print(f"[✓] Sous-catégories restantes   : {SubCategory.objects.count()}")
    print(f"[✓] Marques restantes           : {Brand.objects.count()}")
    print(f"[✓] Produits restants           : {Product.objects.count()}")
    print("=" * 80)
    
    # Confirmation
    print("\n✓ Nettoyage terminé avec succès!")
    print("\nVous pouvez maintenant exécuter 'import_final_structure.py' pour réimporter les données.")

if __name__ == '__main__':
    response = input("\n⚠️  ATTENTION: Cette action va supprimer des données de la base!\nTaper 'OUI' pour confirmer: ")
    if response.upper() == 'OUI':
        main()
    else:
        print("\n[!] Opération annulée.")

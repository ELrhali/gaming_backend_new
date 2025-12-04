"""
Script de test pour l'importation Excel
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admin_panel.excel_import import ExcelImporter
from shop.models import Product, Brand, Type, Category, SubCategory

# Chemin vers le fichier Excel de test
EXCEL_FILE = r"C:\Users\MSI\Desktop\amr\e-commece\public\data_product.xlsx"

def test_import():
    print("=" * 80)
    print("TEST D'IMPORTATION EXCEL")
    print("=" * 80)
    
    # Statistiques avant importation
    print("\n📊 STATISTIQUES AVANT IMPORTATION:")
    print(f"   Produits: {Product.objects.count()}")
    print(f"   Marques: {Brand.objects.count()}")
    print(f"   Types: {Type.objects.count()}")
    print(f"   Catégories: {Category.objects.count()}")
    print(f"   Sous-catégories: {SubCategory.objects.count()}")
    
    # Vérifier que le fichier existe
    if not os.path.exists(EXCEL_FILE):
        print(f"\n❌ ERREUR: Fichier non trouvé: {EXCEL_FILE}")
        return
    
    print(f"\n📂 Fichier Excel: {EXCEL_FILE}")
    print(f"   Taille: {os.path.getsize(EXCEL_FILE) / 1024:.2f} KB")
    
    # Importer
    print("\n🚀 LANCEMENT DE L'IMPORTATION...")
    print("-" * 80)
    
    importer = ExcelImporter()
    result = importer.import_from_excel(EXCEL_FILE)
    
    print("-" * 80)
    
    # Résultats
    if result['success']:
        print("\n✅ IMPORTATION RÉUSSIE!")
        print(f"\n📈 RÉSULTATS:")
        print(f"   ✓ Produits créés: {result['created']}")
        print(f"   ⊘ Produits ignorés: {result['skipped']}")
        
        if result['created_brands']:
            print(f"\n🏷️  NOUVELLES MARQUES CRÉÉES ({len(result['created_brands'])}):")
            for brand in result['created_brands'][:10]:
                print(f"   • {brand}")
            if len(result['created_brands']) > 10:
                print(f"   ... et {len(result['created_brands']) - 10} autres")
        
        if result['created_types']:
            print(f"\n🔧 NOUVEAUX TYPES CRÉÉS ({len(result['created_types'])}):")
            for type_name in result['created_types'][:10]:
                print(f"   • {type_name}")
            if len(result['created_types']) > 10:
                print(f"   ... et {len(result['created_types']) - 10} autres")
        
        if result['created_collections']:
            print(f"\n📦 NOUVELLES COLLECTIONS CRÉÉES ({len(result['created_collections'])}):")
            for collection in result['created_collections']:
                print(f"   • {collection}")
        
        if result['errors']:
            print(f"\n⚠️  ERREURS RENCONTRÉES ({len(result['errors'])}):")
            for error in result['errors'][:10]:
                print(f"   • {error}")
            if len(result['errors']) > 10:
                print(f"   ... et {len(result['errors']) - 10} autres erreurs")
    else:
        print(f"\n❌ ERREUR D'IMPORTATION:")
        print(f"   {result['error']}")
    
    # Statistiques après importation
    print("\n📊 STATISTIQUES APRÈS IMPORTATION:")
    print(f"   Produits: {Product.objects.count()}")
    print(f"   Marques: {Brand.objects.count()}")
    print(f"   Types: {Type.objects.count()}")
    print(f"   Catégories: {Category.objects.count()}")
    print(f"   Sous-catégories: {SubCategory.objects.count()}")
    
    # Quelques exemples de produits créés
    if result['success'] and result['created'] > 0:
        print("\n📦 EXEMPLES DE PRODUITS CRÉÉS:")
        recent_products = Product.objects.order_by('-created_at')[:5]
        for product in recent_products:
            print(f"\n   📌 {product.reference} - {product.name}")
            print(f"      Catégorie: {product.category.name} > {product.subcategory.name}")
            if product.brand_id:
                print(f"      Marque: {product.brand.name}")
            if product.type_id:
                print(f"      Type: {product.type.name}")
            print(f"      Prix: {product.price} DH")
            print(f"      Stock: {product.quantity}")
            
            specs = product.specifications.all()
            if specs:
                print(f"      Caractéristiques: {specs.count()}")
                for spec in specs[:3]:
                    print(f"         • {spec.key}: {spec.value}")
    
    print("\n" + "=" * 80)
    print("TEST TERMINÉ")
    print("=" * 80)

if __name__ == '__main__':
    test_import()

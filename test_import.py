"""
Script de test pour l'importation Excel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admin_panel.excel_import import ExcelImporter

# Chemin du fichier
file_path = r"C:\Users\MSI\Desktop\goback\data_product.xlsx"

print("=" * 80)
print("TEST D'IMPORTATION EXCEL")
print("=" * 80)
print(f"📁 Fichier: {file_path}")
print()

# Créer l'importeur
importer = ExcelImporter()

# Importer
result = importer.import_from_excel(file_path)

print("\n" + "=" * 80)
print("RÉSULTATS")
print("=" * 80)

if result['success']:
    print(f"✅ Importation réussie!")
    print(f"   • {result['created']} produits créés")
    print(f"   • {result['skipped']} produits ignorés")
    
    if result['created_brands']:
        print(f"\n📦 Marques créées ({len(result['created_brands'])}):")
        for brand in result['created_brands']:
            print(f"   • {brand}")
    
    if result['created_types']:
        print(f"\n🏷️  Types créés ({len(result['created_types'])}):")
        for type_name in result['created_types']:
            print(f"   • {type_name}")
    
    if result['created_collections']:
        print(f"\n📚 Collections créées ({len(result['created_collections'])}):")
        for collection in result['created_collections']:
            print(f"   • {collection}")
    
    if result['errors']:
        print(f"\n⚠️  Erreurs ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"   • {error}")
else:
    print(f"❌ Erreur: {result.get('error')}")

print("\n" + "=" * 80)

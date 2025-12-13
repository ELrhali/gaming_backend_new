"""
Script pour vider la base de données (garder les utilisateurs)
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import (
    Category, SubCategory, Type, Brand, Product, 
    ProductImage, ProductSpecification, Collection, HeroSlide
)

def clean_database():
    """Supprime toutes les données sauf les utilisateurs"""
    
    print("🗑️  Nettoyage de la base de données...\n")
    
    # Compter avant suppression
    counts_before = {
        'ProductImage': ProductImage.objects.count(),
        'ProductSpecification': ProductSpecification.objects.count(),
        'Product': Product.objects.count(),
        'Type': Type.objects.count(),
        'SubCategory': SubCategory.objects.count(),
        'Category': Category.objects.count(),
        'Brand': Brand.objects.count(),
        'Collection': Collection.objects.count(),
        'HeroSlide': HeroSlide.objects.count(),
    }
    
    print("📊 État avant nettoyage:")
    for model, count in counts_before.items():
        print(f"  - {model}: {count}")
    
    # Supprimer dans le bon ordre (dépendances)
    print("\n🔄 Suppression en cours...")
    
    ProductImage.objects.all().delete()
    print("  ✅ Images produits supprimées")
    
    ProductSpecification.objects.all().delete()
    print("  ✅ Spécifications produits supprimées")
    
    Product.objects.all().delete()
    print("  ✅ Produits supprimés")
    
    Type.objects.all().delete()
    print("  ✅ Types supprimés")
    
    SubCategory.objects.all().delete()
    print("  ✅ Sous-catégories supprimées")
    
    Category.objects.all().delete()
    print("  ✅ Catégories supprimées")
    
    Brand.objects.all().delete()
    print("  ✅ Marques supprimées")
    
    Collection.objects.all().delete()
    print("  ✅ Collections supprimées")
    
    HeroSlide.objects.all().delete()
    print("  ✅ Slides hero supprimés")
    
    print("\n✅ Base de données nettoyée!")
    print("👤 Les utilisateurs ont été conservés")

if __name__ == '__main__':
    response = input("⚠️  Voulez-vous vraiment vider la base de données? (oui/non): ")
    if response.lower() in ['oui', 'yes', 'o', 'y']:
        clean_database()
    else:
        print("❌ Opération annulée")

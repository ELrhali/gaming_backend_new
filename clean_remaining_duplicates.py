"""
Script pour nettoyer les doublons restants manuellement
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import SubCategory, Type, Product
from collections import defaultdict

def clean_remaining_duplicates():
    """Nettoie les doublons restants dans les sous-catégories"""
    print("🧹 NETTOYAGE DES DOUBLONS RESTANTS\n")
    
    # Grouper les sous-catégories par nom normalisé et catégorie
    subcats_dict = defaultdict(list)
    for subcat in SubCategory.objects.all():
        key = (subcat.name.upper().strip(), subcat.category_id)
        subcats_dict[key].append(subcat)
    
    deleted_count = 0
    
    # Traiter chaque groupe de doublons
    for (name, cat_id), subcats in subcats_dict.items():
        if len(subcats) <= 1:
            continue
        
        # Trier par nombre de produits et types
        subcats_sorted = sorted(
            subcats,
            key=lambda s: (
                Product.objects.filter(subcategory=s).count(),
                Type.objects.filter(subcategory=s).count(),
                bool(s.image)
            ),
            reverse=True
        )
        
        main_subcat = subcats_sorted[0]
        print(f"\n📦 Sous-catégorie: {main_subcat.name} (ID: {main_subcat.id})")
        print(f"   Catégorie: {main_subcat.category.name}")
        print(f"   ✅ Garder: {main_subcat.name} (ID: {main_subcat.id})")
        
        for duplicate in subcats_sorted[1:]:
            print(f"   🗑️  Supprimer: {duplicate.name} (ID: {duplicate.id})")
            
            # Transférer les types
            types = Type.objects.filter(subcategory=duplicate)
            if types.count() > 0:
                types.update(subcategory=main_subcat)
                print(f"      ✅ {types.count()} types transférés")
            
            # Transférer les produits
            products = Product.objects.filter(subcategory=duplicate)
            if products.count() > 0:
                products.update(subcategory=main_subcat)
                print(f"      ✅ {products.count()} produits transférés")
            
            # Transférer l'image si nécessaire
            if duplicate.image and not main_subcat.image:
                main_subcat.image = duplicate.image
                main_subcat.save()
                print(f"      ✅ Image transférée")
            
            # Supprimer le doublon
            duplicate.delete()
            deleted_count += 1
            print(f"      ✅ Doublon supprimé")
    
    print(f"\n📊 Total: {deleted_count} doublons supprimés")
    
    # Afficher l'état final
    print("\n" + "="*60)
    print("✅ NETTOYAGE FINAL TERMINÉ")
    print("="*60)
    print(f"Sous-catégories: {SubCategory.objects.count()}")
    print("="*60)

if __name__ == '__main__':
    clean_remaining_duplicates()

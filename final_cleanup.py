"""
Script final pour supprimer TOUS les doublons restants
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import SubCategory, Type, Product

# Mapping final de toutes les sous-catégories à fusionner
FINAL_MAPPING = {
    # Format: (ancien_nom, nouvelle_nom, catégorie)
    # Composants
    ('PROCESSEUR', 'Processeurs', 'Composants'),
    ('MEMOIRE RAM', 'Mémoire RAM', 'Composants'),
    ('REFROIDISSEMENT', 'Refroidissement', 'Composants'),
    ('STOCKAGE', 'Stockage', 'Composants'),
    ('Boîtiers', 'Boîtiers PC', 'Composants'),
    ('souris', 'Souris Gaming', 'Composants'),  # Déplacer vers Périphériques
    
    # Périphériques
    ('SOURIS', 'Souris Gaming', 'Périphériques'),
    ('Claviers', 'Claviers Gaming', 'Périphériques'),
    ('Casques', 'Casques Audio', 'Périphériques'),
}

def clean_all_duplicates():
    print("🧹 NETTOYAGE FINAL DE TOUS LES DOUBLONS\n")
    print("="*60)
    
    deleted_count = 0
    
    # 1. Traiter les doublons via le mapping
    for old_name, new_name, cat_name in FINAL_MAPPING:
        try:
            from shop.models import Category
            category = Category.objects.get(name=cat_name)
            
            # Trouver l'ancienne sous-catégorie
            old_subcat = SubCategory.objects.filter(
                name=old_name,
                category=category
            ).first()
            
            if not old_subcat:
                continue
            
            # Trouver ou créer la nouvelle sous-catégorie
            from django.utils.text import slugify
            new_subcat, created = SubCategory.objects.get_or_create(
                name=new_name,
                category=category,
                defaults={
                    'slug': slugify(f"{category.slug}-{new_name}"),
                    'description': f'Découvrez nos {new_name.lower()}',
                    'order': 0,
                    'is_active': True,
                }
            )
            
            if old_subcat.id == new_subcat.id:
                continue
            
            print(f"\n📦 [{cat_name}] '{old_name}' -> '{new_name}'")
            
            # Transférer types
            types = Type.objects.filter(subcategory=old_subcat)
            if types.count() > 0:
                types.update(subcategory=new_subcat)
                print(f"   ✅ {types.count()} types transférés")
            
            # Transférer produits
            products = Product.objects.filter(subcategory=old_subcat)
            if products.count() > 0:
                products.update(subcategory=new_subcat)
                print(f"   ✅ {products.count()} produits transférés")
            
            # Transférer image
            if old_subcat.image and not new_subcat.image:
                new_subcat.image = old_subcat.image
                new_subcat.save()
                print(f"   ✅ Image transférée")
            
            # Supprimer
            old_subcat.delete()
            deleted_count += 1
            print(f"   🗑️  Supprimé")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    # 2. Nettoyer les doublons par nom identique (case-insensitive)
    from collections import defaultdict
    
    subcats_dict = defaultdict(list)
    for subcat in SubCategory.objects.all():
        key = (subcat.name.upper().strip(), subcat.category_id)
        subcats_dict[key].append(subcat)
    
    for (name, cat_id), subcats in subcats_dict.items():
        if len(subcats) <= 1:
            continue
        
        # Garder celle avec le plus de contenu
        main = sorted(
            subcats,
            key=lambda s: (
                Product.objects.filter(subcategory=s).count(),
                Type.objects.filter(subcategory=s).count(),
                bool(s.image)
            ),
            reverse=True
        )[0]
        
        print(f"\n📦 Fusion de doublons: {main.name}")
        
        for dup in subcats:
            if dup.id == main.id:
                continue
            
            Type.objects.filter(subcategory=dup).update(subcategory=main)
            Product.objects.filter(subcategory=dup).update(subcategory=main)
            
            if dup.image and not main.image:
                main.image = dup.image
                main.save()
            
            dup.delete()
            deleted_count += 1
            print(f"   🗑️  Supprimé doublon (ID: {dup.id})")
    
    # 3. Déplacer "souris" de Composants vers Périphériques
    try:
        from shop.models import Category
        composants = Category.objects.get(name='Composants')
        peripheriques = Category.objects.get(name='Périphériques')
        
        souris_composants = SubCategory.objects.filter(
            name__iexact='souris',
            category=composants
        ).first()
        
        if souris_composants:
            souris_gaming = SubCategory.objects.filter(
                name='Souris Gaming',
                category=peripheriques
            ).first()
            
            if souris_gaming:
                print(f"\n📦 Déplacement: souris (Composants) -> Souris Gaming (Périphériques)")
                
                # Transférer tout
                Type.objects.filter(subcategory=souris_composants).update(subcategory=souris_gaming)
                Product.objects.filter(subcategory=souris_composants).update(subcategory=souris_gaming)
                
                if souris_composants.image and not souris_gaming.image:
                    souris_gaming.image = souris_composants.image
                    souris_gaming.save()
                
                souris_composants.delete()
                deleted_count += 1
                print(f"   ✅ Déplacé et fusionné")
    except Exception as e:
        print(f"   ❌ Erreur déplacement souris: {e}")
    
    print("\n" + "="*60)
    print(f"✅ NETTOYAGE TERMINÉ - {deleted_count} éléments supprimés")
    print("="*60)
    
    # État final
    from shop.models import Category
    print("\n📊 ÉTAT FINAL:\n")
    for cat in Category.objects.all().order_by('name'):
        subcats = SubCategory.objects.filter(category=cat).order_by('name')
        print(f"\n   📁 {cat.name} ({subcats.count()} sous-catégories):")
        for s in subcats:
            print(f"      - {s.name}")

if __name__ == '__main__':
    clean_all_duplicates()

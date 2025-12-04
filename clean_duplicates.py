"""
Script pour supprimer les doublons dans les catégories, sous-catégories, marques et types
en ignorant les différences de casse et les variations de noms similaires
"""
import os
import sys
import django
from django.db.models import Count

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Brand, Type, Product
from django.utils.text import slugify

def normalize_name(name):
    """Normalise un nom pour la comparaison (minuscules, sans espaces multiples)"""
    return name.strip().upper().replace('  ', ' ')

def merge_categories():
    """Fusionne les catégories en double"""
    print("\n=== NETTOYAGE DES CATEGORIES ===")
    
    # Mapping des catégories similaires
    category_mapping = {
        'COMPOSANT PC': 'Composants',
        'COMPOSANTS': 'Composants',
        'PÉRIPHÉRIQUES PC': 'Périphériques',
        'PERIPHERIQUES PC': 'Périphériques',
        'PÉRIPHÉRIQUES': 'Périphériques',
        'PERIPHERIQUES': 'Périphériques',
        'ACCESSOIRES PC': 'Accessoires',
        'ACCESSOIRES': 'Accessoires',
    }
    
    deleted_count = 0
    updated_products = 0
    
    for old_name, new_name in category_mapping.items():
        try:
            # Trouver la catégorie source (à supprimer)
            old_category = Category.objects.filter(name__iexact=old_name).first()
            if not old_category:
                continue
            
            # Trouver ou créer la catégorie cible (à garder)
            new_category, created = Category.objects.get_or_create(
                name=new_name,
                defaults={
                    'slug': slugify(new_name),
                    'description': f'Découvrez notre gamme de {new_name.lower()}',
                    'order': 1,
                    'is_active': True,
                }
            )
            
            if old_category.id == new_category.id:
                continue
            
            print(f"\n📦 Fusion: '{old_category.name}' -> '{new_category.name}'")
            
            # Transférer toutes les sous-catégories
            subcats = SubCategory.objects.filter(category=old_category)
            subcat_count = subcats.count()
            if subcat_count > 0:
                subcats.update(category=new_category)
                print(f"  ✅ {subcat_count} sous-catégories transférées")
            
            # Transférer tous les produits
            products = Product.objects.filter(category=old_category)
            product_count = products.count()
            if product_count > 0:
                products.update(category=new_category)
                updated_products += product_count
                print(f"  ✅ {product_count} produits transférés")
            
            # Transférer l'image si la nouvelle catégorie n'en a pas
            if old_category.image and not new_category.image:
                new_category.image = old_category.image
                new_category.save()
                print(f"  ✅ Image transférée")
            
            # Supprimer l'ancienne catégorie
            old_category.delete()
            deleted_count += 1
            print(f"  🗑️  Catégorie '{old_name}' supprimée")
            
        except Exception as e:
            print(f"  ❌ Erreur lors de la fusion de '{old_name}': {e}")
    
    print(f"\n📊 Résumé: {deleted_count} catégories en double supprimées")
    return deleted_count

def merge_subcategories():
    """Fusionne les sous-catégories en double"""
    print("\n=== NETTOYAGE DES SOUS-CATEGORIES ===")
    
    # Mapping des sous-catégories similaires
    subcategory_mapping = {
        'PROCESSEUR': 'Processeurs',
        'PROCESSEURS': 'Processeurs',
        'ÉCRAN PC': 'Écrans',
        'ECRAN PC': 'Écrans',
        'ÉCRANS PC': 'Écrans',
        'ECRANS PC': 'Écrans',
        'ECRAN': 'Écrans',
        'ÉCRAN': 'Écrans',
        'SOURIS': 'Souris',
        'CARTE GRAPHIQUE': 'Cartes Graphiques',
        'CARTES GRAPHIQUES': 'Cartes Graphiques',
        'CARTE MERE': 'Cartes Mères',
        'CARTES MÈRES': 'Cartes Mères',
        'CARTES MERES': 'Cartes Mères',
        'MEMOIRE RAM': 'Mémoire RAM',
        'MÉMOIRE RAM': 'Mémoire RAM',
        'CLAVIER': 'Claviers',
        'CLAVIERS': 'Claviers',
        'CASQUE': 'Casques',
        'CASQUES': 'Casques',
        'AURICULAR': 'Casques',
        'REFROIDISSEMENT': 'Refroidissement',
        'STOCKAGE': 'Stockage',
        'ALIMENTATION': 'Alimentations',
        'ALIMENTATIONS': 'Alimentations',
        'BOITIER': 'Boîtiers',
        'BOÎTIER': 'Boîtiers',
        'BOITIERS': 'Boîtiers',
        'BOÎTIERS': 'Boîtiers',
        'VENTILATEUR': 'Ventilateurs',
        'VENTILATEURS': 'Ventilateurs',
        'WEBCAM': 'Webcams',
        'WEBCAMS': 'Webcams',
        'MICROPHONE': 'Microphones',
        'MICROPHONES': 'Microphones',
        'TAPIS': 'Tapis de Souris',
        'TAPIS DE SOURIS': 'Tapis de Souris',
        'JOYSTICK': 'Joysticks',
        'JOYSTICKS': 'Joysticks',
        'STREAMING': 'Streaming',
        'PATE THERMIQUE': 'Pâte Thermique',
        'PÂTE THERMIQUE': 'Pâte Thermique',
        'MODDING': 'Modding',
    }
    
    deleted_count = 0
    updated_products = 0
    
    # Grouper par catégorie parent pour éviter les conflits
    for category in Category.objects.all():
        print(f"\n📁 Traitement de la catégorie: {category.name}")
        
        for old_name, new_name in subcategory_mapping.items():
            try:
                # Trouver la sous-catégorie source
                old_subcat = SubCategory.objects.filter(
                    name__iexact=old_name,
                    category=category
                ).first()
                
                if not old_subcat:
                    continue
                
                # Trouver ou créer la sous-catégorie cible
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
                
                print(f"  📦 Fusion: '{old_subcat.name}' -> '{new_subcat.name}'")
                
                # Transférer tous les types
                types = Type.objects.filter(subcategory=old_subcat)
                type_count = types.count()
                if type_count > 0:
                    types.update(subcategory=new_subcat)
                    print(f"    ✅ {type_count} types transférés")
                
                # Transférer tous les produits
                products = Product.objects.filter(subcategory=old_subcat)
                product_count = products.count()
                if product_count > 0:
                    products.update(subcategory=new_subcat)
                    updated_products += product_count
                    print(f"    ✅ {product_count} produits transférés")
                
                # Transférer l'image si la nouvelle sous-catégorie n'en a pas
                if old_subcat.image and not new_subcat.image:
                    new_subcat.image = old_subcat.image
                    new_subcat.save()
                    print(f"    ✅ Image transférée")
                
                # Supprimer l'ancienne sous-catégorie
                old_subcat.delete()
                deleted_count += 1
                print(f"    🗑️  Sous-catégorie '{old_name}' supprimée")
                
            except Exception as e:
                print(f"    ❌ Erreur lors de la fusion de '{old_name}': {e}")
    
    print(f"\n📊 Résumé: {deleted_count} sous-catégories en double supprimées")
    return deleted_count

def merge_brands():
    """Fusionne les marques en double (insensible à la casse)"""
    print("\n=== NETTOYAGE DES MARQUES ===")
    
    deleted_count = 0
    
    # Grouper les marques par nom normalisé
    brands_dict = {}
    for brand in Brand.objects.all():
        normalized = normalize_name(brand.name)
        if normalized not in brands_dict:
            brands_dict[normalized] = []
        brands_dict[normalized].append(brand)
    
    # Fusionner les doublons
    for normalized, brands in brands_dict.items():
        if len(brands) <= 1:
            continue
        
        # Garder la première marque (ou celle avec le plus de produits)
        brands_sorted = sorted(brands, key=lambda b: Product.objects.filter(brand=b).count(), reverse=True)
        main_brand = brands_sorted[0]
        
        print(f"\n🏷️  Fusion des marques '{normalized}':")
        print(f"  ✅ Marque principale: {main_brand.name}")
        
        for duplicate_brand in brands_sorted[1:]:
            print(f"  📦 Fusion: '{duplicate_brand.name}' -> '{main_brand.name}'")
            
            # Transférer tous les types
            types = Type.objects.filter(brand=duplicate_brand)
            type_count = types.count()
            if type_count > 0:
                types.update(brand=main_brand)
                print(f"    ✅ {type_count} types transférés")
            
            # Transférer tous les produits
            products = Product.objects.filter(brand=duplicate_brand)
            product_count = products.count()
            if product_count > 0:
                products.update(brand=main_brand)
                print(f"    ✅ {product_count} produits transférés")
            
            # Transférer le logo si la marque principale n'en a pas
            if duplicate_brand.logo and not main_brand.logo:
                main_brand.logo = duplicate_brand.logo
                main_brand.save()
                print(f"    ✅ Logo transféré")
            
            # Supprimer la marque en double
            duplicate_brand.delete()
            deleted_count += 1
            print(f"    🗑️  Marque '{duplicate_brand.name}' supprimée")
    
    print(f"\n📊 Résumé: {deleted_count} marques en double supprimées")
    return deleted_count

def merge_types():
    """Fusionne les types en double"""
    print("\n=== NETTOYAGE DES TYPES ===")
    
    deleted_count = 0
    
    # Grouper par sous-catégorie et marque
    for subcategory in SubCategory.objects.all():
        types_dict = {}
        
        for type_obj in Type.objects.filter(subcategory=subcategory):
            key = (normalize_name(type_obj.name), type_obj.brand_id if type_obj.brand else None)
            if key not in types_dict:
                types_dict[key] = []
            types_dict[key].append(type_obj)
        
        # Fusionner les doublons
        for key, types in types_dict.items():
            if len(types) <= 1:
                continue
            
            main_type = types[0]
            print(f"\n🔧 Fusion des types '{main_type.name}' dans '{subcategory.name}':")
            
            for duplicate_type in types[1:]:
                # Transférer tous les produits
                products = Product.objects.filter(type=duplicate_type)
                product_count = products.count()
                if product_count > 0:
                    products.update(type=main_type)
                    print(f"  ✅ {product_count} produits transférés de '{duplicate_type.name}'")
                
                # Supprimer le type en double
                duplicate_type.delete()
                deleted_count += 1
    
    print(f"\n📊 Résumé: {deleted_count} types en double supprimés")
    return deleted_count

def main():
    print("🧹 NETTOYAGE DES DOUBLONS")
    print("="*60)
    
    # Afficher l'état actuel
    print("\n📊 ÉTAT AVANT NETTOYAGE:")
    print(f"Catégories: {Category.objects.count()}")
    print(f"Sous-catégories: {SubCategory.objects.count()}")
    print(f"Marques: {Brand.objects.count()}")
    print(f"Types: {Type.objects.count()}")
    
    # Nettoyer dans l'ordre
    cat_deleted = merge_categories()
    subcat_deleted = merge_subcategories()
    brand_deleted = merge_brands()
    type_deleted = merge_types()
    
    # Afficher l'état final
    print("\n" + "="*60)
    print("✅ NETTOYAGE TERMINÉ")
    print("="*60)
    print(f"\n📊 ÉTAT APRÈS NETTOYAGE:")
    print(f"Catégories: {Category.objects.count()} (supprimées: {cat_deleted})")
    print(f"Sous-catégories: {SubCategory.objects.count()} (supprimées: {subcat_deleted})")
    print(f"Marques: {Brand.objects.count()} (supprimées: {brand_deleted})")
    print(f"Types: {Type.objects.count()} (supprimés: {type_deleted})")
    print("="*60)

if __name__ == '__main__':
    main()

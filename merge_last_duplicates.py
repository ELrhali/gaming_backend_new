"""
Script pour supprimer les derniers doublons
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import SubCategory, Product, Type, Category

# Fusionner MEMOIRE RAM / Mémoire RAM
print("🧹 Fusion des derniers doublons\n")

try:
    composants = Category.objects.get(name='Composants')
    
    # Trouver toutes les variantes de "Mémoire RAM"
    memoires = SubCategory.objects.filter(
        name__iregex=r'^M[ÉE]MOIRE RAM$',
        category=composants
    )
    
    print(f"Trouvé {memoires.count()} sous-catégories 'Mémoire RAM':")
    for m in memoires:
        print(f"  - ID {m.id}: {m.name} - Produits: {Product.objects.filter(subcategory=m).count()}, Types: {Type.objects.filter(subcategory=m).count()}, Image: {bool(m.image)}")
    
    if memoires.count() > 1:
        # Garder celle avec le plus de contenu
        main = sorted(
            memoires,
            key=lambda s: (
                Product.objects.filter(subcategory=s).count(),
                Type.objects.filter(subcategory=s).count(),
                bool(s.image)
            ),
            reverse=True
        )[0]
        
        print(f"\n✅ Garder: {main.name} (ID {main.id})")
        
        for dup in memoires:
            if dup.id == main.id:
                continue
            
            print(f"\n🔄 Fusion: {dup.name} (ID {dup.id}) -> {main.name} (ID {main.id})")
            
            # Transférer
            types = Type.objects.filter(subcategory=dup)
            products = Product.objects.filter(subcategory=dup)
            
            if types.count() > 0:
                types.update(subcategory=main)
                print(f"   ✅ {types.count()} types transférés")
            
            if products.count() > 0:
                products.update(subcategory=main)
                print(f"   ✅ {products.count()} produits transférés")
            
            if dup.image and not main.image:
                main.image = dup.image
                main.save()
                print(f"   ✅ Image transférée")
            
            dup.delete()
            print(f"   🗑️  Supprimé")
        
        # Normaliser le nom
        if main.name != "Mémoire RAM":
            main.name = "Mémoire RAM"
            main.save()
            print(f"\n✅ Nom normalisé en 'Mémoire RAM'")

except Exception as e:
    print(f"❌ Erreur: {e}")

# Autres doublons similaires
OTHER_DUPLICATES = [
    ('REFROIDISSEMENT', 'Refroidissement', 'Composants'),
    ('STOCKAGE', 'Stockage', 'Composants'),
    ('Souris Gaming', 'Souris Gaming', 'Périphériques'),  # Il peut y en avoir 2
    ('STREAMING', 'Streaming', 'Périphériques'),
]

for old_name, new_name, cat_name in OTHER_DUPLICATES:
    try:
        category = Category.objects.get(name=cat_name)
        subcats = SubCategory.objects.filter(
            name__iexact=old_name,
            category=category
        )
        
        if subcats.count() > 1:
            main = subcats.first()
            print(f"\n🔄 Fusion: {old_name} dans {cat_name}")
            
            for dup in subcats[1:]:
                Type.objects.filter(subcategory=dup).update(subcategory=main)
                Product.objects.filter(subcategory=dup).update(subcategory=main)
                
                if dup.image and not main.image:
                    main.image = dup.image
                    main.save()
                
                dup.delete()
                print(f"   🗑️  Doublon supprimé (ID: {dup.id})")
            
            # Normaliser le nom
            if main.name != new_name:
                main.name = new_name
                main.save()
    except Exception as e:
        print(f"❌ Erreur pour {old_name}: {e}")

print("\n" + "="*60)
print("✅ FUSION TERMINÉE")
print("="*60)

# Afficher l'état final propre
print("\n📊 ÉTAT FINAL:")
for cat in Category.objects.all().order_by('name'):
    subcats = SubCategory.objects.filter(category=cat).order_by('name')
    print(f"\n   📁 {cat.name} ({subcats.count()} sous-catégories):")
    for s in subcats:
        img = "✅" if s.image else "❌"
        print(f"      - {s.name} (Image: {img})")

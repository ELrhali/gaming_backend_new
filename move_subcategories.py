"""
Script pour déplacer Souris Gaming et Refroidissement vers les bonnes catégories
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import SubCategory, Product, Type, Category, Brand

print("🔄 Déplacement des sous-catégories mal placées\n")

# 1. Déplacer Souris Gaming de Composants vers Périphériques
try:
    comp = Category.objects.get(name='Composants')
    peri = Category.objects.get(name='Périphériques')
    accessoires = Category.objects.get(name='Accessoires')
    
    souris_comp = SubCategory.objects.filter(name='Souris Gaming', category=comp).first()
    souris_peri = SubCategory.objects.filter(name='Souris Gaming', category=peri).first()
    
    if souris_comp and souris_peri:
        print(f"🐭 Fusion: Souris Gaming (Composants) -> Souris Gaming (Périphériques)")
        print(f"   Composants ID: {souris_comp.id}")
        print(f"   Périphériques ID: {souris_peri.id}")
        
        # Transférer
        types_count = Type.objects.filter(subcategory=souris_comp).count()
        products_count = Product.objects.filter(subcategory=souris_comp).count()
        
        Type.objects.filter(subcategory=souris_comp).update(subcategory=souris_peri)
        Product.objects.filter(subcategory=souris_comp).update(subcategory=souris_peri)
        
        if souris_comp.image and not souris_peri.image:
            souris_peri.image = souris_comp.image
            souris_peri.save()
        
        souris_comp.delete()
        print(f"   ✅ {types_count} types et {products_count} produits transférés")
        print(f"   🗑️  Doublon supprimé")
    
    # 2. Déplacer Refroidissement de Accessoires vers Composants
    refroid_accessoires = SubCategory.objects.filter(name='Refroidissement', category=accessoires).first()
    refroid_composants = SubCategory.objects.filter(name='Refroidissement', category=comp).first()
    
    if refroid_accessoires and refroid_composants:
        print(f"\n❄️  Fusion: Refroidissement (Accessoires) -> Refroidissement (Composants)")
        
        # Transférer
        types_count = Type.objects.filter(subcategory=refroid_accessoires).count()
        products_count = Product.objects.filter(subcategory=refroid_accessoires).count()
        
        Type.objects.filter(subcategory=refroid_accessoires).update(subcategory=refroid_composants)
        Product.objects.filter(subcategory=refroid_accessoires).update(subcategory=refroid_composants)
        
        if refroid_accessoires.image and not refroid_composants.image:
            refroid_composants.image = refroid_accessoires.image
            refroid_composants.save()
        
        refroid_accessoires.delete()
        print(f"   ✅ {types_count} types et {products_count} produits transférés")
        print(f"   🗑️  Doublon supprimé")

except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*60)
print("✅ DÉPLACEMENTS TERMINÉS")
print("="*60)

# Afficher l'état final
print("\n📊 ÉTAT FINAL:")
for cat in Category.objects.all().order_by('name'):
    subcats = SubCategory.objects.filter(category=cat).order_by('name')
    print(f"\n   📁 {cat.name} ({subcats.count()} sous-catégories):")
    for s in subcats:
        img = "✅" if s.image else "❌"
        prod_count = Product.objects.filter(subcategory=s).count()
        type_count = Type.objects.filter(subcategory=s).count()
        print(f"      - {s.name} (Produits: {prod_count}, Types: {type_count}, Image: {img})")

print("\n" + "="*60)
print(f"Total Catégories: {Category.objects.count()}")
print(f"Total Sous-catégories: {SubCategory.objects.count()}")
print(f"Total Marques: {Brand.objects.count()}")
print(f"Total Types: {Type.objects.count()}")
print("="*60)

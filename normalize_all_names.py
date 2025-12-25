import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Product, Brand, Type
from django.utils.text import slugify

def normalize_name(name):
    """
    Normalise un nom: première lettre de chaque mot en majuscule
    Exemple: "gaming" -> "gaming"
            "exemple test" -> "Exemple Test"
    """
    if not name:
        return name
    
    # Utiliser title() pour mettre en majuscule la première lettre de chaque mot
    normalized = name.strip().title()
    
    # Gérer les cas spéciaux (à, de, du, etc.)
    words = normalized.split()
    result = []
    for i, word in enumerate(words):
        # Garder les prépositions en minuscules sauf en début
        if i > 0 and word.lower() in ['à', 'de', 'du', 'des', 'le', 'la', 'les', 'et', 'ou']:
            result.append(word.lower())
        else:
            result.append(word)
    
    return ' '.join(result)

print('\n=== NORMALISATION DES NOMS DANS LA BASE DE DONNÉES ===\n')

# 1. CATÉGORIES
print('🔹 CATÉGORIES')
categories = Category.objects.all()
cat_updated = 0
for cat in categories:
    old_name = cat.name
    new_name = normalize_name(old_name)
    if old_name != new_name:
        cat.name = new_name
        cat.slug = slugify(new_name)
        cat.save()
        cat_updated += 1
        print(f'  ✓ "{old_name}" -> "{new_name}"')
print(f'Catégories mises à jour: {cat_updated}/{categories.count()}\n')

# 2. SOUS-CATÉGORIES
print('🔹 SOUS-CATÉGORIES')
subcategories = SubCategory.objects.all()
subcat_updated = 0
for subcat in subcategories:
    old_name = subcat.name
    new_name = normalize_name(old_name)
    if old_name != new_name:
        old_slug = subcat.slug
        subcat.name = new_name
        new_slug = slugify(new_name)
        
        # Vérifier si le slug existe déjà (sauf pour cet objet)
        if SubCategory.objects.filter(slug=new_slug).exclude(id=subcat.id).exists():
            # Ajouter l'ID pour rendre unique
            new_slug = f"{new_slug}-{subcat.id}"
        
        subcat.slug = new_slug
        subcat.save()
        subcat_updated += 1
        print(f'  ✓ "{old_name}" -> "{new_name}" (slug: {old_slug} -> {new_slug})')
print(f'Sous-catégories mises à jour: {subcat_updated}/{subcategories.count()}\n')

# 3. TYPES
print('🔹 TYPES')
types = Type.objects.all()
type_updated = 0
for typ in types:
    old_name = typ.name
    new_name = normalize_name(old_name)
    if old_name != new_name:
        new_slug = slugify(new_name)
        
        # Vérifier si le slug existe déjà
        if Type.objects.filter(slug=new_slug).exclude(id=typ.id).exists():
            new_slug = f"{new_slug}-{typ.id}"
        
        typ.name = new_name
        typ.slug = new_slug
        typ.save()
        type_updated += 1
        print(f'  ✓ "{old_name}" -> "{new_name}"')
print(f'Types mis à jour: {type_updated}/{types.count()}\n')

# 4. MARQUES
print('🔹 MARQUES')
brands = Brand.objects.all()
brand_updated = 0
for brand in brands:
    old_name = brand.name
    new_name = normalize_name(old_name)
    if old_name != new_name:
        new_slug = slugify(new_name)
        
        # Vérifier si le slug existe déjà
        if Brand.objects.filter(slug=new_slug).exclude(id=brand.id).exists():
            new_slug = f"{new_slug}-{brand.id}"
        
        brand.name = new_name
        brand.slug = new_slug
        brand.save()
        brand_updated += 1
        print(f'  ✓ "{old_name}" -> "{new_name}"')
print(f'Marques mises à jour: {brand_updated}/{brands.count()}\n')

# 5. PRODUITS
print('🔹 PRODUITS (cela peut prendre un moment...)')
products = Product.objects.all()
prod_updated = 0
for i, product in enumerate(products, 1):
    old_name = product.name
    new_name = normalize_name(old_name)
    
    # Aussi normaliser brand_text si présent
    old_brand_text = product.brand_text
    new_brand_text = normalize_name(old_brand_text) if old_brand_text else old_brand_text
    
    if old_name != new_name or old_brand_text != new_brand_text:
        product.name = new_name
        if old_brand_text != new_brand_text:
            product.brand_text = new_brand_text
        product.slug = slugify(f"{product.reference}-{new_name}")
        product.save()
        prod_updated += 1
        if prod_updated <= 20:  # Afficher seulement les 20 premiers
            print(f'  ✓ "{old_name}" -> "{new_name}"')
    
    # Afficher la progression tous les 50 produits
    if i % 50 == 0:
        print(f'  ... {i}/{products.count()} produits traités ...')

print(f'Produits mis à jour: {prod_updated}/{products.count()}\n')

# RÉSUMÉ
print('=' * 60)
print('📊 RÉSUMÉ DE LA NORMALISATION')
print('=' * 60)
print(f'Catégories:       {cat_updated} / {categories.count()}')
print(f'Sous-catégories:  {subcat_updated} / {subcategories.count()}')
print(f'Types:            {type_updated} / {types.count()}')
print(f'Marques:          {brand_updated} / {brands.count()}')
print(f'Produits:         {prod_updated} / {products.count()}')
print(f'\nTotal mis à jour: {cat_updated + subcat_updated + type_updated + brand_updated + prod_updated}')
print('=' * 60)

# Afficher quelques exemples après normalisation
print('\n📝 EXEMPLES APRÈS NORMALISATION:\n')
print('Catégories:', ', '.join([c.name for c in Category.objects.all()[:5]]))
print('Marques:', ', '.join([b.name for b in Brand.objects.all()[:8]]))
print('\n✅ Normalisation terminée!')

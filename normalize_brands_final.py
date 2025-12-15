import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Brand
from django.utils.text import slugify

def normalize_name(name):
    """
    Normalise un nom: première lettre de chaque mot en majuscule
    """
    if not name:
        return name
    
    normalized = name.strip().title()
    
    # Gérer les cas spéciaux (à, de, du, etc.)
    words = normalized.split()
    result = []
    for i, word in enumerate(words):
        if i > 0 and word.lower() in ['à', 'de', 'du', 'des', 'le', 'la', 'les', 'et', 'ou']:
            result.append(word.lower())
        else:
            result.append(word)
    
    return ' '.join(result)

print('\n=== NORMALISATION DES NOMS DE MARQUES ===\n')

brands = Brand.objects.all()
updated = 0

for brand in brands:
    old_name = brand.name
    new_name = normalize_name(old_name)
    
    if old_name != new_name:
        # Vérifier si le slug existe déjà
        new_slug = slugify(new_name)
        if Brand.objects.filter(slug=new_slug).exclude(id=brand.id).exists():
            new_slug = f"{new_slug}-{brand.id}"
        
        brand.name = new_name
        brand.slug = new_slug
        brand.save()
        updated += 1
        print(f'✓ "{old_name}" -> "{new_name}"')

print(f'\n✅ {updated} marques normalisées sur {brands.count()}')

# Afficher toutes les marques après normalisation
print('\n📋 LISTE FINALE DES MARQUES:')
for brand in Brand.objects.all().order_by('name'):
    product_count = brand.products.count()
    status = '✓' if product_count > 0 else '○'
    print(f'  {status} {brand.name} ({product_count} produits)')

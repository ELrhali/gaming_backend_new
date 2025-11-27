"""
Script pour ajouter des marques de test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Brand

# Marques gaming populaires
brands_data = [
    {'name': 'ASUS', 'description': 'Leader mondial en cartes mères, cartes graphiques et PC gaming', 'order': 1},
    {'name': 'MSI', 'description': 'Spécialiste du gaming avec des composants de haute performance', 'order': 2},
    {'name': 'Gigabyte', 'description': 'Fabricant de cartes mères et graphiques de qualité', 'order': 3},
    {'name': 'Corsair', 'description': 'Expert en périphériques gaming, mémoires RAM et boîtiers', 'order': 4},
    {'name': 'Razer', 'description': 'Marque premium de périphériques gaming', 'order': 5},
    {'name': 'Logitech', 'description': 'Leader en souris, claviers et webcams', 'order': 6},
    {'name': 'HyperX', 'description': 'Spécialiste des casques et accessoires gaming', 'order': 7},
    {'name': 'AMD', 'description': 'Fabricant de processeurs et cartes graphiques', 'order': 8},
    {'name': 'Intel', 'description': 'Leader mondial des processeurs', 'order': 9},
    {'name': 'NVIDIA', 'description': 'Leader des cartes graphiques GeForce', 'order': 10},
    {'name': 'Samsung', 'description': 'Écrans gaming et composants de stockage', 'order': 11},
    {'name': 'LG', 'description': 'Moniteurs gaming haute performance', 'order': 12},
    {'name': 'SteelSeries', 'description': 'Périphériques gaming professionnels', 'order': 13},
    {'name': 'Cooler Master', 'description': 'Boîtiers et systèmes de refroidissement', 'order': 14},
    {'name': 'Kingston', 'description': 'Mémoires RAM et stockage SSD', 'order': 15},
]

print("Ajout des marques...")
created_count = 0
updated_count = 0

for brand_data in brands_data:
    brand, created = Brand.objects.get_or_create(
        name=brand_data['name'],
        defaults={
            'description': brand_data['description'],
            'order': brand_data['order'],
            'is_active': True
        }
    )
    
    if created:
        created_count += 1
        print(f"✓ Marque créée: {brand.name}")
    else:
        # Mettre à jour si elle existe déjà
        brand.description = brand_data['description']
        brand.order = brand_data['order']
        brand.is_active = True
        brand.save()
        updated_count += 1
        print(f"→ Marque mise à jour: {brand.name}")

print(f"\nTerminé!")
print(f"- {created_count} marque(s) créée(s)")
print(f"- {updated_count} marque(s) mise(s) à jour")
print(f"Total: {Brand.objects.count()} marques dans la base de données")

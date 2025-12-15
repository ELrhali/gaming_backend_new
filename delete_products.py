"""
Script pour supprimer tous les produits
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

count = Product.objects.count()
Product.objects.all().delete()
print(f"✅ {count} produits supprimés")

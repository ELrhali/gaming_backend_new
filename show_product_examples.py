import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

# Afficher quelques exemples de produits pour comprendre la structure
print("=" * 80)
print("EXEMPLES DE PRODUITS DANS LA BASE")
print("=" * 80)

products = Product.objects.all()[:20]

for p in products:
    print(f"Reference: [{p.reference}]")
    print(f"Nom: {p.name}")
    print("-" * 40)

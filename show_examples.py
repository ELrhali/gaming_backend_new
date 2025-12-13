"""
Script pour afficher des exemples de produits importés
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, SubCategory

print("\n" + "="*80)
print("🛍️ EXEMPLES DE PRODUITS IMPORTÉS")
print("="*80)

# Afficher quelques produits par collection
subcategories = SubCategory.objects.filter(products__isnull=False).distinct()[:5]

for subcat in subcategories:
    products = subcat.products.all()[:5]
    
    print(f"\n📦 {subcat.name} ({subcat.category.name})")
    print("-" * 80)
    
    for product in products:
        discount = f" → {float(product.discount_price)} DH" if product.discount_price else ""
        brand = f" [{product.brand.name}]" if product.brand else ""
        
        print(f"\n  🏷️  {product.name}")
        print(f"     Réf: {product.reference}")
        print(f"     Prix: {float(product.price)} DH{discount}{brand}")
        print(f"     Stock: {product.quantity} unités")
        print(f"     URL: /produit/{product.slug}")

print("\n" + "="*80)
print("✅ Exemples affichés!")
print("\n🌐 Visitez http://localhost:3000 pour voir tous les produits")
print("⚙️  Accédez à http://localhost:8000/admin pour gérer le catalogue")
print("="*80 + "\n")

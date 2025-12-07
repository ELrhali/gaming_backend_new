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
import re

def extract_reference_from_folder_name(folder_name):
    """Extrait le numéro de référence du nom du dossier"""
    # Patterns de références courants
    patterns = [
        r'\b([A-Z0-9]+-[A-Z0-9-]+)\b',  # Format avec tirets: i7-12700K, RTX-4090
        r'\b(RTX\s*\d{4}\s*[A-Z]*|GTX\s*\d{4}\s*[A-Z]*)\b',  # Cartes graphiques NVIDIA
        r'\b(RX\s*\d{4}\s*[A-Z]*)\b',  # Cartes graphiques AMD
        r'\b([iI][3579]-\d{4,5}[A-Z]{0,2})\b',  # Processeurs Intel
        r'\b(Ryzen\s*[3579]\s*\d{4}[A-Z]{0,2})\b',  # Processeurs AMD Ryzen
        r'\b([A-Z]\d{3,4}[A-Z]*-[A-Z0-9]+)\b',  # Format type Z690-A, B550-F
        r'\b([A-Z]{2,}\d{3,})\b',  # Format alphanumérique: RTX4090, Z690A
    ]
    
    for pattern in patterns:
        match = re.search(pattern, folder_name, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def find_product_by_reference(folder_name):
    """Trouve un produit par son numéro de référence"""
    reference = extract_reference_from_folder_name(folder_name)
    
    if not reference:
        return None, None
    
    reference_clean = reference.upper().strip()
    
    # 1. Chercher dans le champ reference (exacte)
    product = Product.objects.filter(reference__iexact=reference_clean).first()
    if product:
        return product, reference
    
    # 2. Chercher dans le champ reference (contient)
    product = Product.objects.filter(reference__icontains=reference_clean).first()
    if product:
        return product, reference
    
    # 3. Chercher dans le nom du produit
    product = Product.objects.filter(name__icontains=reference).first()
    if product:
        return product, reference
    
    return None, reference

# Test avec quelques exemples de dossiers
IMAGES_ROOT = r"C:\Users\MSI\Desktop\all-image-produits\Produits Mustang\Produits Mustang"

print("=" * 80)
print("TEST DE DETECTION DE REFERENCES")
print("=" * 80)

if os.path.exists(IMAGES_ROOT):
    folders = [d for d in os.listdir(IMAGES_ROOT) 
               if os.path.isdir(os.path.join(IMAGES_ROOT, d))]
    
    print(f"\nNombre de dossiers: {len(folders)}")
    print("\nTest sur les 10 premiers dossiers:\n")
    
    found = 0
    not_found = 0
    
    for folder in folders[:10]:
        detected_ref = extract_reference_from_folder_name(folder)
        product, ref = find_product_by_reference(folder)
        
        print(f"Dossier: {folder}")
        print(f"  Reference detectee: {detected_ref if detected_ref else 'AUCUNE'}")
        
        if product:
            print(f"  Produit trouve: [{product.reference}] {product.name}")
            found += 1
        else:
            print(f"  Produit: NON TROUVE")
            not_found += 1
        print()
    
    print(f"\nResultats: {found} trouves, {not_found} non trouves")
else:
    print(f"\nERREUR: Le dossier {IMAGES_ROOT} n'existe pas!")

print("\n" + "=" * 80)

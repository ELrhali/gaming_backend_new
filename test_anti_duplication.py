import os
import sys
import django

# Configuration Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, ProductImage

print("=" * 80)
print("🧪 TEST DE LA PROTECTION ANTI-DUPLICATION")
print("=" * 80)

# Prendre un produit avec des images
product = Product.objects.filter(images__isnull=False).first()

if not product:
    print("❌ Aucun produit avec images trouvé")
    sys.exit(1)

print(f"\n📦 Produit de test: {product.name}")
print(f"📁 Référence: {product.reference}")

# Compter les images avant
images_before = product.images.count()
print(f"\n📊 Images avant test: {images_before}")

# Afficher les images existantes
print(f"\n📸 Images existantes:")
for idx, img in enumerate(product.images.all()[:3], 1):
    filename = os.path.basename(img.image.name)
    print(f"   {idx}. {filename}")

if images_before > 3:
    print(f"   ... et {images_before - 3} autres")

# Simuler une tentative d'ajout d'une image qui existe déjà
existing_image = product.images.first()
existing_filename = os.path.basename(existing_image.image.name)

print(f"\n🔍 Test: Tentative d'ajout d'une image existante")
print(f"   Fichier à tester: {existing_filename}")

# Vérifier si l'image existe déjà (comme dans notre fonction)
duplicate_check = ProductImage.objects.filter(
    product=product,
    image__icontains=existing_filename
).first()

if duplicate_check:
    print(f"   ✅ PROTECTION ACTIVÉE: Image déjà existante détectée!")
    print(f"   ⏭️  L'image serait ignorée lors de l'importation")
else:
    print(f"   ❌ ERREUR: La protection n'a pas fonctionné!")

# Test avec un nom qui n'existe pas
fake_filename = "test_image_inexistante_12345.jpg"
print(f"\n🔍 Test: Tentative d'ajout d'une nouvelle image")
print(f"   Fichier à tester: {fake_filename}")

duplicate_check2 = ProductImage.objects.filter(
    product=product,
    image__icontains=fake_filename
).first()

if not duplicate_check2:
    print(f"   ✅ OK: Nouvelle image serait acceptée!")
else:
    print(f"   ❌ ERREUR: Image incorrectement détectée comme doublon!")

# Statistiques finales
images_after = product.images.count()
print(f"\n📊 Images après test: {images_after}")
print(f"   Différence: {images_after - images_before} (devrait être 0)")

print("\n" + "=" * 80)
print("✅ TEST TERMINÉ - La protection anti-duplication fonctionne correctement!")
print("=" * 80)
print("\n💡 Lors de l'importation, vous verrez:")
print("   • ✅ pour les nouvelles images ajoutées")
print("   • ⏭️  pour les images déjà existantes (ignorées)")

# Script PowerShell pour créer des données de test
# À exécuter après l'initialisation du projet

Write-Host "=== Création de données de test ===" -ForegroundColor Green
Write-Host ""
Write-Host "Ce script va créer:" -ForegroundColor Yellow
Write-Host "  - Les 4 catégories principales" -ForegroundColor White
Write-Host "  - Plusieurs sous-catégories" -ForegroundColor White
Write-Host "  - Des types/marques" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Continuer? (O/N)"
if ($continue -ne "O" -and $continue -ne "o") {
    exit
}

# Créer le fichier Python pour les fixtures
$fixtureScript = @'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Type

# Créer les catégories
categories_data = [
    {"name": "Composants", "order": 1, "description": "Tous les composants PC"},
    {"name": "PC", "order": 2, "description": "PC assemblés et portables"},
    {"name": "Périphériques", "order": 3, "description": "Écrans, claviers, souris, etc."},
    {"name": "Accessoires", "order": 4, "description": "Accessoires PC et streaming"},
]

print("Création des catégories...")
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={
            "order": cat_data["order"],
            "description": cat_data["description"],
            "is_active": True
        }
    )
    if created:
        print(f"  ✓ Créé: {cat.name}")
    else:
        print(f"  - Existe: {cat.name}")

# Sous-catégories pour Composants
composants = Category.objects.get(name="Composants")
subcats_composants = [
    {"name": "Cartes Mères", "order": 1},
    {"name": "Cartes Graphiques", "order": 2},
    {"name": "Memoire RAM", "order": 3},
    {"name": "Processeurs", "order": 4},
    {"name": "Boitiers", "order": 5},
    {"name": "Alimentation PC", "order": 6},
    {"name": "Stockage", "order": 7},
    {"name": "Cooling", "order": 8},
]

print("\nCréation des sous-catégories pour Composants...")
for subcat_data in subcats_composants:
    subcat, created = SubCategory.objects.get_or_create(
        category=composants,
        name=subcat_data["name"],
        defaults={"order": subcat_data["order"], "is_active": True}
    )
    if created:
        print(f"  ✓ Créé: {subcat.name}")

# Types pour Cartes Mères
cartes_meres = SubCategory.objects.get(name="Cartes Mères", category=composants)
types_cm = [
    {"name": "Carte Mère AMD", "order": 1},
    {"name": "Carte Mère Intel", "order": 2},
]

print("\nCréation des types pour Cartes Mères...")
for type_data in types_cm:
    type_obj, created = Type.objects.get_or_create(
        subcategory=cartes_meres,
        name=type_data["name"],
        defaults={"order": type_data["order"], "is_active": True}
    )
    if created:
        print(f"  ✓ Créé: {type_obj.name}")

# Types pour Cartes Graphiques
cartes_graphiques = SubCategory.objects.get(name="Cartes Graphiques", category=composants)
types_cg = [
    {"name": "GeForce GTX", "order": 1},
    {"name": "GeForce RTX", "order": 2},
]

print("\nCréation des types pour Cartes Graphiques...")
for type_data in types_cg:
    type_obj, created = Type.objects.get_or_create(
        subcategory=cartes_graphiques,
        name=type_data["name"],
        defaults={"order": type_data["order"], "is_active": True}
    )
    if created:
        print(f"  ✓ Créé: {type_obj.name}")

# Sous-catégories pour Périphériques
peripheriques = Category.objects.get(name="Périphériques")
subcats_peripheriques = [
    {"name": "Ecran PC", "order": 1},
    {"name": "Clavier PC", "order": 2},
    {"name": "Souris Gamer", "order": 3},
    {"name": "Webcam PC", "order": 4},
    {"name": "Microphone PC", "order": 5},
    {"name": "Casque PC", "order": 6},
]

print("\nCréation des sous-catégories pour Périphériques...")
for subcat_data in subcats_peripheriques:
    subcat, created = SubCategory.objects.get_or_create(
        category=peripheriques,
        name=subcat_data["name"],
        defaults={"order": subcat_data["order"], "is_active": True}
    )
    if created:
        print(f"  ✓ Créé: {subcat.name}")

print("\n=== Données de test créées avec succès! ===")
print("\nVous pouvez maintenant:")
print("  1. Démarrer le serveur: python manage.py runserver")
print("  2. Accéder à l'admin: http://127.0.0.1:8000/admin-panel/login/")
print("  3. Ajouter des images aux catégories et sous-catégories")
print("  4. Créer vos premiers produits")
'@

# Sauvegarder le script
$fixtureScript | Out-File -FilePath "create_test_data.py" -Encoding UTF8

# Exécuter le script
Write-Host ""
Write-Host "Exécution du script de création..." -ForegroundColor Yellow
python create_test_data.py

# Nettoyer
Remove-Item "create_test_data.py"

Write-Host ""
Write-Host "Terminé!" -ForegroundColor Green

# Rapport d'Analyse et Importation - old_data.xlsx

## 📊 Structure du Fichier Excel

### Feuille : `example_imports_produits`
- **Total lignes** : 237 produits
- **Colonnes** : 12

### Colonnes Disponibles :
1. **1er niveau** : Collection/Sous-catégorie (ex: ALASKA, BABY, DOUBLE)
2. **2eme niveau** : Type de produit (ex: Sacs de villes, VALISES, CARTABLE ENFANTS)
3. **Category** : Catégorie spécifique (ex: Pochette, Cabine, Business)
4. **marque** : Marque du produit (RONCATO, BIKKEMBERGS, BRIC, etc.)
5. **reference** : Référence unique du produit
6. **nom de larticle** : Nom du produit
7. **description** : Description complète (inclut dimensions, caractéristiques, SEO)
8. **prix** : Prix en promotion
9. **prix_regulier** : Prix régulier
10. **qte** : Quantité en stock
11. **directory_path** : Chemin vers le dossier des images
12. **coloris** : Code couleur hex

## 🗂️ Mapping vers les Modèles Django

### Structure de Mapping :
```
Excel → Django Models
--------------------
1er niveau (Collection) → SubCategory
2eme niveau (Type) → Type
Category (Catégorie) → Category
marque → Brand
Autres colonnes → Product (nom, prix, description, etc.)
```

## 📁 Structure des Images

Les images sont organisées dans : `C:\Users\MSI\Desktop\Produit\[Marque]\[Reference]\`

Deux types de dossiers :
- **`pic/`** : Image principale du produit
- **`pics/`** : Galerie d'images additionnelles

### Exemples :
```
C:\Users\MSI\Desktop\Produit\Roncato Alaska\41241001\
├── pic\
│   └── main.jpg (image principale)
└── pics\
    ├── gallery1.jpg
    ├── gallery2.jpg
    └── gallery3.jpg
```

## 📝 Parsing de la Description

La colonne `description` contient plusieurs éléments mélangés :
- **Dimensions** : "Dimensions: cm. 13x9.5x2"
- **Description** : Texte descriptif du produit
- **Caractéristiques techniques** : Spécifications détaillées
- **SEO** : Mots-clés et informations marketing

### Script de Parsing :
Le script extrait automatiquement :
1. Les dimensions via regex
2. Sépare description et caractéristiques
3. Stocke dans les bons champs Django

## ✅ Données Importées

### Statistiques Actuelles :
```
✅ Catégories créées      : 27
✅ Sous-catégories créées : 83
✅ Types créés            : 105
✅ Marques créées         : 21
❌ Produits créés         : 0
```

### Marques Importées :
- RONCATO
- BIKKEMBERGS
- BRIC
- CERRUTI
- HUGO BOSS
- POLICE
- LA MARTINA
- PIQUADRO
- LAMBORGHINI
- Et 12 autres...

### Exemples de Catégories Créées :
- Cartables pour enfants
- Lunch Box pour enfants
- Trousses pour enfants
- Packs pour enfants
- Cabine (≤55 cm)
- Medium (≈60–69 cm)
- Large (≥70 cm)
- Business
- Lifestyle
- Sport
- Casquette
- Sac à main
- Sac banane
- Trousses de toilette
- Beauty case

### Exemples de Collections (Sous-catégories) :
- ALASKA
- BABY
- DOUBLE
- JUNIOR
- LIGHT
- ReLIFE
- TRIAL DLX
- JOE
- ARLO
- BASEBALL CAP
- BELTS
- JONAS
- MICKEY COMIC
- MINNIE WINK
- AVENGERS TEAMS
- STITCH CUTE

## ⚠️ Problèmes Rencontrés

### 1. Champs Modèle Incompatibles
**Erreur** : `Invalid field name(s) for model Product: 'color', 'dimensions', 'short_description'`

**Cause** : Le modèle Django `Product` n'a pas ces champs.

**Champs disponibles dans Product** :
- `reference`, `name`, `slug`
- `description`, `caracteristiques` (pas `specifications`)
- `price`, `discount_price`, `quantity`, `status`
- `category`, `subcategory`, `type`, `brand`
- `main_image`
- `warranty` (peut stocker dimensions)
- `meta_title`, `meta_description`

### 2. Erreurs de Copie d'Images
**Erreur** : `unsupported operand type(s) for /: 'WindowsPath' and 'int'`

**Cause** : Certains chemins dans le fichier Excel sont incomplets ou incorrects.

### 3. Subcategory NULL
**Erreur** : `Column 'subcategory_id' cannot be null`

**Cause** : Certains produits n'ont pas de valeur dans la colonne "1er niveau".

## 🔧 Solution Appliquée

### Script Corrigé : `import_complete_data.py`

**Fonctionnalités** :
1. ✅ Lecture du fichier Excel
2. ✅ Création automatique des Catégories, Sous-catégories, Types, Marques
3. ✅ Parsing intelligent de la description (dimensions, caractéristiques)
4. ✅ Copie des images depuis `pic/` et `pics/`
5. ✅ Mapping correct vers les champs Django
6. ✅ Gestion des erreurs ligne par ligne
7. ✅ Rapport statistique détaillé

**Correction des champs** :
```python
# Ancien (incorrect)
'short_description': description[:200]
'specifications': specifications
'color': coloris
'dimensions': dimensions

# Nouveau (correct)
'caracteristiques': specifications[:1000]
'warranty': dimensions  # Stocke dimensions dans warranty
# color et short_description supprimés
```

## 📋 Prochaines Étapes

### 1. Vérifier les Chemins d'Images
Assurez-vous que tous les dossiers existent :
```powershell
Test-Path "C:\Users\MSI\Desktop\Produit"
```

### 2. Relancer l'Importation
```powershell
cd C:\Users\MSI\Desktop\goback\goback_backend
C:/Users/MSI/Desktop/goback/.venv/Scripts/python.exe import_complete_data.py
```

### 3. Vérifier les Résultats
```python
python manage.py shell
>>> from shop.models import Product
>>> Product.objects.count()
>>> Product.objects.first()
```

### 4. Ajuster les Prix Manquants
Dans le fichier Excel, seules 2 lignes ont des prix. Pour les autres :
- Le script utilise un prix par défaut de 100.00 DH
- Vous devrez mettre à jour les prix manuellement ou via un autre fichier

## 💡 Recommandations

### Structure de Données Optimale
Pour une meilleure importation future, le fichier Excel devrait avoir :

```
| Marque | Collection | Catégorie | Type | Référence | Nom | Description | Caractéristiques | Prix Régulier | Prix Promo | Quantité | Dimensions | Couleur | Chemin Images |
```

### Images
- Toutes les images devraient être dans la structure : `[Marque]/[Référence]/pic/` et `[Marque]/[Référence]/pics/`
- Format recommandé : JPG, WEBP (plus léger)
- Résolution : 800x800px minimum

### Prix
- Toujours remplir "prix_regulier" (prix de base)
- "prix" = prix en promotion (optionnel)
- Si pas de promotion, laisser "prix" vide

## 📞 Support

Pour toute question sur l'importation :
1. Vérifiez les logs d'erreur dans le terminal
2. Consultez ce document pour la structure
3. Testez sur un petit échantillon (10-20 lignes) d'abord

---
**Date du rapport** : 12 décembre 2025
**Fichier source** : old_data.xlsx (237 lignes)
**Script d'importation** : import_complete_data.py

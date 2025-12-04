# Importation des Images de Produits

## 📋 Description

Cette fonctionnalité permet d'importer automatiquement les images de produits depuis un dossier local vers votre base de données. Elle est accessible directement depuis le panneau d'administration.

## 🚀 Accès à la Fonctionnalité

### Via le Menu
1. Connectez-vous au panneau d'administration
2. Dans le menu latéral, section **IMPORTATION**
3. Cliquez sur **Images Produits**

### Via la Liste des Produits
1. Allez dans **Produits**
2. Cliquez sur le bouton **Importer Images** en haut à droite

### URL Directe
```
http://127.0.0.1:8000/admin/products/images-import/
```

## 📁 Structure du Dossier Requise

Le dossier d'images doit suivre cette structure :

```
Dossier Principal/
├── Nom du Produit 1/              # Le nom doit correspondre au nom dans la base
│   └── Référence Produit/          # Ex: BT000050
│       ├── Image/                  # Contient l'image principale
│       │   └── image-principale.jpg
│       └── Menu/                   # Contient les images supplémentaires
│           ├── image-1.jpg
│           ├── image-2.jpg
│           └── image-3.jpg
├── Nom du Produit 2/
│   └── Référence Produit/
│       ├── Image/
│       └── Menu/
└── ...
```

### Exemple Réel
```
C:\Users\MSI\Desktop\all-image-produits\Produits Mustang\Produits Mustang\
├── AH T200 Noir/
│   └── BT000050/
│       ├── Image/
│       │   └── Atlas-Gaming-Thermaltake-AH-T200-Noir-A-1200x1200.jpg
│       └── Menu/
│           ├── ah_t200_3.jpg
│           ├── ah_t200_5.jpg
│           └── ...
├── CORSAIR SOURIS IRONCLAW RGB NOIR/
│   └── SR0000003/
│       ├── Image/
│       └── Menu/
└── ...
```

## ⚙️ Utilisation

1. **Entrez le chemin du dossier**
   - Collez le chemin complet du dossier contenant vos produits
   - Exemple : `C:\Users\MSI\Desktop\all-image-produits\Produits Mustang\Produits Mustang`

2. **Cliquez sur "Démarrer l'importation"**
   - Le système va scanner tous les sous-dossiers
   - Rechercher les produits correspondants dans la base
   - Importer les images

3. **Consultez les résultats**
   - Un résumé s'affiche avec les statistiques
   - Les logs détaillés montrent chaque opération

## 📊 Rapports d'Importation

Le système génère un rapport détaillé incluant :

- ✅ Nombre de produits traités avec succès
- 🖼️ Nombre total d'images importées
- ⚠️ Produits non trouvés en base de données
- ❌ Erreurs rencontrées

### Exemple de Rapport
```
✅ Importation terminée!
• 150/208 produits traités avec succès
• 837 images importées
• 58 produits non trouvés en base
• 0 erreurs
```

## 🔍 Correspondance des Noms

Le système effectue une recherche **insensible à la casse** :
- `AH T200 Noir` = `ah t200 noir` = `AH t200 NOIR`
- Les espaces en début/fin sont automatiquement supprimés

## 📝 Notes Importantes

### Formats d'Images Supportés
- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.webp`
- `.bmp`

### Images Principales
- La **première image** du dossier `Image/` devient l'image principale
- Si une image principale existe déjà, elle sera remplacée

### Images Supplémentaires
- Toutes les images du dossier `Menu/` sont ajoutées comme images supplémentaires
- Elles sont triées par ordre alphabétique

### Gestion des Erreurs
- Les images corrompues sont ignorées
- Les noms de fichiers trop longs (>100 caractères) peuvent causer des erreurs
- Les produits non trouvés sont listés dans un rapport

## 🛠️ Script en Ligne de Commande

Si vous préférez utiliser le script en ligne de commande :

```bash
cd backend
python import_product_images.py
```

Le script utilisera le chemin par défaut défini dans le code :
```python
IMAGES_ROOT = r"C:\Users\MSI\Desktop\all-image-produits\Produits Mustang\Produits Mustang"
```

Pour utiliser un autre chemin, modifiez cette variable dans `import_product_images.py`.

## 🔧 Fichiers Créés/Modifiés

### Nouveaux Fichiers
- `backend/import_product_images.py` - Script d'importation autonome
- `backend/templates/admin_panel/product_images_import.html` - Interface admin

### Fichiers Modifiés
- `backend/admin_panel/views.py` - Ajout de la vue `product_images_import`
- `backend/admin_panel/urls.py` - Ajout de la route
- `backend/templates/admin_panel/base.html` - Ajout du menu
- `backend/templates/admin_panel/product_list.html` - Ajout du bouton

## 💡 Conseils

1. **Vérifiez les noms** : Assurez-vous que les noms de dossiers correspondent exactement aux noms de produits en base
2. **Sauvegardez** : Faites une sauvegarde de votre base avant une importation massive
3. **Testez** : Commencez avec un petit dossier pour tester
4. **Nettoyez** : Supprimez les images inutiles avant l'importation pour gagner du temps

## ❓ Dépannage

### "Produit non trouvé dans la base de données"
- Vérifiez que le nom du dossier correspond exactement au nom du produit
- Cherchez le produit dans l'admin pour voir son nom exact
- Vérifiez qu'il n'y a pas d'espaces supplémentaires

### "Dossier 'Image' non trouvé"
- Vérifiez la structure : `Nom Produit/Référence/Image/`
- Le nom du dossier doit être exactement "Image" (peut être en minuscules)

### "Data too long for column 'image'"
- Le nom de fichier est trop long
- Renommez le fichier avec un nom plus court

### Images non visibles sur le site
- Vérifiez que les images sont bien dans `media/products/gallery/`
- Redémarrez le serveur Django
- Videz le cache du navigateur

## 📞 Support

Pour toute question ou problème, consultez les logs détaillés affichés après l'importation.

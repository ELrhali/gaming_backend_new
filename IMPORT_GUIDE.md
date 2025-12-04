# Guide d'Importation de Produits depuis Excel

## 📋 Vue d'ensemble

Cette fonctionnalité permet d'importer plusieurs produits en une seule fois depuis un fichier Excel, avec gestion automatique des doublons, création de relations (catégories, sous-catégories, marques, types) et parsing des caractéristiques.

## 🚀 Accès à l'Interface

1. Connectez-vous au panel d'administration
2. Allez dans **Produits** → Cliquez sur le bouton **"Importer Excel"**
3. Vous accédez à la page d'importation avec les statistiques actuelles

## 📊 Format du Fichier Excel

### Colonnes Obligatoires (*)

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| **Référence *** | Texte | Référence unique du produit | CPU001, GPU002 |
| **Nom du produit *** | Texte | Nom commercial du produit | Intel Core i9-13900K |
| **Catégorie *** | Texte | Catégorie principale (doit exister) | Composants, Périphériques |
| **Sous-catégorie *** | Texte | Sous-catégorie (doit exister) | Processeurs, Cartes Graphiques |
| **Prix (DH) *** | Nombre | Prix unitaire en dirhams | 6500.00 |
| **Quantité *** | Nombre | Stock disponible | 15 |
| **Description *** | Texte | Description du produit | Processeur gaming haute performance |

### Colonnes Optionnelles

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| Marque | Texte | Marque du produit (créée automatiquement) | Intel, AMD, NVIDIA |
| Type | Texte | Type/Modèle (créé automatiquement) | Core i9, RTX 4090 |
| Collection | Texte | Collection (créée automatiquement) | Gaming Pro 2024 |
| Prix Promo (DH) | Nombre | Prix réduit si promo | 5999.00 |
| Caractéristiques | Texte multiligne | Spécifications techniques | • Cœurs: 24<br>• Threads: 32 |
| Garantie | Texte | Durée de garantie | 2 ans, 3 ans constructeur |
| Poids (kg) | Nombre | Poids du produit | 0.5 |
| Meta Titre SEO | Texte | Titre pour SEO | Processeur Intel i9 Gaming |
| Meta Description SEO | Texte | Description pour SEO | Le meilleur processeur... |
| Best Seller | Oui/Non | Produit best-seller | Oui, Non, True, False |
| En vedette | Oui/Non | Produit en vedette | Oui, Non |
| Nouveau | Oui/Non | Nouveau produit | Oui, Non |
| Statut | Texte | État du stock | en stock, rupture, précommande |

## 🔧 Fonctionnalités Automatiques

### 1. Déduplication Intelligente

- **Références uniques**: Les produits avec une référence existante sont automatiquement ignorés
- **Rapports détaillés**: Le système indique combien de produits ont été créés vs ignorés

### 2. Normalisation des Noms

Le système normalise automatiquement les noms de sous-catégories:

| Excel | Base de données |
|-------|-----------------|
| ALIMENTATION, alimentations | Alimentations |
| BOITIER, BOÎTIER | Boîtiers PC |
| PROCESSEUR, processeurs | Processeurs |
| ECRAN, ÉCRAN | Écrans |
| CARTE GRAPHIQUE | Cartes Graphiques |
| MEMOIRE RAM, mémoire ram | Mémoire RAM |
| SOURIS | Souris Gaming |

### 3. Création Automatique

- **Marques**: Si une marque n'existe pas, elle est créée automatiquement
- **Types**: Créés automatiquement avec relation à la sous-catégorie et la marque
- **Collections**: Créées automatiquement si mentionnées

### 4. Parsing des Caractéristiques

Le système parse automatiquement les caractéristiques au format:

```
• Cœurs: 24
• Threads: 32
• Fréquence: 5.8 GHz
• Socket: LGA 1700
• TDP: 125W
```

Chaque ligne est extraite comme une paire clé-valeur et stockée séparément dans `ProductSpecification`.

### 5. Validation des Données

Le système ignore automatiquement les lignes avec:
- Champs obligatoires vides
- Prix ou quantité invalides (marqués avec "-")
- Données incohérentes
- Erreurs d'encodage

## 📝 Exemple de Fichier Excel

Voici un exemple de fichier Excel prêt à l'importation:

| Référence * | Nom du produit * | Catégorie * | Sous-catégorie * | Marque | Type | Prix (DH) * | Quantité * | Description * | Caractéristiques |
|-------------|------------------|-------------|------------------|---------|------|-------------|------------|---------------|------------------|
| CPU001 | Processeur Intel Core i9-13900K | Composants | Processeurs | Intel | Core i9 | 6500.00 | 15 | Processeur gaming haute performance | • Cœurs: 24<br>• Threads: 32<br>• Fréquence: 5.8 GHz |
| GPU001 | NVIDIA RTX 4090 | Composants | Cartes Graphiques | NVIDIA | RTX 4090 | 22000.00 | 8 | Carte graphique ultra puissante | • Mémoire: 24 GB GDDR6X<br>• CUDA Cores: 16384 |
| RAM001 | Corsair Vengeance RGB 32GB | Composants | Mémoire RAM | Corsair | Vengeance | 1500.00 | 25 | Kit mémoire DDR5 32GB | • Capacité: 32 GB<br>• Type: DDR5<br>• Fréquence: 6000 MHz |

## 🎯 Processus d'Importation

### Étape 1: Préparation
1. Préparez votre fichier Excel avec toutes les données
2. Vérifiez que les catégories et sous-catégories existent dans la base
3. Assurez-vous que les références sont uniques

### Étape 2: Upload
1. Accédez à la page d'importation
2. Cliquez sur "Choisir un fichier"
3. Sélectionnez votre fichier Excel (.xlsx ou .xls)
4. Cliquez sur "Importer les Produits"

### Étape 3: Résultat
Le système affiche un rapport complet:
```
✅ Importation terminée avec succès!
• 196 produits créés
• 35 produits ignorés (doublons ou données manquantes)
• 5 nouvelles marques créées: ASUS, MSI, Gigabyte, Corsair, Kingston
• 12 nouveaux types créés: RTX 4090, Core i9, Vengeance, ...
• 2 nouvelles collections créées: Gaming Pro 2024, RGB Elite
```

### Étape 4: Vérification
- Les produits sont immédiatement visibles dans la liste
- Toutes les relations (marques, types) sont créées
- Les caractéristiques sont parsées et stockées

## ⚠️ Points d'Attention

### Catégories et Sous-catégories
**Important**: Les catégories et sous-catégories doivent déjà exister dans la base de données. Si elles n'existent pas, créez-les d'abord via:
- **Catégories** → Ajouter une catégorie
- **Sous-catégories** → Ajouter une sous-catégorie

### Références Uniques
- Chaque référence doit être unique
- Les doublons sont automatiquement ignorés
- Aucun produit existant n'est modifié

### Format des Données
- **Prix**: Nombres décimaux avec point (6500.00)
- **Quantités**: Nombres entiers (15, 20, 100)
- **Booléens**: "Oui", "Non", "True", "False", "1", "0"

### Encodage
- Utilisez UTF-8 pour l'encodage du fichier Excel
- Les caractères spéciaux (é, à, ç) sont supportés

## 🔍 Dépannage

### Problème: "Catégorie non trouvée"
**Solution**: Créez d'abord la catégorie via l'interface admin

### Problème: "Sous-catégorie non trouvée"
**Solution**: 
1. Vérifiez l'orthographe exacte
2. Utilisez les noms normalisés (voir tableau de normalisation)
3. Créez la sous-catégorie si elle n'existe pas

### Problème: "Produits ignorés"
**Causes possibles**:
- Référence déjà existante (doublon)
- Champs obligatoires vides
- Prix ou quantité avec "-"
- Données de mauvaise qualité

**Solution**: Consultez le rapport d'erreurs détaillé affiché après l'importation

### Problème: Caractéristiques non parsées
**Solution**: Utilisez le format exact:
```
• Nom: Valeur
• Autre: Autre valeur
```
- Commencez par une puce (•, -, *, +)
- Utilisez deux-points (:) pour séparer clé et valeur
- Une caractéristique par ligne

## 📈 Bonnes Pratiques

1. **Testez avec un petit fichier** (5-10 produits) avant l'import complet
2. **Vérifiez les statistiques** avant et après l'import
3. **Gardez une copie** de votre fichier Excel original
4. **Consultez les rapports** d'erreurs pour corriger les problèmes
5. **Importez par lots** si vous avez beaucoup de produits (max 500 par fichier)

## 🎓 Exemples Avancés

### Exemple 1: Produit Complet avec Toutes les Options

```
Référence: CPU-INTEL-I9-13900K
Nom: Processeur Intel Core i9-13900K 13ème Génération
Catégorie: Composants
Sous-catégorie: Processeurs
Marque: Intel
Type: Core i9
Collection: 13ème Génération
Prix: 6500.00
Prix Promo: 5999.00
Quantité: 15
Description: Le processeur Intel Core i9-13900K offre des performances exceptionnelles pour le gaming et la création de contenu...
Caractéristiques:
• Cœurs: 24 (8P+16E)
• Threads: 32
• Fréquence de base: 3.0 GHz
• Fréquence turbo: 5.8 GHz
• Cache: 36 MB Intel Smart Cache
• Socket: LGA 1700
• TDP: 125W
• Mémoire supportée: DDR5-5600, DDR4-3200
Garantie: 3 ans constructeur
Poids: 0.5
Meta Titre SEO: Processeur Intel Core i9-13900K - Performance Gaming Ultime
Meta Description SEO: Découvrez le processeur Intel Core i9-13900K avec 24 cœurs...
Best Seller: Oui
En vedette: Oui
Nouveau: Non
Statut: en stock
```

### Exemple 2: Import de Plusieurs Marques

Vous pouvez importer des produits de différentes marques en une seule fois:

| Référence | Nom | Marque | Type | Catégorie | Sous-catégorie |
|-----------|-----|--------|------|-----------|----------------|
| CPU-INTEL-01 | Intel Core i9 | Intel | Core i9 | Composants | Processeurs |
| CPU-AMD-01 | AMD Ryzen 9 | AMD | Ryzen 9 | Composants | Processeurs |
| GPU-NVIDIA-01 | NVIDIA RTX 4090 | NVIDIA | RTX 4090 | Composants | Cartes Graphiques |
| GPU-AMD-01 | AMD RX 7900 XTX | AMD | RX 7900 | Composants | Cartes Graphiques |

Toutes les marques et types seront créés automatiquement!

## 📞 Support

Si vous rencontrez des problèmes:
1. Consultez les messages d'erreur détaillés
2. Vérifiez le format de votre fichier Excel
3. Testez avec un fichier exemple minimal
4. Contactez l'administrateur système si le problème persiste

---

**Version**: 1.0  
**Dernière mise à jour**: Décembre 2024  
**Auteur**: Backend Admin Panel

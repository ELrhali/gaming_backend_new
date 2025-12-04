"""
Script pour créer un fichier Excel de test minimal
"""
import pandas as pd
import os

# Données de test
data = {
    'Référence *': ['TEST001', 'TEST002', 'TEST003', 'TEST004', 'TEST005'],
    'Nom du produit *': [
        'Processeur Test Intel Core i5',
        'Carte Graphique Test NVIDIA GTX 1650',
        'Clavier Gaming Test RGB',
        'Souris Gaming Test Pro',
        'Écran Test 24 pouces Full HD'
    ],
    'Catégorie *': ['Composants', 'Composants', 'Périphériques', 'Périphériques', 'Périphériques'],
    'Sous-catégorie *': ['Processeurs', 'Cartes Graphiques', 'Claviers Gaming', 'Souris Gaming', 'Écrans'],
    'Marque': ['Intel', 'NVIDIA', 'Logitech', 'Razer', 'Samsung'],
    'Type': ['Core i5', 'GTX 1650', 'G Pro', 'DeathAdder', 'Monitor'],
    'Prix (DH) *': [1500.00, 2500.00, 450.00, 350.00, 1800.00],
    'Prix Promo (DH)': [1399.00, None, 399.00, None, 1699.00],
    'Quantité *': [20, 15, 30, 25, 10],
    'Description *': [
        'Processeur Intel Core i5 pour gaming et bureautique',
        'Carte graphique NVIDIA GTX 1650 performante',
        'Clavier gaming mécanique avec RGB',
        'Souris gaming haute précision',
        'Écran 24 pouces Full HD pour gaming'
    ],
    'Caractéristiques': [
        '• Cœurs: 6\n• Threads: 12\n• Fréquence: 4.2 GHz\n• Socket: LGA 1700',
        '• Mémoire: 4 GB GDDR6\n• CUDA Cores: 896\n• Fréquence: 1665 MHz',
        '• Type: Mécanique\n• Switches: Cherry MX Red\n• RGB: Oui\n• Touches: 104',
        '• DPI: 16000\n• Capteur: Optique\n• Boutons: 7\n• RGB: Oui',
        '• Taille: 24 pouces\n• Résolution: 1920x1080\n• Fréquence: 144 Hz\n• Temps de réponse: 1ms'
    ],
    'Garantie': ['3 ans', '2 ans', '2 ans', '2 ans', '3 ans'],
    'Poids (kg)': [0.3, 0.8, 1.2, 0.15, 4.5],
    'Meta Titre SEO': [
        'Processeur Intel Core i5 - Gaming PC',
        'Carte Graphique NVIDIA GTX 1650',
        'Clavier Gaming RGB Logitech',
        'Souris Gaming Razer Pro',
        'Écran Gaming 24" 144Hz'
    ],
    'Meta Description SEO': [
        'Processeur Intel Core i5 pour PC gaming performant',
        'Carte graphique NVIDIA GTX 1650 4GB pour gaming',
        'Clavier gaming mécanique RGB avec switches Cherry MX',
        'Souris gaming haute précision 16000 DPI',
        'Écran gaming 24 pouces Full HD 144Hz 1ms'
    ],
    'Best Seller': ['Oui', 'Non', 'Oui', 'Oui', 'Non'],
    'En vedette': ['Oui', 'Oui', 'Non', 'Oui', 'Oui'],
    'Nouveau': ['Non', 'Non', 'Oui', 'Non', 'Oui'],
    'Statut': ['en stock', 'en stock', 'en stock', 'en stock', 'en stock'],
    'Collection': ['Gaming Pro 2024', 'Budget Gaming', 'RGB Elite', 'Pro Series', 'Gaming Monitors']
}

# Créer le DataFrame
df = pd.DataFrame(data)

# Chemin de sauvegarde
output_path = r'C:\Users\MSI\Desktop\amr\backend\test_import_products.xlsx'

# Sauvegarder en Excel
df.to_excel(output_path, index=False, sheet_name='Produits')

print(f"✅ Fichier Excel de test créé: {output_path}")
print(f"📊 Nombre de produits: {len(df)}")
print(f"\n📋 Colonnes incluses:")
for col in df.columns:
    print(f"   • {col}")

print(f"\n📦 Produits créés:")
for idx, row in df.iterrows():
    print(f"   {idx+1}. {row['Référence *']} - {row['Nom du produit *']}")

print(f"\n💡 Pour importer ce fichier:")
print(f"   1. Accédez à http://localhost:8000/admin-panel/products/import/")
print(f"   2. Uploadez le fichier: {output_path}")
print(f"   3. Cliquez sur 'Importer les Produits'")

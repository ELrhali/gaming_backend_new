import pandas as pd
from collections import defaultdict

# Charger le fichier Excel
EXCEL_FILE = r'C:\Users\MSI\Desktop\gaming\old_data.xlsx'
df = pd.read_excel(EXCEL_FILE)

print("\n" + "=" * 80)
print("ANALYSE DU FICHIER old_data.xlsx")
print("=" * 80)
print(f"\nNombre total de lignes: {len(df)}")
print(f"Nombre de colonnes: {len(df.columns)}")

# Colonnes selon import_final_structure.py
COL_1ER_NIVEAU = 0    # Collection
COL_2EME_NIVEAU = 1   # Category
COL_CATEGORY = 2      # SubCategory
COL_MARQUE = 3        # Brand

print("\n" + "-" * 80)
print("COLONNES DU FICHIER:")
print("-" * 80)
for idx, col in enumerate(df.columns):
    print(f"{idx}: {col}")

# 1. ANALYSE DES CATEGORIES (2eme niveau)
print("\n" + "=" * 80)
print("1. CATEGORIES (Colonne '2eme niveau' - index 1)")
print("=" * 80)

categories = df.iloc[:, COL_2EME_NIVEAU].dropna().unique()
print(f"\n[✓] Nombre de catégories UNIQUES: {len(categories)}")
print("\nListe des catégories:")
for i, cat in enumerate(sorted(categories), 1):
    count = (df.iloc[:, COL_2EME_NIVEAU] == cat).sum()
    print(f"  {i:2d}. {cat} ({count} produits)")

# 2. ANALYSE DES SOUS-CATEGORIES
print("\n" + "=" * 80)
print("2. SOUS-CATEGORIES (Colonne 'Category' - index 2)")
print("=" * 80)

subcategories = df.iloc[:, COL_CATEGORY].dropna().unique()
print(f"\n[✓] Nombre de sous-catégories UNIQUES: {len(subcategories)}")

# Vérifier la relation sous-catégorie -> catégorie
subcategory_to_categories = defaultdict(set)
for _, row in df.iterrows():
    subcategory = row.iloc[COL_CATEGORY]
    category = row.iloc[COL_2EME_NIVEAU]
    if pd.notna(subcategory) and pd.notna(category):
        subcategory_to_categories[subcategory].add(category)

print("\nListe des sous-catégories avec leur(s) catégorie(s) parente(s):")
duplicates_found = False
for i, subcat in enumerate(sorted(subcategories), 1):
    categories_list = sorted(subcategory_to_categories[subcat])
    count = (df.iloc[:, COL_CATEGORY] == subcat).sum()
    
    # Vérifier si la sous-catégorie appartient à plusieurs catégories
    if len(categories_list) > 1:
        duplicates_found = True
        print(f"  {i:2d}. ⚠️  {subcat} ({count} produits)")
        print(f"      -> APPARTIENT À {len(categories_list)} CATÉGORIES: {', '.join(categories_list)}")
    else:
        print(f"  {i:2d}. ✓ {subcat} ({count} produits) -> {categories_list[0] if categories_list else 'N/A'}")

# 3. ALERTE DUPLICATIONS
print("\n" + "=" * 80)
print("3. VÉRIFICATION DES DUPLICATIONS")
print("=" * 80)

if duplicates_found:
    print("\n⚠️  ATTENTION: Des sous-catégories sont affectées à PLUSIEURS catégories!")
    print("\nDétails des problèmes:")
    for subcat, cats in sorted(subcategory_to_categories.items()):
        if len(cats) > 1:
            print(f"\n  • Sous-catégorie: {subcat}")
            print(f"    Catégories parentes: {', '.join(sorted(cats))}")
            print(f"    Nombre de catégories: {len(cats)}")
            
            # Afficher la répartition
            for cat in sorted(cats):
                count = len(df[(df.iloc[:, COL_CATEGORY] == subcat) & (df.iloc[:, COL_2EME_NIVEAU] == cat)])
                print(f"      - {cat}: {count} produits")
else:
    print("\n✓ PARFAIT: Chaque sous-catégorie appartient à UNE SEULE catégorie!")

# 4. ANALYSE DES MARQUES
print("\n" + "=" * 80)
print("4. MARQUES (Colonne 'marque' - index 3)")
print("=" * 80)

brands = df.iloc[:, COL_MARQUE].dropna().unique()
print(f"\n[✓] Nombre de marques UNIQUES: {len(brands)}")
print("\nListe des marques (top 30):")
brand_counts = df.iloc[:, COL_MARQUE].value_counts()
for i, (brand, count) in enumerate(brand_counts.head(30).items(), 1):
    print(f"  {i:2d}. {brand} ({count} produits)")

if len(brand_counts) > 30:
    print(f"  ... et {len(brand_counts) - 30} autres marques")

# 5. ANALYSE DES COLLECTIONS (1er niveau)
print("\n" + "=" * 80)
print("5. COLLECTIONS (Colonne '1er niveau' - index 0)")
print("=" * 80)

collections = df.iloc[:, COL_1ER_NIVEAU].dropna().unique()
print(f"\n[✓] Nombre de collections UNIQUES: {len(collections)}")
print("\nListe des collections:")
for i, coll in enumerate(sorted(collections), 1):
    count = (df.iloc[:, COL_1ER_NIVEAU] == coll).sum()
    print(f"  {i:2d}. {coll} ({count} produits)")

# 6. RÉSUMÉ FINAL
print("\n" + "=" * 80)
print("RÉSUMÉ DE L'ANALYSE")
print("=" * 80)
print(f"""
📊 Statistiques globales:
   - Collections (1er niveau)     : {len(collections)}
   - Catégories (2eme niveau)     : {len(categories)}
   - Sous-catégories (Category)   : {len(subcategories)}
   - Marques                      : {len(brands)}
   - Total produits               : {len(df)}

{'⚠️  ATTENTION: Des duplications détectées!' if duplicates_found else '✓ Structure propre, pas de duplications'}
""")

# 7. RECOMMENDATIONS
if duplicates_found:
    print("\n" + "=" * 80)
    print("RECOMMANDATIONS")
    print("=" * 80)
    print("""
Pour corriger les duplications, vous avez 2 options:

OPTION 1: Renommer les sous-catégories dupliquées
   Exemple: Si "Sacs" existe dans "Maternelle" et "Primaire"
   -> Renommer en "Sacs Maternelle" et "Sacs Primaire"

OPTION 2: Accepter les duplications mais les lier correctement
   -> Modifier le script import pour utiliser une clé unique 
      (catégorie + sous-catégorie) au lieu du nom seul

Le script actuel utilise déjà l'OPTION 2 (ligne 211):
   subcategory_key = f"{deuxieme_niveau}_{subcategory_name}"

Donc l'import devrait fonctionner correctement même avec les duplications!
""")

print("=" * 80)

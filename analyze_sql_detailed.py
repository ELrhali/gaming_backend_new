import re

# Lire le fichier SQL et extraire les informations importantes
sql_file = r"C:\Users\MSI\Desktop\goback\gobagma_boutique_valises_maroc (1).sql"

print("📊 ANALYSE COMPLÈTE DE LA BASE DE DONNÉES SQL\n")
print("=" * 80)

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
    
    # Trouver toutes les tables CREATE TABLE
    tables_pattern = r'CREATE TABLE `(\w+)` \((.*?)\) ENGINE'
    tables = re.findall(tables_pattern, content, re.DOTALL | re.IGNORECASE)
    
    print("\n📋 TABLES TROUVÉES ET LEURS COLONNES:\n")
    
    for table_name, columns in tables[:20]:  # Premières 20 tables
        print(f"\n{'='*80}")
        print(f"TABLE: {table_name}")
        print(f"{'='*80}")
        
        # Extraire les colonnes
        column_lines = columns.strip().split('\n')
        for line in column_lines[:15]:  # Premières 15 colonnes
            line = line.strip()
            if line and not line.startswith('KEY') and not line.startswith('CONSTRAINT'):
                print(f"  {line}")
    
    # Statistiques
    print(f"\n\n{'='*80}")
    print(f"STATISTIQUES:")
    print(f"{'='*80}")
    print(f"Total de tables: {len(tables)}")
    
    # Tables importantes pour mapping
    important_tables = ['categories', 'types', 'produits', 'produit_categories', 'category_images']
    
    print(f"\n\n{'='*80}")
    print(f"TABLES IMPORTANTES IDENTIFIÉES:")
    print(f"{'='*80}")
    for table_name, _ in tables:
        if table_name in important_tables or 'categ' in table_name.lower() or 'prod' in table_name.lower() or 'type' in table_name.lower():
            print(f"  ✓ {table_name}")

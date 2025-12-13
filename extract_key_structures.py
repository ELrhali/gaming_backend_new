import re

sql_file = r"C:\Users\MSI\Desktop\goback\gobagma_boutique_valises_maroc (1).sql"

print("📊 EXTRACTION DES STRUCTURES CLÉS\n")

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
    
    # Tables à analyser en détail
    tables_to_analyze = ['types', 'produits', 'produit_categories', 'niveaux']
    
    for table_name in tables_to_analyze:
        pattern = rf'CREATE TABLE `{table_name}` \((.*?)\) ENGINE'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            print(f"\n{'='*80}")
            print(f"TABLE: {table_name}")
            print(f"{'='*80}")
            columns = match.group(1).strip().split('\n')
            for line in columns:
                line = line.strip()
                if line and not line.startswith('KEY') and not line.startswith('CONSTRAINT'):
                    print(f"  {line}")
    
    # Extraire quelques données d'exemple de la table categories
    print(f"\n\n{'='*80}")
    print(f"EXEMPLES DE DONNÉES - CATEGORIES")
    print(f"{'='*80}")
    
    categories_pattern = r"INSERT INTO `categories`.*?VALUES\s+(.*?);"
    categories_match = re.search(categories_pattern, content[:100000], re.DOTALL)
    if categories_match:
        # Afficher les 5 premières catégories
        lines = categories_match.group(1).split('\n')
        for i, line in enumerate(lines[:10]):
            if line.strip() and not line.strip().startswith('--'):
                print(line[:200] + "...")
    
    # Extraire quelques données de types
    print(f"\n\n{'='*80}")
    print(f"EXEMPLES DE DONNÉES - TYPES")
    print(f"{'='*80}")
    
    types_pattern = r"INSERT INTO `types`.*?VALUES\s+(.*?);"
    types_match = re.search(types_pattern, content[:200000], re.DOTALL)
    if types_match:
        lines = types_match.group(1).split('\n')
        for i, line in enumerate(lines[:15]):
            if line.strip() and not line.strip().startswith('--'):
                print(line[:200] + "...")

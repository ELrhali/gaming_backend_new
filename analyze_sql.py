import re

# Lire les premières lignes du fichier SQL pour analyser la structure
sql_file = r"C:\Users\MSI\Desktop\goback\gobagma_boutique_valises_maroc (1).sql"

print("📊 Analyse du fichier SQL...\n")

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = []
    for i, line in enumerate(f):
        if i < 200:  # Lire les 200 premières lignes
            lines.append(line)
        else:
            break
    
    content = ''.join(lines)
    
    # Chercher les CREATE TABLE statements
    print("=" * 60)
    print("TABLES TROUVÉES:")
    print("=" * 60)
    
    tables = re.findall(r'CREATE TABLE.*?`(\w+)`', content, re.IGNORECASE)
    for table in tables:
        print(f"  - {table}")
    
    print("\n" + "=" * 60)
    print("STRUCTURE DES TABLES:")
    print("=" * 60)
    
    # Afficher les 200 premières lignes
    for line in lines[:200]:
        print(line, end='')

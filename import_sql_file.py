import pymysql

print("🔧 IMPORTATION DU FICHIER SQL DANS MYSQL")
print("="*80)

# Configuration
sql_file = r"C:\Users\MSI\Desktop\goback\gobagma_boutique_valises_maroc (1).sql"
temp_db_name = "gobagma_boutique_valises_maroc"

print(f"\nFichier SQL: {sql_file}")
print(f"Base de données temporaire: {temp_db_name}")

try:
    # Connexion à MySQL
    print("\n📡 Connexion à MySQL...")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    
    # Créer la base de données temporaire
    print(f"\n📊 Création de la base de données {temp_db_name}...")
    cursor.execute(f"DROP DATABASE IF EXISTS {temp_db_name}")
    cursor.execute(f"CREATE DATABASE {temp_db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE {temp_db_name}")
    print(f"✓ Base de données {temp_db_name} créée")
    
    # Lire et exécuter le fichier SQL
    print(f"\n📥 Importation du fichier SQL...")
    print("   (Cela peut prendre quelques minutes pour un gros fichier...)")
    
    with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
        sql_content = f.read()
    
    # Diviser en requêtes (approximatif)
    statements = []
    current_statement = []
    
    for line in sql_content.split('\n'):
        # Ignorer les commentaires
        if line.strip().startswith('--') or line.strip().startswith('/*') or line.strip() == '':
            continue
        
        current_statement.append(line)
        
        # Si la ligne se termine par ;, c'est la fin d'une requête
        if line.strip().endswith(';'):
            statement = '\n'.join(current_statement)
            if statement.strip():
                statements.append(statement)
            current_statement = []
    
    print(f"   Nombre de requêtes à exécuter: {len(statements)}")
    
    # Exécuter les requêtes par batch
    executed = 0
    errors = 0
    
    for i, statement in enumerate(statements):
        try:
            cursor.execute(statement)
            executed += 1
            
            if (i + 1) % 100 == 0:
                print(f"   Progression: {i + 1}/{len(statements)} requêtes...")
                connection.commit()
        except Exception as e:
            errors += 1
            if 'CREATE DATABASE' not in statement and 'USE ' not in statement:
                # Afficher seulement les premières erreurs
                if errors <= 5:
                    print(f"   ⚠ Erreur requête {i + 1}: {str(e)[:100]}")
    
    connection.commit()
    
    # Statistiques
    print(f"\n📊 STATISTIQUES:")
    print(f"   ✓ Requêtes exécutées: {executed}")
    print(f"   ⚠ Erreurs: {errors}")
    
    # Lister les tables créées
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📋 TABLES CRÉÉES ({len(tables)}):")
    for table in tables[:20]:  # Afficher les 20 premières
        cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`")
        count = cursor.fetchone()[0]
        print(f"   • {table[0]}: {count} lignes")
    
    if len(tables) > 20:
        print(f"   ... et {len(tables) - 20} autres tables")
    
    cursor.close()
    connection.close()
    
    print(f"\n✅ IMPORTATION TERMINÉE!")
    print(f"\nLa base de données '{temp_db_name}' est prête.")
    print(f"Vous pouvez maintenant exécuter: python import_from_old_sql.py")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

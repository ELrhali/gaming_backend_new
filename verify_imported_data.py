import pymysql

print("📊 VÉRIFICATION DES DONNÉES IMPORTÉES")
print("="*80)

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='gobagma_boutique_valises_maroc',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    
    # Vérifier les types (futures catégories)
    print("\n📁 TYPES (futures Catégories):")
    print("-"*80)
    cursor.execute("""
        SELECT id, nom, is_active 
        FROM types 
        WHERE deleted_at IS NULL 
        ORDER BY id
    """)
    types = cursor.fetchall()
    for t in types:
        print(f"  [{t['id']}] {t['nom']} (actif: {bool(t['is_active'])})")
    
    # Vérifier les categories (futures sous-catégories)
    print(f"\n📂 CATEGORIES (futures Sous-Catégories): {len(cursor.fetchall()) if cursor.execute('SELECT COUNT(*) FROM categories WHERE deleted_at IS NULL') else 0}")
    print("-"*80)
    cursor.execute("""
        SELECT c.id, c.nom, c.type_id, t.nom as type_nom
        FROM categories c
        LEFT JOIN types t ON c.type_id = t.id
        WHERE c.deleted_at IS NULL
        ORDER BY c.type_id, c.id
        LIMIT 20
    """)
    categories = cursor.fetchall()
    current_type = None
    for c in categories:
        if c['type_nom'] != current_type:
            current_type = c['type_nom']
            print(f"\n  Type: {current_type}")
        print(f"    [{c['id']}] {c['nom']}")
    
    # Vérifier les marques
    print(f"\n📦 MARQUES:")
    print("-"*80)
    cursor.execute("""
        SELECT id, nom, is_active
        FROM marques
        WHERE deleted_at IS NULL
        ORDER BY nom
    """)
    marques = cursor.fetchall()
    for m in marques:
        print(f"  [{m['id']}] {m['nom']} (actif: {bool(m['is_active'])})")
    
    # Vérifier les produits
    print(f"\n📦 PRODUITS (échantillon):")
    print("-"*80)
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM produits
        WHERE deleted_at IS NULL
    """)
    total = cursor.fetchone()['total']
    print(f"  Total: {total} produits")
    
    cursor.execute("""
        SELECT p.id, p.nom, p.prix, m.nom as marque
        FROM produits p
        LEFT JOIN marques m ON p.marque_id = m.id
        WHERE p.deleted_at IS NULL AND p.is_active = 1
        ORDER BY p.id
        LIMIT 10
    """)
    produits = cursor.fetchall()
    for p in produits:
        marque = p['marque'] if p['marque'] else 'Sans marque'
        prix = f"{float(p['prix']):.2f} DH" if p['prix'] else 'N/A'
        print(f"  [{p['id']}] {p['nom']} - {prix} ({marque})")
    
    # Vérifier les relations produit-catégorie
    print(f"\n🔗 RELATIONS PRODUIT-CATÉGORIE:")
    print("-"*80)
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM produit_categories
        WHERE deleted_at IS NULL
    """)
    total_relations = cursor.fetchone()['total']
    print(f"  Total: {total_relations} relations produit-catégorie")
    
    cursor.execute("""
        SELECT p.nom as produit, c.nom as categorie
        FROM produit_categories pc
        JOIN produits p ON pc.produit_id = p.id
        JOIN categories c ON pc.categorie_id = c.id
        WHERE pc.deleted_at IS NULL
        LIMIT 10
    """)
    relations = cursor.fetchall()
    for r in relations:
        print(f"  • {r['produit']} → {r['categorie']}")
    
    cursor.close()
    connection.close()
    
    print("\n" + "="*80)
    print("✅ VÉRIFICATION TERMINÉE")
    print("="*80)
    print("\nRésumé:")
    print(f"  • {len(types)} types (catégories)")
    print(f"  • {len(categories)} catégories actives (sous-catégories)")
    print(f"  • {len(marques)} marques")
    print(f"  • {total} produits")
    print(f"  • {total_relations} relations")
    print("\n✓ Prêt pour l'importation Django!")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

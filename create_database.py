import pymysql

# Configuration de connexion
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}

try:
    # Connexion au serveur MySQL
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    # Créer la base de données
    cursor.execute("CREATE DATABASE IF NOT EXISTS goback CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Base de données 'goback' créée avec succès!")
    
    # Vérifier la création
    cursor.execute("SHOW DATABASES LIKE 'goback'")
    result = cursor.fetchone()
    if result:
        print(f"✓ Base de données confirmée: {result[0]}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"✗ Erreur: {e}")

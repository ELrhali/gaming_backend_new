"""
Script pour tester les APIs utilisées par le frontend
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_categories():
    print("=" * 80)
    print("TEST API CATÉGORIES")
    print("=" * 80)
    
    response = requests.get(f'{BASE_URL}/categories/')
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        categories = data if isinstance(data, list) else data.get('results', [])
        
        print(f"✅ Catégories retournées: {len(categories)}")
        for cat in categories:
            print(f"\n📁 {cat['name']} (id={cat['id']}, slug={cat['slug']})")
            subcats = cat.get('subcategories', [])
            print(f"   Sous-catégories: {len(subcats)}")
            for sub in subcats[:3]:
                print(f"   - {sub['name']}")
            if len(subcats) > 3:
                print(f"   ... et {len(subcats) - 3} autres")
    else:
        print(f"❌ Erreur: {response.status_code}")

def test_subcategories():
    print("\n" + "=" * 80)
    print("TEST API SOUS-CATÉGORIES")
    print("=" * 80)
    
    response = requests.get(f'{BASE_URL}/subcategories/')
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        subcategories = data if isinstance(data, list) else data.get('results', [])
        
        print(f"✅ Sous-catégories retournées: {len(subcategories)}")
        
        # Grouper par catégorie
        by_category = {}
        for sub in subcategories:
            cat_id = sub.get('category')
            cat_name = sub.get('category_name', f'Catégorie {cat_id}')
            if cat_name not in by_category:
                by_category[cat_name] = []
            by_category[cat_name].append(sub)
        
        for cat_name, subs in by_category.items():
            print(f"\n📂 {cat_name}: {len(subs)} sous-catégories")
            for sub in subs:
                print(f"   - {sub['name']} (id={sub['id']}, slug={sub['slug']})")
    else:
        print(f"❌ Erreur: {response.status_code}")

def test_types():
    print("\n" + "=" * 80)
    print("TEST API TYPES")
    print("=" * 80)
    
    response = requests.get(f'{BASE_URL}/types/')
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        types = data if isinstance(data, list) else data.get('results', [])
        
        print(f"✅ Types retournés: {len(types)}")
        
        # Grouper par sous-catégorie
        by_subcategory = {}
        for typ in types:
            subcat_id = typ.get('subcategory')
            subcat_name = typ.get('subcategory_name', f'Sous-catégorie {subcat_id}')
            if subcat_name not in by_subcategory:
                by_subcategory[subcat_name] = []
            by_subcategory[subcat_name].append(typ)
        
        print(f"\nTypes groupés par sous-catégorie:")
        for subcat_name, typs in sorted(by_subcategory.items()):
            print(f"\n🔧 {subcat_name}: {len(typs)} types")
            for typ in typs[:5]:
                print(f"   - {typ['name']} (id={typ['id']})")
            if len(typs) > 5:
                print(f"   ... et {len(typs) - 5} autres")
    else:
        print(f"❌ Erreur: {response.status_code}")

def test_frontend_data():
    print("\n" + "=" * 80)
    print("SIMULATION CHARGEMENT FRONTEND")
    print("=" * 80)
    
    # Ce que le frontend fait
    print("\n1️⃣ Chargement des catégories...")
    cats_response = requests.get(f'{BASE_URL}/categories/')
    categories = cats_response.json() if isinstance(cats_response.json(), list) else cats_response.json().get('results', [])
    print(f"   ✅ {len(categories)} catégories chargées")
    
    print("\n2️⃣ Chargement des sous-catégories...")
    subs_response = requests.get(f'{BASE_URL}/subcategories/')
    subcategories = subs_response.json() if isinstance(subs_response.json(), list) else subs_response.json().get('results', [])
    print(f"   ✅ {len(subcategories)} sous-catégories chargées")
    
    print("\n3️⃣ Chargement des types...")
    types_response = requests.get(f'{BASE_URL}/types/')
    types = types_response.json() if isinstance(types_response.json(), list) else types_response.json().get('results', [])
    print(f"   ✅ {len(types)} types chargés")
    
    print("\n4️⃣ Simulation du dropdown pour chaque catégorie:")
    for cat in categories:
        print(f"\n📁 {cat['name']}")
        
        # Filtrer les sous-catégories de cette catégorie
        cat_subs = [s for s in subcategories if s.get('category') == cat['id']]
        print(f"   Sous-catégories: {len(cat_subs)}")
        
        for sub in cat_subs:
            # Filtrer les types de cette sous-catégorie
            sub_types = [t for t in types if t.get('subcategory') == sub['id']]
            print(f"   - {sub['name']}: {len(sub_types)} types")
            for typ in sub_types[:3]:
                print(f"     • {typ['name']}")

if __name__ == '__main__':
    try:
        test_categories()
        test_subcategories()
        test_types()
        test_frontend_data()
        
        print("\n" + "=" * 80)
        print("✅ TESTS TERMINÉS")
        print("=" * 80)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERREUR: Le serveur Django n'est pas démarré!")
        print("Lancez: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")

"""
Script de test pour vérifier l'API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(name, url):
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"URL: {url}")
    print('='*60)
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Résultats: {len(data)} éléments")
                if len(data) > 0:
                    print(f"Premier élément: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
            else:
                print(f"Données: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == '__main__':
    # Test des endpoints principaux
    test_endpoint("Catégories", f"{BASE_URL}/categories/")
    test_endpoint("Sous-catégories Homepage", f"{BASE_URL}/subcategories/homepage/")
    test_endpoint("Produits Bestsellers", f"{BASE_URL}/products/bestsellers/?limit=6")
    test_endpoint("Produits par sous-catégorie", f"{BASE_URL}/products/by_subcategory/?subcategory=processeurs&limit=4")
    
    print(f"\n{'='*60}")
    print("Tests terminés!")
    print('='*60)

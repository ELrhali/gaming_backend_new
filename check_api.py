import requests
import json

response = requests.get('http://127.0.0.1:8000/api/hero-slides/')
data = response.json()['results']

print("Ordre des slides dans l'API:")
print("=" * 80)
for i, s in enumerate(data):
    title = s['title'] if s['title'] else '(sans titre)'
    print(f"{i+1}. ID {s['id']}: {title}")
    print(f"   Link: {s['link']}")
    print(f"   Order: {s['order']}")
    print("-" * 80)

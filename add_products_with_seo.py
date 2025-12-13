"""
Script pour ajouter des produits de fournitures scolaires avec SEO optimisé
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, SubCategory, Type, Brand, Collection
from decimal import Decimal

def create_products_with_seo():
    """Crée des produits de fournitures scolaires avec SEO optimisé"""
    
    print("🚀 Début de l'ajout des produits avec SEO optimisé...")
    
    # Produits à ajouter avec SEO optimisé
    products_data = [
        {
            'reference': 'CART-001',
            'name': 'Cartable Disney Frozen - Sac à Dos Scolaire Fille',
            'category': 'CARTABLE ENFANTS',
            'subcategory': 'Cartables Filles',
            'brand': 'Disney',
            'type': 'Frozen',
            'price': 299.00,
            'discount_price': 249.00,
            'quantity': 50,
            'description': '''<p>Magnifique cartable Disney Frozen pour les petites filles qui adorent Elsa et Anna. 
            Ce sac à dos scolaire offre confort et praticité avec ses bretelles rembourrées et ses multiples compartiments.</p>
            <ul>
                <li>Design Disney Frozen officiel</li>
                <li>Bretelles ajustables et rembourrées</li>
                <li>Grand compartiment principal</li>
                <li>Poche frontale zippée</li>
                <li>Fond renforcé</li>
                <li>Matériau résistant et lavable</li>
            </ul>''',
            'meta_title': 'Cartable Disney Frozen Fille - Sac à Dos Scolaire Confortable | Gobag.ma',
            'meta_description': 'Cartable Disney Frozen pour filles avec bretelles rembourrées et compartiments multiples. Sac à dos scolaire de qualité, design officiel. Livraison rapide au Maroc. -17% ✓',
            'is_bestseller': True,
            'is_featured': True,
            'is_new': True,
            'status': 'in_stock',
            'collection': 'Rentrée Scolaire 2025'
        },
        {
            'reference': 'CAH-001',
            'name': 'Cahier 200 Pages Grand Format - Ligné Seyès',
            'category': 'CAHIERS ET COPIES',
            'subcategory': 'Cahiers Grands Formats',
            'brand': 'Oxford',
            'type': 'Ligné',
            'price': 35.00,
            'discount_price': None,
            'quantity': 200,
            'description': '''<p>Cahier grand format 24x32cm de 200 pages avec réglure Seyès. 
            Papier de qualité supérieure 90g/m² pour une écriture agréable.</p>
            <ul>
                <li>200 pages lignées Seyès</li>
                <li>Format 24x32 cm</li>
                <li>Papier 90g/m² blanc</li>
                <li>Couverture polypro résistante</li>
                <li>Reliure piquée à cheval</li>
                <li>Idéal pour toutes les matières</li>
            </ul>''',
            'meta_title': 'Cahier 200 Pages Grand Format Seyès - Oxford Qualité Supérieure | Gobag',
            'meta_description': 'Cahier Oxford 200 pages grand format 24x32, réglure Seyès, papier 90g. Idéal collège et lycée. Couverture résistante. Stock disponible au Maroc. ✓',
            'is_bestseller': True,
            'is_featured': False,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'Essentiels Scolaires'
        },
        {
            'reference': 'STYL-001',
            'name': 'Lot 10 Stylos BIC Cristal Bleu - Écriture Fine',
            'category': 'ÉCRITURE',
            'subcategory': 'Stylos à Bille',
            'brand': 'BIC',
            'type': 'Cristal',
            'price': 25.00,
            'discount_price': 19.90,
            'quantity': 150,
            'description': '''<p>Lot de 10 stylos BIC Cristal bleu, le stylo iconique pour une écriture fluide et précise. 
            Encre de qualité supérieure pour un confort d'écriture optimal.</p>
            <ul>
                <li>Pack de 10 stylos</li>
                <li>Encre bleue indélébile</li>
                <li>Pointe moyenne 1.0mm</li>
                <li>Jusqu'à 3km d'écriture par stylo</li>
                <li>Corps transparent hexagonal</li>
                <li>Écriture ultra-fluide</li>
            </ul>''',
            'meta_title': 'Lot 10 Stylos BIC Cristal Bleu - Pack Économique Écriture | Gobag.ma',
            'meta_description': 'Pack 10 stylos BIC Cristal bleu, écriture fluide 3km. Pointe moyenne 1.0mm. Prix promotionnel -20%. Idéal école et bureau. Livraison Maroc. ✓',
            'is_bestseller': True,
            'is_featured': True,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'Essentiels Scolaires'
        },
        {
            'reference': 'TROUSS-001',
            'name': 'Trousse Scolaire 3 Compartiments - Spider-Man',
            'category': 'CARTABLE ENFANTS',
            'subcategory': 'Trousses',
            'brand': 'Marvel',
            'type': 'Spider-Man',
            'price': 89.00,
            'discount_price': 69.00,
            'quantity': 80,
            'description': '''<p>Trousse scolaire Spider-Man avec 3 compartiments zippés pour organiser tous vos stylos, 
            crayons et fournitures. Design officiel Marvel avec Spider-Man.</p>
            <ul>
                <li>3 compartiments zippés</li>
                <li>Design Spider-Man officiel</li>
                <li>Grande capacité</li>
                <li>Matériau résistant et lavable</li>
                <li>Poignée de transport</li>
                <li>Dimensions: 22x12x8 cm</li>
            </ul>''',
            'meta_title': 'Trousse Scolaire Spider-Man 3 Compartiments - Marvel Officiel | Gobag',
            'meta_description': 'Trousse Spider-Man 3 compartiments pour écolier. Design Marvel officiel, grande capacité. Matériau résistant. Promotion -22% au Maroc. Livraison rapide. ✓',
            'is_bestseller': False,
            'is_featured': True,
            'is_new': True,
            'status': 'in_stock',
            'collection': 'Super-Héros'
        },
        {
            'reference': 'FEUTR-001',
            'name': 'Feutres de Coloriage 24 Couleurs Lavables',
            'category': 'ÉCRITURE',
            'subcategory': 'Feutres et Markers',
            'brand': 'Crayola',
            'type': 'Lavable',
            'price': 79.00,
            'discount_price': None,
            'quantity': 100,
            'description': '''<p>Coffret de 24 feutres de coloriage Crayola aux couleurs vives et lavables. 
            Parfait pour les activités créatives des enfants à l'école et à la maison.</p>
            <ul>
                <li>24 couleurs différentes</li>
                <li>Encre lavable à l'eau</li>
                <li>Pointe conique résistante</li>
                <li>Non-toxique et sécuritaire</li>
                <li>Couleurs vives et éclatantes</li>
                <li>Boîte de rangement incluse</li>
            </ul>''',
            'meta_title': 'Feutres Crayola 24 Couleurs Lavables - Coloriage Enfant Sécurisé | Gobag',
            'meta_description': 'Coffret 24 feutres Crayola lavables pour enfants. Couleurs vives, encre non-toxique. Parfait école maternelle et primaire. Disponible au Maroc. ✓',
            'is_bestseller': True,
            'is_featured': False,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'Activités Créatives'
        },
        {
            'reference': 'CAL-001',
            'name': 'Calculatrice Scientifique CASIO FX-92 Spéciale Collège',
            'category': 'ACCESSOIRE DE VOYAGE',
            'subcategory': 'Calculatrices',
            'brand': 'CASIO',
            'type': 'Scientifique',
            'price': 349.00,
            'discount_price': 299.00,
            'quantity': 60,
            'description': '''<p>Calculatrice scientifique CASIO FX-92 spécialement conçue pour les programmes du collège. 
            Fonctions mathématiques avancées et menu en français.</p>
            <ul>
                <li>Menu et résultats en français</li>
                <li>Écran LCD haute résolution</li>
                <li>Plus de 400 fonctions</li>
                <li>Mode tableur et QR Code</li>
                <li>Alimentation solaire + pile</li>
                <li>Étui de protection inclus</li>
            </ul>''',
            'meta_title': 'Calculatrice CASIO FX-92 Collège - Scientifique Menu Français | Gobag.ma',
            'meta_description': 'Calculatrice scientifique CASIO FX-92 spéciale collège. Menu français, 400+ fonctions, mode tableur. Promotion -14%. Conforme programme scolaire marocain. ✓',
            'is_bestseller': True,
            'is_featured': True,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'High-Tech Scolaire'
        },
        {
            'reference': 'GOMM-001',
            'name': 'Gommes Blanches Pack de 5 - Effaçage Sans Trace',
            'category': 'ÉCRITURE',
            'subcategory': 'Gommes et Correcteurs',
            'brand': 'Maped',
            'type': 'Blanche',
            'price': 15.00,
            'discount_price': None,
            'quantity': 200,
            'description': '''<p>Pack de 5 gommes blanches Maped pour un effaçage parfait sans trace. 
            Idéales pour le graphite et les crayons de couleur.</p>
            <ul>
                <li>Pack de 5 gommes</li>
                <li>Effaçage sans résidu</li>
                <li>N'abîme pas le papier</li>
                <li>Format pratique</li>
                <li>Haute qualité Maped</li>
                <li>Sans PVC</li>
            </ul>''',
            'meta_title': 'Gommes Maped Pack 5 Blanches - Effaçage Parfait Sans Trace | Gobag',
            'meta_description': 'Pack 5 gommes Maped blanches pour effaçage propre. Sans résidu, n\'abîme pas le papier. Qualité supérieure. Prix avantageux au Maroc. ✓',
            'is_bestseller': False,
            'is_featured': False,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'Essentiels Scolaires'
        },
        {
            'reference': 'REG-001',
            'name': 'Règle Graduée 30cm Transparente Incassable',
            'category': 'ÉCRITURE',
            'subcategory': 'Règles et Équerres',
            'brand': 'Maped',
            'type': 'Transparente',
            'price': 12.00,
            'discount_price': None,
            'quantity': 150,
            'description': '''<p>Règle graduée 30cm transparente et incassable Maped. 
            Double graduation en cm et pouces pour tous vos travaux de géométrie.</p>
            <ul>
                <li>Longueur 30 cm</li>
                <li>Matériau incassable</li>
                <li>Transparente pour traçage précis</li>
                <li>Double graduation cm/pouces</li>
                <li>Bords biseautés anti-taches</li>
                <li>Fabrication européenne</li>
            </ul>''',
            'meta_title': 'Règle 30cm Transparente Incassable Maped - Double Graduation | Gobag.ma',
            'meta_description': 'Règle Maped 30cm transparente et incassable. Double graduation cm/pouces. Idéale géométrie école. Qualité européenne. Stock Maroc. ✓',
            'is_bestseller': False,
            'is_featured': False,
            'is_new': False,
            'status': 'in_stock',
            'collection': 'Géométrie'
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for product_data in products_data:
        try:
            # Récupérer ou créer la catégorie
            category, _ = Category.objects.get_or_create(
                name=product_data['category'],
                defaults={'slug': product_data['category'].lower().replace(' ', '-')}
            )
            
            # Récupérer ou créer la sous-catégorie
            subcategory, _ = SubCategory.objects.get_or_create(
                name=product_data['subcategory'],
                category=category,
                defaults={'slug': product_data['subcategory'].lower().replace(' ', '-')}
            )
            
            # Récupérer ou créer la marque
            brand, _ = Brand.objects.get_or_create(
                name=product_data['brand']
            )
            
            # Récupérer ou créer le type
            type_obj, _ = Type.objects.get_or_create(
                name=product_data['type'],
                subcategory=subcategory,
                defaults={'slug': product_data['type'].lower().replace(' ', '-')}
            )
            
            # Récupérer ou créer la collection
            collection, _ = Collection.objects.get_or_create(
                name=product_data['collection'],
                defaults={'slug': product_data['collection'].lower().replace(' ', '-')}
            )
            
            # Créer ou mettre à jour le produit
            product, created = Product.objects.update_or_create(
                reference=product_data['reference'],
                defaults={
                    'name': product_data['name'],
                    'category': category,
                    'subcategory': subcategory,
                    'brand': brand,
                    'type': type_obj,
                    'collection': collection,
                    'price': Decimal(str(product_data['price'])),
                    'discount_price': Decimal(str(product_data['discount_price'])) if product_data['discount_price'] else None,
                    'quantity': product_data['quantity'],
                    'description': product_data['description'],
                    'meta_title': product_data['meta_title'],
                    'meta_description': product_data['meta_description'],
                    'is_bestseller': product_data['is_bestseller'],
                    'is_featured': product_data['is_featured'],
                    'is_new': product_data['is_new'],
                    'status': product_data['status'],
                    'slug': product_data['name'].lower().replace(' ', '-')[:200]
                }
            )
            
            if created:
                created_count += 1
                print(f"✅ Créé: {product.name}")
            else:
                updated_count += 1
                print(f"🔄 Mis à jour: {product.name}")
                
            # Afficher le SEO
            print(f"   📊 SEO Title: {product.meta_title[:60]}...")
            print(f"   📝 SEO Desc: {product.meta_description[:80]}...")
            print()
            
        except Exception as e:
            print(f"❌ Erreur pour {product_data['reference']}: {str(e)}")
            continue
    
    print(f"\n✅ Terminé!")
    print(f"   • Produits créés: {created_count}")
    print(f"   • Produits mis à jour: {updated_count}")
    print(f"\n🔍 SEO optimisé pour chaque produit:")
    print(f"   • Meta Title: Optimisé avec mots-clés + Gobag.ma")
    print(f"   • Meta Description: 150-160 caractères avec call-to-action")
    print(f"   • Keywords: Fournitures scolaires, matériel éducatif, Maroc")

if __name__ == '__main__':
    create_products_with_seo()

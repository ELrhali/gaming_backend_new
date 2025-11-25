"""
Script pour peupler la base de données avec des données de test
Usage: python populate_db.py
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Category, SubCategory, Type, Product, ProductImage, ProductSpecification
from decimal import Decimal

def clear_database():
    """Supprime toutes les données existantes"""
    print("🗑️  Suppression des données existantes...")
    ProductSpecification.objects.all().delete()
    ProductImage.objects.all().delete()
    Product.objects.all().delete()
    Type.objects.all().delete()
    SubCategory.objects.all().delete()
    Category.objects.all().delete()
    print("✅ Données supprimées")

def create_categories():
    """Crée les catégories principales"""
    print("\n📁 Création des catégories...")
    
    categories_data = [
        {
            'name': 'COMPOSANT PC',
            'description': 'Tous les composants pour monter ou upgrader votre PC',
            'order': 1
        },
        {
            'name': 'PÉRIPHÉRIQUES PC',
            'description': 'Claviers, souris, écrans et accessoires gaming',
            'order': 2
        },
        {
            'name': 'Accessoires PC',
            'description': 'Câbles, refroidissement et accessoires divers',
            'order': 3
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat = Category.objects.create(**cat_data)
        categories[cat.name] = cat
        print(f"  ✓ {cat.name}")
    
    return categories

def create_subcategories(categories):
    """Crée les sous-catégories"""
    print("\n📂 Création des sous-catégories...")
    
    subcategories_data = [
        # COMPOSANT PC
        {'category': 'COMPOSANT PC', 'name': 'Processeurs', 'show_on_homepage': True, 'order': 1},
        {'category': 'COMPOSANT PC', 'name': 'Cartes Graphiques', 'show_on_homepage': True, 'order': 2},
        {'category': 'COMPOSANT PC', 'name': 'Cartes Mères', 'show_on_homepage': True, 'order': 3},
        {'category': 'COMPOSANT PC', 'name': 'Mémoire RAM', 'show_on_homepage': True, 'order': 4},
        {'category': 'COMPOSANT PC', 'name': 'Disques SSD', 'show_on_homepage': True, 'order': 5},
        {'category': 'COMPOSANT PC', 'name': 'Disques Durs', 'show_on_homepage': False, 'order': 6},
        {'category': 'COMPOSANT PC', 'name': 'Alimentations', 'show_on_homepage': True, 'order': 7},
        {'category': 'COMPOSANT PC', 'name': 'Boîtiers PC', 'show_on_homepage': False, 'order': 8},
        
        # PÉRIPHÉRIQUES PC
        {'category': 'PÉRIPHÉRIQUES PC', 'name': 'Écrans PC', 'show_on_homepage': True, 'order': 1},
        {'category': 'PÉRIPHÉRIQUES PC', 'name': 'Claviers Gaming', 'show_on_homepage': True, 'order': 2},
        {'category': 'PÉRIPHÉRIQUES PC', 'name': 'Souris Gaming', 'show_on_homepage': True, 'order': 3},
        {'category': 'PÉRIPHÉRIQUES PC', 'name': 'Casques Audio', 'show_on_homepage': True, 'order': 4},
        {'category': 'PÉRIPHÉRIQUES PC', 'name': 'Webcams', 'show_on_homepage': False, 'order': 5},
        
        # Accessoires PC
        {'category': 'Accessoires PC', 'name': 'Refroidissement', 'show_on_homepage': True, 'order': 1},
        {'category': 'Accessoires PC', 'name': 'Câbles et Adaptateurs', 'show_on_homepage': False, 'order': 2},
        {'category': 'Accessoires PC', 'name': 'Tapis de Souris', 'show_on_homepage': True, 'order': 3},
        {'category': 'Accessoires PC', 'name': 'Supports et Stands', 'show_on_homepage': False, 'order': 4},
    ]
    
    subcategories = {}
    for subcat_data in subcategories_data:
        cat_name = subcat_data.pop('category')
        subcat = SubCategory.objects.create(
            category=categories[cat_name],
            **subcat_data
        )
        subcategories[subcat.name] = subcat
        homepage = "🏠" if subcat.show_on_homepage else "  "
        print(f"  {homepage} ✓ {subcat.name} ({cat_name})")
    
    return subcategories

def create_types(subcategories):
    """Crée les types/marques"""
    print("\n🏷️  Création des types...")
    
    types_data = [
        # Processeurs
        {'subcategory': 'Processeurs', 'name': 'Intel Core i9', 'order': 1},
        {'subcategory': 'Processeurs', 'name': 'Intel Core i7', 'order': 2},
        {'subcategory': 'Processeurs', 'name': 'Intel Core i5', 'order': 3},
        {'subcategory': 'Processeurs', 'name': 'AMD Ryzen 9', 'order': 4},
        {'subcategory': 'Processeurs', 'name': 'AMD Ryzen 7', 'order': 5},
        {'subcategory': 'Processeurs', 'name': 'AMD Ryzen 5', 'order': 6},
        
        # Cartes Graphiques
        {'subcategory': 'Cartes Graphiques', 'name': 'NVIDIA RTX 4090', 'order': 1},
        {'subcategory': 'Cartes Graphiques', 'name': 'NVIDIA RTX 4080', 'order': 2},
        {'subcategory': 'Cartes Graphiques', 'name': 'NVIDIA RTX 4070', 'order': 3},
        {'subcategory': 'Cartes Graphiques', 'name': 'AMD Radeon RX 7900', 'order': 4},
        {'subcategory': 'Cartes Graphiques', 'name': 'AMD Radeon RX 7800', 'order': 5},
        
        # Cartes Mères
        {'subcategory': 'Cartes Mères', 'name': 'ASUS ROG', 'order': 1},
        {'subcategory': 'Cartes Mères', 'name': 'MSI Gaming', 'order': 2},
        {'subcategory': 'Cartes Mères', 'name': 'Gigabyte AORUS', 'order': 3},
        {'subcategory': 'Cartes Mères', 'name': 'ASRock', 'order': 4},
        
        # Mémoire RAM
        {'subcategory': 'Mémoire RAM', 'name': 'Corsair Vengeance', 'order': 1},
        {'subcategory': 'Mémoire RAM', 'name': 'G.Skill Trident', 'order': 2},
        {'subcategory': 'Mémoire RAM', 'name': 'Kingston Fury', 'order': 3},
    ]
    
    types = {}
    for type_data in types_data:
        subcat_name = type_data.pop('subcategory')
        type_obj = Type.objects.create(
            subcategory=subcategories[subcat_name],
            **type_data
        )
        types[type_obj.name] = type_obj
        print(f"  ✓ {type_obj.name}")
    
    return types

def create_products(subcategories, types):
    """Crée les produits"""
    print("\n🎮 Création des produits...")
    
    products_data = [
        # ========== PROCESSEURS ==========
        {
            'reference': 'CPU-001',
            'name': 'Intel Core i9-14900K Processeur Gaming',
            'description': 'Processeur haute performance avec 24 cœurs (8P + 16E) et 32 threads. Fréquence turbo jusqu\'à 6.0 GHz. Architecture Raptor Lake Refresh optimisée pour le gaming et les applications professionnelles.',
            'subcategory': 'Processeurs',
            'type': 'Intel Core i9',
            'price': Decimal('5499.00'),
            'discount_price': Decimal('4999.00'),
            'quantity': 15,
            'is_bestseller': True,
            'is_new': True,
            'brand': 'Intel',
            'warranty': '3 ans',
            'specs': [
                ('Nombre de cœurs', '24 (8P + 16E)'),
                ('Nombre de threads', '32'),
                ('Fréquence de base', '3.2 GHz'),
                ('Fréquence turbo max', '6.0 GHz'),
                ('Cache', '36 MB L3'),
                ('Socket', 'LGA 1700'),
                ('TDP', '125W'),
            ]
        },
        {
            'reference': 'CPU-002',
            'name': 'AMD Ryzen 9 7950X3D Processeur Gaming',
            'description': 'Processeur ultime pour les gamers avec technologie 3D V-Cache. 16 cœurs, 32 threads et jusqu\'à 5.7 GHz. Performance exceptionnelle en gaming et création de contenu.',
            'subcategory': 'Processeurs',
            'type': 'AMD Ryzen 9',
            'price': Decimal('6299.00'),
            'discount_price': Decimal('5799.00'),
            'quantity': 10,
            'is_bestseller': True,
            'is_featured': True,
            'brand': 'AMD',
            'warranty': '3 ans',
            'specs': [
                ('Nombre de cœurs', '16'),
                ('Nombre de threads', '32'),
                ('Fréquence de base', '4.2 GHz'),
                ('Fréquence turbo max', '5.7 GHz'),
                ('Cache', '128 MB (3D V-Cache)'),
                ('Socket', 'AM5'),
                ('TDP', '120W'),
            ]
        },
        {
            'reference': 'CPU-003',
            'name': 'Intel Core i7-14700K Processeur',
            'description': 'Excellent rapport performance/prix. 20 cœurs (8P + 12E), 28 threads, jusqu\'à 5.6 GHz. Parfait pour le gaming et le multitâche.',
            'subcategory': 'Processeurs',
            'type': 'Intel Core i7',
            'price': Decimal('4299.00'),
            'quantity': 25,
            'is_bestseller': True,
            'brand': 'Intel',
            'warranty': '3 ans',
            'specs': [
                ('Nombre de cœurs', '20 (8P + 12E)'),
                ('Nombre de threads', '28'),
                ('Fréquence turbo max', '5.6 GHz'),
                ('Socket', 'LGA 1700'),
            ]
        },
        {
            'reference': 'CPU-004',
            'name': 'AMD Ryzen 7 7800X3D Processeur Gaming',
            'description': 'Le meilleur processeur pour le gaming pur. 8 cœurs, 16 threads avec 3D V-Cache. Performance gaming inégalée à ce prix.',
            'subcategory': 'Processeurs',
            'type': 'AMD Ryzen 7',
            'price': Decimal('3999.00'),
            'discount_price': Decimal('3699.00'),
            'quantity': 30,
            'is_bestseller': True,
            'is_featured': True,
            'brand': 'AMD',
            'warranty': '3 ans',
            'specs': [
                ('Nombre de cœurs', '8'),
                ('Nombre de threads', '16'),
                ('Fréquence turbo max', '5.0 GHz'),
                ('Cache', '96 MB (3D V-Cache)'),
                ('Socket', 'AM5'),
            ]
        },
        
        # ========== CARTES GRAPHIQUES ==========
        {
            'reference': 'GPU-001',
            'name': 'NVIDIA GeForce RTX 4090 MSI Gaming X Trio 24GB',
            'description': 'La carte graphique la plus puissante du marché. Architecture Ada Lovelace, 24GB GDDR6X, Ray Tracing 3ème génération, DLSS 3.0. Performance 4K ultime.',
            'subcategory': 'Cartes Graphiques',
            'type': 'NVIDIA RTX 4090',
            'price': Decimal('19999.00'),
            'discount_price': Decimal('18499.00'),
            'quantity': 5,
            'is_bestseller': True,
            'is_featured': True,
            'is_new': True,
            'brand': 'MSI',
            'warranty': '3 ans',
            'specs': [
                ('GPU', 'NVIDIA GeForce RTX 4090'),
                ('Mémoire', '24 GB GDDR6X'),
                ('Interface mémoire', '384-bit'),
                ('Cœurs CUDA', '16384'),
                ('Fréquence Boost', '2610 MHz'),
                ('TDP', '450W'),
                ('Connecteurs', '3x DisplayPort 1.4a, 1x HDMI 2.1'),
            ]
        },
        {
            'reference': 'GPU-002',
            'name': 'NVIDIA GeForce RTX 4080 ASUS ROG Strix 16GB',
            'description': 'Performance 4K exceptionnelle. 16GB GDDR6X, refroidissement ROG Strix avancé. Parfaite pour le gaming haute résolution et la création.',
            'subcategory': 'Cartes Graphiques',
            'type': 'NVIDIA RTX 4080',
            'price': Decimal('13999.00'),
            'discount_price': Decimal('12999.00'),
            'quantity': 8,
            'is_bestseller': True,
            'brand': 'ASUS',
            'warranty': '3 ans',
            'specs': [
                ('GPU', 'NVIDIA GeForce RTX 4080'),
                ('Mémoire', '16 GB GDDR6X'),
                ('Cœurs CUDA', '9728'),
                ('Fréquence Boost', '2565 MHz'),
            ]
        },
        {
            'reference': 'GPU-003',
            'name': 'NVIDIA GeForce RTX 4070 Ti Gigabyte Gaming OC 12GB',
            'description': 'Excellent choix pour le 1440p et 4K. 12GB GDDR6X, performance impressionnante, consommation maîtrisée.',
            'subcategory': 'Cartes Graphiques',
            'type': 'NVIDIA RTX 4070',
            'price': Decimal('8999.00'),
            'quantity': 12,
            'is_bestseller': True,
            'brand': 'Gigabyte',
            'warranty': '3 ans',
            'specs': [
                ('GPU', 'NVIDIA GeForce RTX 4070 Ti'),
                ('Mémoire', '12 GB GDDR6X'),
                ('Cœurs CUDA', '7680'),
            ]
        },
        {
            'reference': 'GPU-004',
            'name': 'AMD Radeon RX 7900 XTX Sapphire Nitro+ 24GB',
            'description': 'Carte graphique AMD haut de gamme. 24GB GDDR6, architecture RDNA 3. Excellente alternative à la RTX 4080.',
            'subcategory': 'Cartes Graphiques',
            'type': 'AMD Radeon RX 7900',
            'price': Decimal('11999.00'),
            'discount_price': Decimal('10999.00'),
            'quantity': 10,
            'is_featured': True,
            'brand': 'Sapphire',
            'warranty': '3 ans',
            'specs': [
                ('GPU', 'AMD Radeon RX 7900 XTX'),
                ('Mémoire', '24 GB GDDR6'),
                ('Stream Processors', '6144'),
            ]
        },
        
        # ========== CARTES MÈRES ==========
        {
            'reference': 'MB-001',
            'name': 'ASUS ROG MAXIMUS Z790 HERO ATX',
            'description': 'Carte mère premium pour Intel 13/14ème génération. Socket LGA1700, DDR5, PCIe 5.0, WiFi 6E, RGB Aura Sync.',
            'subcategory': 'Cartes Mères',
            'type': 'ASUS ROG',
            'price': Decimal('4999.00'),
            'discount_price': Decimal('4499.00'),
            'quantity': 8,
            'is_featured': True,
            'brand': 'ASUS',
            'warranty': '3 ans',
            'specs': [
                ('Format', 'ATX'),
                ('Socket', 'LGA 1700'),
                ('Chipset', 'Intel Z790'),
                ('Mémoire', 'DDR5 jusqu\'à 7800 MHz'),
                ('PCIe', '5.0 x16'),
                ('WiFi', '6E'),
            ]
        },
        {
            'reference': 'MB-002',
            'name': 'MSI MAG X670E TOMAHAWK WiFi ATX',
            'description': 'Carte mère AMD AM5 pour Ryzen 7000. DDR5, PCIe 5.0, excellent VRM pour overclocking.',
            'subcategory': 'Cartes Mères',
            'type': 'MSI Gaming',
            'price': Decimal('3299.00'),
            'quantity': 15,
            'is_bestseller': True,
            'brand': 'MSI',
            'warranty': '3 ans',
            'specs': [
                ('Format', 'ATX'),
                ('Socket', 'AM5'),
                ('Chipset', 'AMD X670E'),
                ('Mémoire', 'DDR5 jusqu\'à 6400 MHz'),
            ]
        },
        
        # ========== MÉMOIRE RAM ==========
        {
            'reference': 'RAM-001',
            'name': 'Corsair Vengeance DDR5 32GB (2x16GB) 6000MHz RGB',
            'description': 'Kit mémoire DDR5 haute performance. 32GB (2x16GB), 6000MHz, latence CL36, RGB iCUE compatible.',
            'subcategory': 'Mémoire RAM',
            'type': 'Corsair Vengeance',
            'price': Decimal('1499.00'),
            'discount_price': Decimal('1299.00'),
            'quantity': 50,
            'is_bestseller': True,
            'brand': 'Corsair',
            'warranty': 'Lifetime',
            'specs': [
                ('Capacité', '32 GB (2x16GB)'),
                ('Type', 'DDR5'),
                ('Fréquence', '6000 MHz'),
                ('Latence', 'CL36'),
                ('RGB', 'Oui'),
            ]
        },
        {
            'reference': 'RAM-002',
            'name': 'G.Skill Trident Z5 RGB DDR5 64GB (2x32GB) 6400MHz',
            'description': 'Kit mémoire premium 64GB. DDR5 6400MHz, parfait pour stations de travail et gaming extrême.',
            'subcategory': 'Mémoire RAM',
            'type': 'G.Skill Trident',
            'price': Decimal('2999.00'),
            'quantity': 20,
            'is_featured': True,
            'is_new': True,
            'brand': 'G.Skill',
            'warranty': 'Lifetime',
            'specs': [
                ('Capacité', '64 GB (2x32GB)'),
                ('Type', 'DDR5'),
                ('Fréquence', '6400 MHz'),
                ('Latence', 'CL32'),
            ]
        },
        
        # ========== DISQUES SSD ==========
        {
            'reference': 'SSD-001',
            'name': 'Samsung 990 PRO NVMe M.2 2TB PCIe 4.0',
            'description': 'SSD NVMe ultra-rapide. 2TB, jusqu\'à 7450 MB/s en lecture, 6900 MB/s en écriture. Idéal gaming et création.',
            'subcategory': 'Disques SSD',
            'price': Decimal('1799.00'),
            'discount_price': Decimal('1599.00'),
            'quantity': 35,
            'is_bestseller': True,
            'brand': 'Samsung',
            'warranty': '5 ans',
            'specs': [
                ('Capacité', '2 TB'),
                ('Interface', 'NVMe M.2 PCIe 4.0'),
                ('Lecture séquentielle', '7450 MB/s'),
                ('Écriture séquentielle', '6900 MB/s'),
            ]
        },
        {
            'reference': 'SSD-002',
            'name': 'WD Black SN850X NVMe 1TB PCIe 4.0',
            'description': 'SSD gaming haute performance. 1TB, vitesses jusqu\'à 7300 MB/s, Game Mode 2.0.',
            'subcategory': 'Disques SSD',
            'price': Decimal('999.00'),
            'quantity': 40,
            'is_bestseller': True,
            'brand': 'Western Digital',
            'warranty': '5 ans',
            'specs': [
                ('Capacité', '1 TB'),
                ('Interface', 'NVMe M.2 PCIe 4.0'),
                ('Lecture', 'jusqu\'à 7300 MB/s'),
            ]
        },
        
        # ========== ALIMENTATIONS ==========
        {
            'reference': 'PSU-001',
            'name': 'Corsair RM1000x 1000W 80+ Gold Modulaire',
            'description': 'Alimentation modulaire 1000W certifiée 80+ Gold. Silencieuse, efficace, câbles entièrement modulaires. Parfaite pour configs haut de gamme.',
            'subcategory': 'Alimentations',
            'price': Decimal('1899.00'),
            'discount_price': Decimal('1699.00'),
            'quantity': 15,
            'is_bestseller': True,
            'brand': 'Corsair',
            'warranty': '10 ans',
            'specs': [
                ('Puissance', '1000W'),
                ('Certification', '80+ Gold'),
                ('Type', 'Modulaire'),
                ('Ventilateur', '135mm'),
            ]
        },
        
        # ========== ÉCRANS PC ==========
        {
            'reference': 'MON-001',
            'name': 'ASUS ROG Swift PG27AQDM 27" OLED 240Hz QHD',
            'description': 'Écran gaming OLED ultime. 27", QHD (2560x1440), 240Hz, 0.03ms, G-SYNC, HDR, 99% DCI-P3. Experience visuelle exceptionnelle.',
            'subcategory': 'Écrans PC',
            'price': Decimal('9999.00'),
            'discount_price': Decimal('8999.00'),
            'quantity': 6,
            'is_featured': True,
            'is_new': True,
            'brand': 'ASUS',
            'warranty': '3 ans',
            'specs': [
                ('Taille', '27 pouces'),
                ('Résolution', '2560 x 1440 (QHD)'),
                ('Dalle', 'OLED'),
                ('Taux de rafraîchissement', '240 Hz'),
                ('Temps de réponse', '0.03 ms'),
                ('Technologie', 'G-SYNC Compatible'),
            ]
        },
        {
            'reference': 'MON-002',
            'name': 'Samsung Odyssey G7 32" Curved 240Hz QHD',
            'description': 'Écran gaming incurvé 1000R. 32", QHD, 240Hz, 1ms, HDR600, courbure immersive.',
            'subcategory': 'Écrans PC',
            'price': Decimal('4999.00'),
            'discount_price': Decimal('4499.00'),
            'quantity': 10,
            'is_bestseller': True,
            'brand': 'Samsung',
            'warranty': '3 ans',
            'specs': [
                ('Taille', '32 pouces'),
                ('Résolution', '2560 x 1440'),
                ('Courbure', '1000R'),
                ('Taux de rafraîchissement', '240 Hz'),
            ]
        },
        {
            'reference': 'MON-003',
            'name': 'LG UltraGear 27" IPS 165Hz Full HD',
            'description': 'Écran gaming abordable. 27", Full HD, IPS, 165Hz, 1ms, FreeSync Premium, excellent rapport qualité/prix.',
            'subcategory': 'Écrans PC',
            'price': Decimal('1999.00'),
            'quantity': 25,
            'is_bestseller': True,
            'brand': 'LG',
            'warranty': '2 ans',
            'specs': [
                ('Taille', '27 pouces'),
                ('Résolution', '1920 x 1080'),
                ('Dalle', 'IPS'),
                ('Taux de rafraîchissement', '165 Hz'),
            ]
        },
        
        # ========== CLAVIERS GAMING ==========
        {
            'reference': 'KB-001',
            'name': 'Corsair K100 RGB Clavier Mécanique Gaming',
            'description': 'Clavier gaming premium. Switchs Cherry MX Speed, roulette iCUE, repose-poignet magnétique, RGB dynamique.',
            'subcategory': 'Claviers Gaming',
            'price': Decimal('2299.00'),
            'discount_price': Decimal('1999.00'),
            'quantity': 12,
            'is_featured': True,
            'brand': 'Corsair',
            'warranty': '2 ans',
            'specs': [
                ('Type', 'Mécanique'),
                ('Switchs', 'Cherry MX Speed'),
                ('Rétroéclairage', 'RGB Per-Key'),
                ('Connectivité', 'USB + sans fil'),
            ]
        },
        {
            'reference': 'KB-002',
            'name': 'Logitech G915 TKL Clavier Sans Fil RGB',
            'description': 'Clavier gaming sans fil low-profile. Switchs GL Tactile, autonomie 40h, LIGHTSPEED, design compact TKL.',
            'subcategory': 'Claviers Gaming',
            'price': Decimal('1799.00'),
            'quantity': 18,
            'is_bestseller': True,
            'brand': 'Logitech',
            'warranty': '2 ans',
            'specs': [
                ('Type', 'Mécanique Low-Profile'),
                ('Switchs', 'GL Tactile'),
                ('Connectivité', 'Sans fil LIGHTSPEED'),
                ('Autonomie', '40 heures'),
            ]
        },
        
        # ========== SOURIS GAMING ==========
        {
            'reference': 'MS-001',
            'name': 'Logitech G Pro X Superlight 2 Souris Gaming',
            'description': 'Souris gaming ultra-légère. 60g, capteur HERO 2, 32000 DPI, autonomie 95h, sans fil LIGHTSPEED.',
            'subcategory': 'Souris Gaming',
            'price': Decimal('1499.00'),
            'discount_price': Decimal('1299.00'),
            'quantity': 30,
            'is_bestseller': True,
            'is_featured': True,
            'brand': 'Logitech',
            'warranty': '2 ans',
            'specs': [
                ('Poids', '60g'),
                ('Capteur', 'HERO 2'),
                ('DPI Max', '32000'),
                ('Autonomie', '95 heures'),
            ]
        },
        {
            'reference': 'MS-002',
            'name': 'Razer DeathAdder V3 Pro Souris Gaming',
            'description': 'Souris ergonomique sans fil. Capteur Focus Pro 30K, 63g, switches optiques Gen-3.',
            'subcategory': 'Souris Gaming',
            'price': Decimal('1399.00'),
            'quantity': 20,
            'is_bestseller': True,
            'brand': 'Razer',
            'warranty': '2 ans',
            'specs': [
                ('Capteur', 'Focus Pro 30K'),
                ('DPI Max', '30000'),
                ('Poids', '63g'),
            ]
        },
        
        # ========== CASQUES AUDIO ==========
        {
            'reference': 'HS-001',
            'name': 'SteelSeries Arctis Nova Pro Wireless Casque Gaming',
            'description': 'Casque gaming premium sans fil. Audio haute résolution, ANC, station d\'accueil, double batterie, compatible multi-plateformes.',
            'subcategory': 'Casques Audio',
            'price': Decimal('3999.00'),
            'discount_price': Decimal('3499.00'),
            'quantity': 8,
            'is_featured': True,
            'is_new': True,
            'brand': 'SteelSeries',
            'warranty': '2 ans',
            'specs': [
                ('Type', 'Sans fil'),
                ('Audio', 'Haute résolution'),
                ('ANC', 'Oui'),
                ('Autonomie', 'Double batterie'),
            ]
        },
        {
            'reference': 'HS-002',
            'name': 'HyperX Cloud III Casque Gaming',
            'description': 'Casque gaming confortable et abordable. Audio spatial DTS, micro antibruit, compatible PC/consoles.',
            'subcategory': 'Casques Audio',
            'price': Decimal('899.00'),
            'quantity': 25,
            'is_bestseller': True,
            'brand': 'HyperX',
            'warranty': '2 ans',
            'specs': [
                ('Type', 'Filaire'),
                ('Audio', 'DTS Spatial'),
                ('Micro', 'Antibruit'),
            ]
        },
        
        # ========== REFROIDISSEMENT ==========
        {
            'reference': 'COOL-001',
            'name': 'Corsair iCUE H150i Elite LCD Watercooling AIO 360mm',
            'description': 'Watercooling AIO premium. Radiateur 360mm, écran LCD personnalisable, RGB, silencieux, haute performance.',
            'subcategory': 'Refroidissement',
            'price': Decimal('2799.00'),
            'discount_price': Decimal('2499.00'),
            'quantity': 10,
            'is_featured': True,
            'brand': 'Corsair',
            'warranty': '5 ans',
            'specs': [
                ('Type', 'Watercooling AIO'),
                ('Taille radiateur', '360mm'),
                ('Écran', 'LCD 2.1"'),
                ('RGB', 'Oui'),
            ]
        },
        {
            'reference': 'COOL-002',
            'name': 'Noctua NH-D15 Ventirad CPU Air Cooling',
            'description': 'Le meilleur ventirad air du marché. Double ventilateur 140mm, ultra-silencieux, performance équivalente watercooling.',
            'subcategory': 'Refroidissement',
            'price': Decimal('999.00'),
            'quantity': 15,
            'is_bestseller': True,
            'brand': 'Noctua',
            'warranty': '6 ans',
            'specs': [
                ('Type', 'Air Cooling'),
                ('Ventilateurs', '2x 140mm'),
                ('Niveau sonore', '24.6 dB(A)'),
            ]
        },
        
        # ========== TAPIS DE SOURIS ==========
        {
            'reference': 'PAD-001',
            'name': 'Razer Goliathus Extended Chroma RGB Tapis de Souris',
            'description': 'Tapis de souris XXL avec RGB. 920x294mm, surface textile optimisée, éclairage Chroma RGB.',
            'subcategory': 'Tapis de Souris',
            'price': Decimal('499.00'),
            'discount_price': Decimal('399.00'),
            'quantity': 40,
            'is_bestseller': True,
            'brand': 'Razer',
            'warranty': '1 an',
            'specs': [
                ('Dimensions', '920 x 294 x 3 mm'),
                ('Surface', 'Textile micro-texturé'),
                ('RGB', 'Oui - Chroma'),
            ]
        },
    ]
    
    products = []
    for prod_data in products_data:
        # Extraire les specs
        specs = prod_data.pop('specs', [])
        
        # Récupérer la sous-catégorie et le type
        subcat_name = prod_data.pop('subcategory')
        type_name = prod_data.pop('type', None)
        
        # Créer le produit
        product = Product.objects.create(
            subcategory=subcategories[subcat_name],
            category=subcategories[subcat_name].category,
            type=types.get(type_name) if type_name else None,
            **prod_data
        )
        
        # Ajouter les spécifications
        for i, (key, value) in enumerate(specs):
            ProductSpecification.objects.create(
                product=product,
                key=key,
                value=value,
                order=i
            )
        
        products.append(product)
        price_display = f"{product.final_price} MAD"
        if product.discount_price:
            price_display += f" (↓ {product.discount_percentage}%)"
        
        badges = []
        if product.is_bestseller:
            badges.append("🔥")
        if product.is_new:
            badges.append("✨")
        if product.is_featured:
            badges.append("⭐")
        
        badge_str = " ".join(badges) if badges else ""
        print(f"  {badge_str} ✓ {product.reference} - {product.name[:50]}... | {price_display}")
    
    return products

def main():
    print("=" * 70)
    print("🎮 SCRIPT DE POPULATION DE LA BASE DE DONNÉES")
    print("=" * 70)
    
    # Demander confirmation
    response = input("\n⚠️  Ce script va SUPPRIMER toutes les données existantes. Continuer? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("❌ Annulé")
        return
    
    # Exécuter le peuplement
    clear_database()
    categories = create_categories()
    subcategories = create_subcategories(categories)
    types = create_types(subcategories)
    products = create_products(subcategories, types)
    
    # Résumé
    print("\n" + "=" * 70)
    print("✅ BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS!")
    print("=" * 70)
    print(f"📊 Statistiques:")
    print(f"  • Catégories: {Category.objects.count()}")
    print(f"  • Sous-catégories: {SubCategory.objects.count()}")
    print(f"  • Types: {Type.objects.count()}")
    print(f"  • Produits: {Product.objects.count()}")
    print(f"  • Spécifications: {ProductSpecification.objects.count()}")
    print("\n📝 Prochaines étapes:")
    print("  1. Créer un superuser: python manage.py createsuperuser")
    print("  2. Démarrer le serveur: python manage.py runserver")
    print("  3. Accéder à l'admin: http://localhost:8000/admin")
    print("  4. Ajouter des images aux produits via l'interface admin")
    print("=" * 70)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from orders.models import Order

print("=" * 60)
print("TEST DES FILTRES DE DATE")
print("=" * 60)

now = timezone.now()
print(f"\n⏰ Date actuelle: {now}")
print(f"⏰ Date actuelle (date only): {now.date()}")

# Test 1: Toutes les commandes
print("\n" + "=" * 60)
print("TEST 1: Toutes les commandes")
print("=" * 60)
all_orders = Order.objects.all()
print(f"Total commandes: {all_orders.count()}")
for order in all_orders:
    print(f"  Commande {order.id}: {order.created_at} (date: {order.created_at.date()})")

# Test 2: Cette semaine (7 jours)
print("\n" + "=" * 60)
print("TEST 2: Cette semaine (7 derniers jours)")
print("=" * 60)
date_from = (now - timedelta(days=7)).date()
date_to = now.date()
print(f"Date de début: {date_from}")
print(f"Date de fin: {date_to}")

# Méthode 1: Utiliser __date__gte/lte
print("\nMéthode 1 (avec __date__):")
orders_method1 = Order.objects.filter(
    created_at__date__gte=date_from,
    created_at__date__lte=date_to
)
print(f"Résultats: {orders_method1.count()}")

# Méthode 2: Convertir en datetime
print("\nMéthode 2 (avec datetime):")
datetime_from = timezone.make_aware(datetime.combine(date_from, datetime.min.time()))
datetime_to = timezone.make_aware(datetime.combine(date_to, datetime.max.time()))
print(f"Datetime de début: {datetime_from}")
print(f"Datetime de fin: {datetime_to}")
orders_method2 = Order.objects.filter(
    created_at__gte=datetime_from,
    created_at__lte=datetime_to
)
print(f"Résultats: {orders_method2.count()}")
for order in orders_method2:
    print(f"  Commande {order.id}: {order.created_at}")

# Test 3: Ce mois (30 jours)
print("\n" + "=" * 60)
print("TEST 3: Ce mois (30 derniers jours)")
print("=" * 60)
date_from = (now - timedelta(days=30)).date()
date_to = now.date()
print(f"Date de début: {date_from}")
print(f"Date de fin: {date_to}")

datetime_from = timezone.make_aware(datetime.combine(date_from, datetime.min.time()))
datetime_to = timezone.make_aware(datetime.combine(date_to, datetime.max.time()))
orders = Order.objects.filter(
    created_at__gte=datetime_from,
    created_at__lte=datetime_to
)
print(f"Résultats: {orders.count()}")

# Test 4: Aujourd'hui
print("\n" + "=" * 60)
print("TEST 4: Aujourd'hui")
print("=" * 60)
date_from = now.date()
date_to = now.date()
print(f"Date: {date_from}")

datetime_from = timezone.make_aware(datetime.combine(date_from, datetime.min.time()))
datetime_to = timezone.make_aware(datetime.combine(date_to, datetime.max.time()))
orders = Order.objects.filter(
    created_at__gte=datetime_from,
    created_at__lte=datetime_to
)
print(f"Résultats: {orders.count()}")

print("\n" + "=" * 60)
print("FIN DES TESTS")
print("=" * 60)

"""
Configuration du dashboard admin pour afficher des statistiques
"""
from django.db.models import Count, Sum, Avg
from django.utils.translation import gettext_lazy as _


def get_dashboard_stats():
    """Retourne les statistiques pour le dashboard"""
    from shop.models import Product, Category, Brand
    from orders.models import Order, Customer
    
    stats = {
        'products': {
            'total': Product.objects.count(),
            'categories': Category.objects.count(),
            'icon': 'fas fa-gamepad',
            'color': 'primary',
        },
        'orders': {
            'total': Order.objects.filter(status='confirmed').count(),
            'pending': Order.objects.filter(status='pending').count(),
            'revenue': Order.objects.filter(status='confirmed').aggregate(total=Sum('total_price'))['total'] or 0,
            'icon': 'fas fa-shopping-cart',
            'color': 'success',
        },
        'customers': {
            'total': Customer.objects.count(),
            'icon': 'fas fa-users',
            'color': 'info',
        },
        'brands': {
            'total': Brand.objects.count(),
            'icon': 'fas fa-trademark',
            'color': 'warning',
        }
    }
    
    return stats

"""
URLs pour l'API shop
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Créer le router pour les ViewSets
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'subcategories', views.SubCategoryViewSet, basename='subcategory')
router.register(r'types', views.TypeViewSet, basename='type')
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'hero-slides', views.HeroSlideViewSet, basename='hero-slide')

urlpatterns = [
    path('', include(router.urls)),
]

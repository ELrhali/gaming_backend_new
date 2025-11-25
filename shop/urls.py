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
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]

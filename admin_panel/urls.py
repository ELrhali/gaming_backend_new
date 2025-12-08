from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Redirection de /admin-panel/ vers /admin-panel/dashboard/
    path('', RedirectView.as_view(url='dashboard/', permanent=False), name='index'),
    
    # Authentification
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Catégories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Sous-catégories
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/add/', views.subcategory_add, name='subcategory_add'),
    path('subcategories/<int:pk>/edit/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategories/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),
    
    # Types
    path('types/', views.type_list, name='type_list'),
    path('types/add/', views.type_add, name='type_add'),
    path('types/<int:pk>/edit/', views.type_edit, name='type_edit'),
    path('types/<int:pk>/delete/', views.type_delete, name='type_delete'),
    
    # Marques
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/add/', views.brand_add, name='brand_add'),
    path('brands/<int:pk>/edit/', views.brand_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete, name='brand_delete'),
    
    # Produits
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/import/', views.product_import, name='product_import'),
    path('products/images-import/', views.product_images_import, name='product_images_import'),
    path('product/image/<int:pk>/delete/', views.product_image_delete, name='product_image_delete'),
    
    # Commandes
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('orders/<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    
    # Livraisons
    path('deliveries/', views.delivery_list, name='delivery_list'),
    path('deliveries/<int:pk>/', views.delivery_detail, name='delivery_detail'),
    path('deliveries/<int:pk>/update/', views.delivery_update, name='delivery_update'),
    
    # Utilisateurs
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Hero Slides
    path('hero-slides/', views.hero_slide_list, name='hero_slide_list'),
    path('hero-slides/add/', views.hero_slide_add, name='hero_slide_add'),
    path('hero-slides/<int:pk>/edit/', views.hero_slide_edit, name='hero_slide_edit'),
    path('hero-slides/<int:pk>/delete/', views.hero_slide_delete, name='hero_slide_delete'),
    
    # AJAX endpoints
    path('ajax/subcategories/', views.get_subcategories_by_category, name='ajax_subcategories'),
    path('ajax/subcategories-by-category/', views.get_subcategories_by_category, name='ajax_subcategories_by_category'),
    path('ajax/types/', views.get_types_by_subcategory, name='ajax_types'),
    path('ajax/types-by-brand/', views.get_types_by_brand, name='ajax_types_by_brand'),
    path('ajax/types-filtered/', views.get_types_filtered, name='ajax_types_filtered'),
]

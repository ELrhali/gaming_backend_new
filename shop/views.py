"""
Vues API pour le shop
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from .models import Category, SubCategory, Type, Product, ProductImage, Brand, HeroSlide
from .serializers import (
    CategorySerializer, SubCategoryListSerializer, SubCategoryDetailSerializer,
    TypeSerializer, ProductListSerializer, ProductDetailSerializer, BrandSerializer,
    HeroSlideSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les catégories
    
    list: Retourne toutes les catégories avec leurs sous-catégories
    retrieve: Retourne une catégorie spécifique avec ses sous-catégories
    """
    queryset = Category.objects.filter(is_active=True).prefetch_related(
        Prefetch('subcategories', queryset=SubCategory.objects.filter(is_active=True))
    )
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les sous-catégories
    
    list: Retourne toutes les sous-catégories
    retrieve: Retourne une sous-catégorie spécifique
    homepage: Retourne uniquement les sous-catégories à afficher sur la page d'accueil
    """
    queryset = SubCategory.objects.filter(is_active=True).select_related('category')
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubCategoryDetailSerializer
        return SubCategoryListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par is_essential si spécifié
        is_essential = self.request.query_params.get('is_essential', None)
        if is_essential and is_essential.lower() == 'true':
            queryset = queryset.filter(is_essential=True)
        
        # Limiter le nombre de résultats si spécifié
        limit = self.request.query_params.get('limit', None)
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def homepage(self, request):
        """
        Retourne les sous-catégories à afficher sur la page d'accueil
        GET /api/subcategories/homepage/
        """
        subcategories = self.queryset.filter(show_on_homepage=True).order_by('order', 'name')
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les types/marques
    """
    queryset = Type.objects.filter(is_active=True).select_related('subcategory')
    serializer_class = TypeSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer par sous-catégorie si spécifié
        subcategory_slug = self.request.query_params.get('subcategory', None)
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        return queryset


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les marques
    
    list: Retourne toutes les marques
    retrieve: Retourne une marque spécifique avec ses produits
    """
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les produits
    
    list: Retourne tous les produits avec filtres
    retrieve: Retourne un produit spécifique avec tous les détails
    bestsellers: Retourne les produits les plus vendus
    new: Retourne les nouveaux produits
    featured: Retourne les produits en vedette
    search: Recherche de produits
    
    Paramètres de filtrage (query params):
    - category: slug de la catégorie
    - subcategory: slug de la sous-catégorie
    - type: slug du type
    - is_bestseller: true/false
    - is_new: true/false
    - is_featured: true/false
    - min_price: prix minimum
    - max_price: prix maximum
    - search: recherche textuelle
    - ordering: champ de tri (price, -price, name, -created_at)
    """
    queryset = Product.objects.select_related(
        'category', 'subcategory', 'type'
    ).prefetch_related(
        'images', 'specifications'
    )
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'name', 'created_at', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par catégorie
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filtrer par sous-catégorie
        subcategory_slug = self.request.query_params.get('subcategory', None)
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        
        # Filtrer par type
        type_slug = self.request.query_params.get('type', None)
        if type_slug:
            queryset = queryset.filter(type__slug=type_slug)
        
        # Filtrer par marque (ID ou slug)
        brand = self.request.query_params.get('brand', None)
        if brand:
            # Essayer d'abord par ID, sinon par slug
            try:
                queryset = queryset.filter(brand_id=int(brand))
            except ValueError:
                queryset = queryset.filter(brand__slug=brand)
        
        # Filtrer par bestseller
        is_bestseller = self.request.query_params.get('is_bestseller', None)
        if is_bestseller and is_bestseller.lower() == 'true':
            queryset = queryset.filter(is_bestseller=True)
        
        # Filtrer par nouveau
        is_new = self.request.query_params.get('is_new', None)
        if is_new and is_new.lower() == 'true':
            queryset = queryset.filter(is_new=True)
        
        # Filtrer par featured
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured and is_featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filtrer par prix
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Recherche textuelle
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(reference__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(brand_text__icontains=search)
            )
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Incrémenter le compteur de vues"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """
        Retourne les produits bestsellers
        GET /api/products/bestsellers/?limit=6
        """
        limit = int(request.query_params.get('limit', 6))
        products = self.get_queryset().filter(is_bestseller=True, status='in_stock')[:limit]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new(self, request):
        """
        Retourne les nouveaux produits
        GET /api/products/new/?limit=10
        """
        limit = int(request.query_params.get('limit', 10))
        products = self.get_queryset().filter(is_new=True)[:limit]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Retourne les produits en vedette
        GET /api/products/featured/?limit=10
        """
        limit = int(request.query_params.get('limit', 10))
        products = self.get_queryset().filter(is_featured=True)[:limit]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_subcategory(self, request):
        """
        Retourne les produits d'une sous-catégorie avec un nombre limité
        GET /api/products/by_subcategory/?subcategory=cartes-graphiques&limit=4
        """
        subcategory_slug = request.query_params.get('subcategory')
        limit = int(request.query_params.get('limit', 4))
        
        if not subcategory_slug:
            return Response({'error': 'subcategory parameter is required'}, status=400)
        
        products = self.get_queryset().filter(
            subcategory__slug=subcategory_slug,
            status='in_stock'
        )[:limit]
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ad_slider(self, request):
        """
        Retourne les catégories et produits à afficher dans le slider de publicité
        GET /api/products/ad_slider/
        
        Retourne un objet avec:
        - categories: liste des catégories avec show_in_ad_slider=True
        - products: liste des produits avec show_in_ad_slider=True
        """
        from .serializers import CategorySerializer
        
        # Récupérer les catégories à afficher dans le slider
        categories = Category.objects.filter(
            is_active=True,
            show_in_ad_slider=True
        ).order_by('order', 'name')
        
        # Récupérer les produits à afficher dans le slider
        products = self.get_queryset().filter(
            show_in_ad_slider=True,
            status='in_stock'
        ).order_by('-created_at')
        
        category_serializer = CategorySerializer(categories, many=True, context={'request': request})
        product_serializer = self.get_serializer(products, many=True)
        
        return Response({
            'categories': category_serializer.data,
            'products': product_serializer.data
        })


class HeroSlideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Hero Slides
    
    list: Retourne tous les slides actifs pour le hero slider
    """
    queryset = HeroSlide.objects.filter(is_active=True).select_related(
        'category', 'subcategory', 'product'
    ).order_by('order', '-created_at')
    serializer_class = HeroSlideSerializer


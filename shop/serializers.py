"""
Serializers pour l'API REST
"""
from rest_framework import serializers
from .models import Category, SubCategory, Type, Product, ProductImage, ProductSpecification, Brand, HeroSlide


class BrandSerializer(serializers.ModelSerializer):
    """Serializer pour les marques"""
    logo_url_computed = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'logo_url', 'logo_url_computed', 'description', 'order', 'is_active', 'product_count']
    
    def get_logo_url_computed(self, obj):
        # Priorité: logo_url (URL directe) > logo uploadé
        if obj.logo_url:
            return obj.logo_url
        elif obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
        return None
    
    def get_product_count(self, obj):
        return obj.products.filter(status='in_stock').count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer pour les images de produits"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'is_main', 'order']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer pour les spécifications de produits"""
    
    class Meta:
        model = ProductSpecification
        fields = ['id', 'key', 'value', 'order']


class TypeSerializer(serializers.ModelSerializer):
    """Serializer pour les types"""
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    
    class Meta:
        model = Type
        fields = ['id', 'subcategory', 'name', 'slug', 'description', 'order', 'subcategory_name', 'subcategory_slug']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des produits (version simple)"""
    main_image_url = serializers.SerializerMethodField()
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'reference', 'name', 'slug', 'price', 'discount_price',
            'final_price', 'discount_percentage', 'main_image_url',
            'is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider', 'status', 'quantity',
            'category_name', 'category_slug', 'subcategory_name', 'subcategory_slug',
            'brand_name', 'brand_logo_url'
        ]
    
    def get_main_image_url(self, obj):
        main_image = obj.get_main_image
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.url)
        return None
    
    def get_brand_logo_url(self, obj):
        if obj.brand and obj.brand.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.brand.logo.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les détails d'un produit"""
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    
    # Champs simples pour compatibilité frontend
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    subcategory_slug = serializers.CharField(source='subcategory.slug', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, allow_null=True)
    
    # Champs détaillés pour informations complètes
    category_data = serializers.SerializerMethodField()
    subcategory_data = serializers.SerializerMethodField()
    type_data = TypeSerializer(source='type', read_only=True)
    brand_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'reference', 'name', 'slug', 'meta_title', 'meta_description',
            'description', 'caracteristiques', 'price', 'discount_price',
            'final_price', 'discount_percentage', 'quantity', 'status',
            'is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider', 'warranty', 'weight',
            'main_image_url', 'images', 'specifications',
            'category_name', 'category_slug', 'subcategory_name', 'subcategory_slug',
            'brand_name', 'brand_data',
            'category_data', 'subcategory_data', 'type_data', 'views_count',
            'created_at', 'updated_at'
        ]
    
    def get_main_image_url(self, obj):
        main_image = obj.get_main_image
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.url)
        return None
    
    def get_category_data(self, obj):
        if obj.category:
            return {
                'id': obj.category.id,
                'name': obj.category.name,
                'slug': obj.category.slug
            }
        return None
    
    def get_subcategory_data(self, obj):
        if obj.subcategory:
            return {
                'id': obj.subcategory.id,
                'name': obj.subcategory.name,
                'slug': obj.subcategory.slug
            }
        return None
    
    def get_brand_data(self, obj):
        if obj.brand:
            brand_serializer = BrandSerializer(obj.brand, context=self.context)
            return brand_serializer.data
        return None


class SubCategoryListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des sous-catégories"""
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = [
            'id', 'category', 'name', 'slug', 'image', 'image_url', 'description',
            'order', 'is_essential', 'show_on_homepage', 'category_name', 'category_slug',
            'product_count'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_product_count(self, obj):
        return obj.products.filter(status='in_stock').count()


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les détails d'une sous-catégorie"""
    image_url = serializers.SerializerMethodField()
    category_data = serializers.SerializerMethodField()
    types = TypeSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = [
            'id', 'name', 'slug', 'image', 'image_url', 'description',
            'order', 'is_essential', 'show_on_homepage', 'category_data', 'types', 'product_count'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_category_data(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name,
            'slug': obj.category.slug
        }
    
    def get_product_count(self, obj):
        return obj.products.filter(status='in_stock').count()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories"""
    image_url = serializers.SerializerMethodField()
    subcategories = SubCategoryListSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'image', 'image_url', 'description',
            'order', 'show_in_ad_slider', 'subcategories', 'product_count'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_product_count(self, obj):
        return Product.objects.filter(category=obj, status='in_stock').count()


class HeroSlideSerializer(serializers.ModelSerializer):
    """Serializer pour les Hero Slides"""
    image_url = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    target_name = serializers.SerializerMethodField()
    badge = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    
    class Meta:
        model = HeroSlide
        fields = [
            'id', 'title', 'description', 'slide_type', 'image_url',
            'link', 'target_name', 'badge', 'price', 'discount',
            'order', 'is_active'
        ]
    
    def get_image_url(self, obj):
        """Retourne l'URL de l'image"""
        image_url = obj.get_image_url()
        if image_url:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image_url)
        return None
    
    def get_link(self, obj):
        """Retourne le lien vers l'élément"""
        return obj.get_link()
    
    def get_target_name(self, obj):
        """Retourne le nom de l'élément ciblé"""
        if obj.slide_type == 'category' and obj.category:
            return obj.category.name
        elif obj.slide_type == 'subcategory' and obj.subcategory:
            return obj.subcategory.name
        elif obj.slide_type == 'product' and obj.product:
            return obj.product.name
        return None
    
    def get_badge(self, obj):
        """Retourne le badge a afficher"""
        if obj.slide_type == 'category':
            return 'Categorie en vedette'
        elif obj.slide_type == 'subcategory':
            return 'Sous-categorie populaire'
        elif obj.slide_type == 'product' and obj.product:
            if obj.product.discount_percentage > 0:
                return f'-{obj.product.discount_percentage}% de reduction'
            return 'Produit en promotion'
        return None
    
    def get_price(self, obj):
        """Retourne le prix pour les produits"""
        if obj.slide_type == 'product' and obj.product:
            return f"{float(obj.product.final_price):.0f} MAD"
        return None
    
    def get_discount(self, obj):
        """Retourne le pourcentage de réduction pour les produits"""
        if obj.slide_type == 'product' and obj.product:
            return obj.product.discount_percentage
        return 0

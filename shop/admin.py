from django.contrib import admin
from .models import Category, SubCategory, Type, Collection, Product, ProductImage, Brand, HeroSlide


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'show_in_ad_slider', 'created_at']
    list_filter = ['is_active', 'show_in_ad_slider']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['show_in_ad_slider']
    inlines = [SubCategoryInline]


class TypeInline(admin.TabularInline):
    model = Type
    extra = 1


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_essential', 'is_active', 'show_on_homepage', 'created_at']
    list_filter = ['category', 'is_essential', 'is_active', 'show_on_homepage']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_essential', 'is_active', 'show_on_homepage']
    inlines = [TypeInline]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'order', 'is_active', 'created_at']
    list_filter = ['subcategory', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'website', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'logo')
        }),
        ('Description', {
            'fields': ('description', 'website')
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['reference', 'name', 'category', 'subcategory', 'brand', 'price', 'quantity', 'status', 'is_bestseller', 'show_in_ad_slider', 'created_at']
    list_filter = ['category', 'subcategory', 'brand', 'status', 'is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider']
    search_fields = ['reference', 'name', 'description']
    prepopulated_fields = {'slug': ('reference', 'name')}
    list_editable = ['show_in_ad_slider']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('reference', 'name', 'slug', 'main_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Description', {
            'fields': ('description', 'caracteristiques')
        }),
        ('Classification', {
            'fields': ('category', 'subcategory', 'type', 'collection', 'brand')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'discount_price', 'quantity', 'status')
        }),
        ('Caractéristiques spéciales', {
            'fields': ('is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider')
        }),
        ('Autres informations', {
            'fields': ('brand_text', 'warranty', 'weight')
        }),
    )


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_type', 'get_target', 'order', 'is_active', 'created_at']
    list_filter = ['slide_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Informations du Slide', {
            'fields': ('title', 'description', 'slide_type'),
            'description': 'Informations principales affichées sur le slide'
        }),
        ('Sélection de l\'élément', {
            'fields': ('category', 'subcategory', 'product'),
            'description': 'Sélectionnez UN SEUL élément selon le type choisi ci-dessus'
        }),
        ('Image', {
            'fields': ('custom_image',),
            'description': 'Image personnalisée (optionnel - sinon l\'image de l\'élément sera utilisée)'
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active'),
            'description': 'Ordre d\'affichage et activation du slide'
        }),
    )
    
    def get_target(self, obj):
        """Affiche l'élément ciblé par le slide"""
        if obj.slide_type == 'category' and obj.category:
            return f"📁 {obj.category.name}"
        elif obj.slide_type == 'subcategory' and obj.subcategory:
            return f"📂 {obj.subcategory.name}"
        elif obj.slide_type == 'product' and obj.product:
            return f"🎮 {obj.product.name}"
        return "❌ Non défini"
    get_target.short_description = "Élément ciblé"
    
    class Media:
        css = {
            'all': ('admin/css/hero-slide-admin.css',)
        }
        js = ('admin/js/hero-slide-admin.js',)

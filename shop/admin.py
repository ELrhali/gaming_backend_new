from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
    readonly_fields = ['image_dimension_info']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'collection')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image',),
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active', 'show_in_ad_slider')
        }),
    )
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">800 × 320 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 2.5:1 (paysage large)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: WebP ou JPG optimisé<br>'
            '✅ Taille max: 100 KB<br>'
            '✅ Sujet principal au centre'
            '</div></div>'
        )
    image_dimension_info.short_description = ''


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
    readonly_fields = ['image_dimension_info']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('category', 'name', 'slug')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image',),
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active', 'is_essential', 'show_on_homepage')
        }),
    )
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">400 × 450 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: ~1:1 (carré/portrait)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: WebP ou JPG optimisé<br>'
            '✅ Taille max: 80 KB<br>'
            '✅ Utilisée dans CreativeBackground'
            '</div></div>'
        )
    image_dimension_info.short_description = ''


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'order', 'is_active', 'created_at']
    list_filter = ['subcategory', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview_large', 'logo_dimension_info']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug')
        }),
        ('Logo', {
            'fields': ('logo_dimension_info', 'logo_preview_large', 'logo', 'logo_url'),
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def logo_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">200 × 200 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carré)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: PNG transparent ou WebP<br>'
            '✅ Taille max: 50 KB<br>'
            '✅ Affiché dans un cercle'
            '</div></div>'
        )
    logo_dimension_info.short_description = ''
    
    def logo_preview(self, obj):
        """Prévisualisation du logo dans la liste"""
        if obj.logo_url:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: contain;" />',
                obj.logo_url
            )
        elif obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: contain;" />',
                obj.logo.url
            )
        return '-'
    logo_preview.short_description = 'Logo'
    
    def logo_preview_large(self, obj):
        """Prévisualisation du logo dans le formulaire"""
        if obj.logo_url:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border: 1px solid #ddd; padding: 10px; background: white;" />',
                obj.logo_url
            )
        elif obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border: 1px solid #ddd; padding: 10px; background: white;" />',
                obj.logo.url
            )
        return 'Aucun logo'
    logo_preview_large.short_description = 'Prévisualisation actuelle'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_dimension_info']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image',),
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Paramètres', {
            'fields': ('is_active',)
        }),
    )
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">600 × 600 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carré)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: WebP ou JPG optimisé<br>'
            '✅ Taille max: 100 KB'
            '</div></div>'
        )
    image_dimension_info.short_description = ''


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_info']
    fields = ['image_info', 'image', 'is_main', 'order']
    
    def image_info(self, obj):
        return format_html(
            '<span style="background: #ff6b6b; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px;">'
            '📐 600×600 px (carré)'
            '</span>'
        )
    image_info.short_description = 'Dimension'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['reference', 'name', 'category', 'subcategory', 'brand', 'price', 'quantity', 'status', 'is_bestseller', 'show_in_ad_slider', 'created_at']
    list_filter = ['category', 'subcategory', 'brand', 'status', 'is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider']
    search_fields = ['reference', 'name', 'description']
    prepopulated_fields = {'slug': ('reference', 'name')}
    list_editable = ['show_in_ad_slider']
    inlines = [ProductImageInline]
    readonly_fields = ['image_dimension_info']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('reference', 'name', 'slug')
        }),
        ('Image principale', {
            'fields': ('image_dimension_info', 'main_image'),
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
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">600 × 600 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carré)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: WebP ou JPG optimisé<br>'
            '✅ Taille max: 100 KB<br>'
            '✅ Fond blanc préféré'
            '</div></div>'
        )
    image_dimension_info.short_description = ''


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_type', 'get_target', 'order', 'is_active', 'created_at']
    list_filter = ['slide_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['image_dimension_info']
    
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
            'fields': ('image_dimension_info', 'custom_image',),
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active'),
            'description': 'Ordre d\'affichage et activation du slide'
        }),
    )
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">📐 DIMENSION RECOMMANDÉE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">1200 × 500 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 2.4:1 (bannière)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            '✅ Format: WebP ou JPG optimisé<br>'
            '✅ Taille max: 150 KB<br>'
            '✅ Sur mobile, image centrée<br>'
            '⚠️ Laissez vide pour utiliser l\'image de l\'élément'
            '</div></div>'
        )
    image_dimension_info.short_description = ''
    
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

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models
from .models import Category, SubCategory, Type, Collection, Product, ProductImage, Brand, HeroSlide


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'order', 'is_active', 'show_in_ad_slider', 'created_at']
    list_filter = ['is_active', 'show_in_ad_slider']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['show_in_ad_slider']
    inlines = [SubCategoryInline]
    readonly_fields = ['image_dimension_info', 'image_preview_large']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'collection')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image_preview_large', 'image',),
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
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">800 x 320 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 2.5:1 (paysage large)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: WebP ou JPG optimise<br>'
            'Taille max: 100 KB<br>'
            'Sujet principal au centre'
            '</div></div>'
        )
    image_dimension_info.short_description = ''
    
    def image_preview(self, obj):
        """Prévisualisation de l'image dans la liste"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """Previsualisation de l'image dans le formulaire"""
        if obj and obj.pk and obj.image:
            try:
                return mark_safe(
                    '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px; border: 2px solid #667eea;">'
                    '<p style="margin: 0 0 15px 0; font-weight: bold; color: #333; font-size: 14px;">IMAGE ACTUELLE:</p>'
                    '<img src="{url}" style="max-width: 400px; max-height: 200px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 10px;" />'
                    '<div style="margin-top: 15px;">'
                    '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold; margin-right: 10px;">Voir en taille reelle</a>'
                    '</div>'
                    '</div>'.format(url=obj.image.url)
                )
            except Exception:
                pass
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucune image - Ajoutez une image ci-dessous</span>'
            '</div>'
        )
    image_preview_large.short_description = ''


class TypeInline(admin.TabularInline):
    model = Type
    extra = 1


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'category', 'order', 'is_essential', 'is_active', 'show_on_homepage', 'created_at']
    list_filter = ['category', 'is_essential', 'is_active', 'show_on_homepage']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_essential', 'is_active', 'show_on_homepage']
    inlines = [TypeInline]
    readonly_fields = ['image_dimension_info', 'image_preview_large']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('category', 'name', 'slug')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image_preview_large', 'image',),
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
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">400 x 450 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: ~1:1 (carre/portrait)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: WebP ou JPG optimise<br>'
            'Taille max: 80 KB<br>'
            'Utilisee dans CreativeBackground'
            '</div></div>'
        )
    image_dimension_info.short_description = ''
    
    def image_preview(self, obj):
        """Previsualisation de l'image dans la liste"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """Previsualisation de l'image dans le formulaire"""
        if obj and obj.pk and obj.image:
            try:
                return mark_safe(
                    '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px; border: 2px solid #11998e;">'
                    '<p style="margin: 0 0 15px 0; font-weight: bold; color: #333; font-size: 14px;">IMAGE ACTUELLE:</p>'
                    '<img src="{url}" style="max-width: 200px; max-height: 250px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 10px;" />'
                    '<div style="margin-top: 15px;">'
                    '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold;">Voir en taille reelle</a>'
                    '</div>'
                    '</div>'.format(url=obj.image.url)
                )
            except Exception:
                pass
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucune image - Ajoutez une image ci-dessous</span>'
            '</div>'
        )
    image_preview_large.short_description = ''


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
    readonly_fields = ['logo_dimension_info', 'logo_preview_large']
    
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
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">200 x 200 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carre)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: PNG transparent ou WebP<br>'
            'Taille max: 50 KB<br>'
            'Affiche dans un cercle'
            '</div></div>'
        )
    logo_dimension_info.short_description = ''
    
    def logo_preview(self, obj):
        """Previsualisation du logo dans la liste"""
        if obj.logo_url:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: contain; border-radius: 50%;" />',
                obj.logo_url
            )
        elif obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: contain; border-radius: 50%;" />',
                obj.logo.url
            )
        return '-'
    logo_preview.short_description = 'Logo'
    
    def logo_preview_large(self, obj):
        """Previsualisation du logo dans le formulaire"""
        logo_url = None
        try:
            if obj and obj.pk:
                if obj.logo_url:
                    logo_url = obj.logo_url
                elif obj.logo:
                    logo_url = obj.logo.url
        except Exception:
            pass
        
        if logo_url:
            return mark_safe(
                '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px; border: 2px solid #f093fb;">'
                '<p style="margin: 0 0 15px 0; font-weight: bold; color: #333; font-size: 14px;">LOGO ACTUEL:</p>'
                '<img src="{url}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 15px;" />'
                '<div style="margin-top: 15px;">'
                '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold;">Voir en taille reelle</a>'
                '</div>'
                '</div>'.format(url=logo_url)
            )
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucun logo - Ajoutez un logo ci-dessous ou renseignez l\'URL</span>'
            '</div>'
        )
    logo_preview_large.short_description = ''


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_dimension_info', 'image_preview_large']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug')
        }),
        ('Image', {
            'fields': ('image_dimension_info', 'image_preview_large', 'image',),
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
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">600 x 600 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carre)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: WebP ou JPG optimise<br>'
            'Taille max: 100 KB'
            '</div></div>'
        )
    image_dimension_info.short_description = ''
    
    def image_preview(self, obj):
        """Previsualisation de l'image dans la liste"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """Previsualisation de l'image dans le formulaire"""
        if obj and obj.pk and obj.image:
            try:
                return mark_safe(
                    '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px; border: 2px solid #a18cd1;">'
                    '<p style="margin: 0 0 15px 0; font-weight: bold; color: #333; font-size: 14px;">IMAGE ACTUELLE:</p>'
                    '<img src="{url}" style="max-width: 300px; max-height: 300px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 10px;" />'
                    '<div style="margin-top: 15px;">'
                    '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold;">Voir en taille reelle</a>'
                    '</div>'
                    '</div>'.format(url=obj.image.url)
                )
            except Exception:
                pass
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucune image - Ajoutez une image ci-dessous</span>'
            '</div>'
        )
    image_preview_large.short_description = ''


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview', 'image_info']
    fields = ['image_preview', 'image_info', 'image', 'is_main', 'order']
    
    def image_preview(self, obj):
        """Previsualisation de l'image dans l'inline"""
        if obj and obj.pk and obj.image:
            try:
                return mark_safe(
                    '<a href="{url}" target="_blank">'
                    '<img src="{url}" style="max-width: 80px; max-height: 80px; object-fit: cover; border-radius: 4px; border: 2px solid #ddd;" />'
                    '</a>'.format(url=obj.image.url)
                )
            except Exception:
                pass
        return mark_safe('<span style="color: #999; font-size: 11px;">Nouvelle image</span>')
    image_preview.short_description = 'Apercu'
    
    def image_info(self, obj):
        return format_html(
            '<span style="background: #ff6b6b; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px;">'
            '600x600 px (carre)'
            '</span>'
        )
    image_info.short_description = 'Dimension'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['reference', 'name', 'main_image_preview', 'category', 'subcategory', 'brand', 'price', 'quantity', 'status', 'is_bestseller', 'show_in_ad_slider', 'created_at']
    list_filter = ['category', 'subcategory', 'brand', 'status', 'is_bestseller', 'is_featured', 'is_new', 'show_in_ad_slider']
    search_fields = ['reference', 'name', 'description']
    prepopulated_fields = {'slug': ('reference', 'name')}
    list_editable = ['show_in_ad_slider']
    inlines = [ProductImageInline]
    readonly_fields = ['image_dimension_info', 'main_image_preview_large', 'all_images_preview']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('reference', 'name', 'slug')
        }),
        ('Image principale', {
            'fields': ('image_dimension_info', 'main_image_preview_large', 'main_image'),
        }),
        ('Galerie d\'images', {
            'fields': ('all_images_preview',),
            'description': 'Les images supplémentaires se gèrent dans la section "Images des produits" ci-dessous'
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
    
    def main_image_preview(self, obj):
        """Previsualisation de l'image principale dans la liste"""
        main_img = obj.get_main_image
        if main_img:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px; object-fit: cover; border-radius: 4px;" />',
                main_img.url
            )
        return '-'
    main_image_preview.short_description = 'Image'
    
    def main_image_preview_large(self, obj):
        """Previsualisation de l'image principale dans le formulaire"""
        if obj and obj.pk:
            try:
                main_img = obj.get_main_image
                if main_img:
                    return mark_safe(
                        '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px; border: 2px solid #ff6b6b;">'
                        '<p style="margin: 0 0 15px 0; font-weight: bold; color: #333; font-size: 14px;">IMAGE PRINCIPALE ACTUELLE:</p>'
                        '<img src="{url}" style="max-width: 300px; max-height: 300px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 10px;" />'
                        '<div style="margin-top: 15px;">'
                        '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold;">Voir en taille reelle</a>'
                        '</div>'
                        '</div>'.format(url=main_img.url)
                    )
            except Exception:
                pass
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucune image principale - Ajoutez une image ci-dessous</span>'
            '</div>'
        )
    main_image_preview_large.short_description = ''
    
    def all_images_preview(self, obj):
        """Affiche toutes les images du produit"""
        if not obj.pk:
            return mark_safe('<span style="color: #999;">Sauvegardez le produit pour voir la galerie</span>')
        
        images = obj.images.all().order_by('order')
        if not images:
            return mark_safe(
                '<div style="padding: 20px; background: #e8f4fd; border-radius: 8px; border: 2px dashed #2196f3; text-align: center;">'
                '<span style="color: #1565c0; font-size: 14px;">Aucune image dans la galerie - Ajoutez des images dans la section ci-dessous</span>'
                '</div>'
            )
        
        html_parts = ['<div style="display: flex; flex-wrap: wrap; gap: 10px; padding: 15px; background: #f8f9fa; border-radius: 8px;">']
        for img in images:
            is_main_badge = ''
            if img.is_main:
                is_main_badge = '<span style="position: absolute; top: 5px; left: 5px; background: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px;">Principale</span>'
            
            html_parts.append(
                '<div style="position: relative; border: 2px solid #ddd; border-radius: 8px; padding: 5px; background: white;">'
                '{badge}'
                '<a href="{url}" target="_blank">'
                '<img src="{url}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 4px;" />'
                '</a>'
                '<div style="text-align: center; font-size: 10px; color: #666; margin-top: 5px;">Ordre: {order}</div>'
                '</div>'.format(badge=is_main_badge, url=img.image.url, order=img.order)
            )
        html_parts.append('</div>')
        return mark_safe(''.join(html_parts))
    all_images_preview.short_description = 'Galerie d\'images actuelle'
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">600 x 600 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 1:1 (carre)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: WebP ou JPG optimise<br>'
            'Taille max: 100 KB<br>'
            'Fond blanc prefere'
            '</div></div>'
        )
    image_dimension_info.short_description = ''


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'slide_type', 'get_target', 'order', 'is_active', 'created_at']
    list_filter = ['slide_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['image_dimension_info', 'current_image_preview']
    
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
            'fields': ('image_dimension_info', 'current_image_preview', 'custom_image',),
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active'),
            'description': 'Ordre d\'affichage et activation du slide'
        }),
    )
    
    def image_preview(self, obj):
        """Previsualisation de l'image dans la liste"""
        image_url = obj.get_image_url()
        if image_url:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 50px; object-fit: cover; border-radius: 4px;" />',
                image_url
            )
        return '-'
    image_preview.short_description = 'Image'
    
    def current_image_preview(self, obj):
        """Previsualisation de l'image provenant de l'element lie"""
        if obj and obj.pk:
            try:
                image_url = obj.get_image_url()
                source = "personnalisee"
                if not obj.custom_image:
                    if obj.slide_type == 'category' and obj.category:
                        source = "categorie ({name})".format(name=obj.category.name)
                    elif obj.slide_type == 'subcategory' and obj.subcategory:
                        source = "sous-categorie ({name})".format(name=obj.subcategory.name)
                    elif obj.slide_type == 'product' and obj.product:
                        source = "produit ({name})".format(name=obj.product.name)
                
                if image_url:
                    return mark_safe(
                        '<div style="margin-bottom: 15px; padding: 20px; background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%); border-radius: 12px; border: 2px solid #4facfe;">'
                        '<p style="margin: 0 0 15px 0; font-weight: bold; color: #234e52; font-size: 14px;">IMAGE ACTUELLE (source: {source}):</p>'
                        '<img src="{url}" style="max-width: 500px; max-height: 250px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); background: white; padding: 10px;" />'
                        '<div style="margin-top: 15px;">'
                        '<a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold;">Voir en taille reelle</a>'
                        '</div>'
                        '</div>'.format(url=image_url, source=source)
                    )
            except Exception:
                pass
        return mark_safe(
            '<div style="padding: 20px; background: #fff3cd; border-radius: 8px; border: 2px dashed #ffc107; text-align: center;">'
            '<span style="color: #856404; font-size: 14px;">Aucune image - Selectionnez un element ou ajoutez une image personnalisee</span>'
            '</div>'
        )
    current_image_preview.short_description = ''
    
    def image_dimension_info(self, obj):
        return format_html(
            '<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
            '<strong style="font-size: 16px;">DIMENSION RECOMMANDEE</strong><br><br>'
            '<span style="font-size: 24px; font-weight: bold;">1200 x 500 px</span><br>'
            '<span style="opacity: 0.9;">Ratio: 2.4:1 (banniere)</span><br><br>'
            '<div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 4px; font-size: 12px;">'
            'Format: WebP ou JPG optimise<br>'
            'Taille max: 150 KB<br>'
            'Sur mobile, image centree<br>'
            'Laissez vide pour utiliser l\'image de l\'element'
            '</div></div>'
        )
    image_dimension_info.short_description = ''
    
    def get_target(self, obj):
        """Affiche l'element cible par le slide"""
        if obj.slide_type == 'category' and obj.category:
            return f"[CAT] {obj.category.name}"
        elif obj.slide_type == 'subcategory' and obj.subcategory:
            return f"[SCAT] {obj.subcategory.name}"
        elif obj.slide_type == 'product' and obj.product:
            return f"[PROD] {obj.product.name}"
        return "Non defini"
    get_target.short_description = "Element cible"
    
    class Media:
        css = {
            'all': ('admin/css/hero-slide-admin.css',)
        }
        js = ('admin/js/hero-slide-admin.js',)

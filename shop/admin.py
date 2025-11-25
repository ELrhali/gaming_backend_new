from django.contrib import admin
from .models import Category, SubCategory, Type, Collection, Product, ProductImage


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]


class TypeInline(admin.TabularInline):
    model = Type
    extra = 1


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TypeInline]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'order', 'is_active', 'created_at']
    list_filter = ['subcategory', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


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
    list_display = ['reference', 'name', 'category', 'subcategory', 'price', 'quantity', 'status', 'is_bestseller', 'created_at']
    list_filter = ['category', 'subcategory', 'status', 'is_bestseller', 'is_featured', 'is_new']
    search_fields = ['reference', 'name', 'description']
    prepopulated_fields = {'slug': ('reference', 'name')}
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
            'fields': ('category', 'subcategory', 'type', 'collection')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'discount_price', 'quantity', 'status')
        }),
        ('Caractéristiques spéciales', {
            'fields': ('is_bestseller', 'is_featured', 'is_new')
        }),
        ('Autres informations', {
            'fields': ('brand', 'warranty', 'weight')
        }),
    )

from django import forms
from .models import Category, SubCategory, Brand, Collection, Product, ProductImage, HeroSlide
from .widgets import (
    AdminImagePreviewWidget, 
    AdminLogoPreviewWidget, 
    AdminProductImagePreviewWidget,
    AdminHeroSlideImagePreviewWidget
)


class CategoryAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les catégories avec prévisualisation d'image"""
    
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'image': AdminImagePreviewWidget(preview_width=400, preview_height=160, color='linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
        }


class SubCategoryAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les sous-catégories avec prévisualisation d'image"""
    
    class Meta:
        model = SubCategory
        fields = '__all__'
        widgets = {
            'image': AdminImagePreviewWidget(preview_width=200, preview_height=225, color='linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'),
        }


class BrandAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les marques avec prévisualisation du logo"""
    
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'logo': AdminLogoPreviewWidget(),
        }


class CollectionAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les collections avec prévisualisation d'image"""
    
    class Meta:
        model = Collection
        fields = '__all__'
        widgets = {
            'image': AdminImagePreviewWidget(preview_width=300, preview_height=300, color='linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)'),
        }


class ProductAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les produits avec prévisualisation d'image"""
    
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'main_image': AdminProductImagePreviewWidget(),
        }


class ProductImageInlineForm(forms.ModelForm):
    """Formulaire personnalisé pour les images de produits inline"""
    
    class Meta:
        model = ProductImage
        fields = '__all__'
        widgets = {
            'image': AdminProductImagePreviewWidget(),
        }


class HeroSlideAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les slides hero avec prévisualisation d'image"""
    
    class Meta:
        model = HeroSlide
        fields = '__all__'
        widgets = {
            'custom_image': AdminHeroSlideImagePreviewWidget(),
        }

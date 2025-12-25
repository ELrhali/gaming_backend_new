from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.admin.widgets import AdminFileWidget


class AdminImagePreviewWidget(AdminFileWidget):
    """Widget admin personnalise pour afficher la previsualisation de l'image"""
    
    def __init__(self, attrs=None, preview_width=300, preview_height=200, color='#667eea'):
        self.preview_width = preview_width
        self.preview_height = preview_height
        self.color = color
        super().__init__(attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        
        # Ajouter la previsualisation si une image existe
        if value and hasattr(value, 'url'):
            try:
                output.append(
                    '<div style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 2px solid #e9ecef;">'
                    '<p style="margin: 0 0 10px 0; font-weight: bold; color: #495057;">'
                    'Image actuelle:'
                    '</p>'
                    '<a href="{url}" target="_blank">'
                    '<img src="{url}" style="max-width: {width}px; max-height: {height}px; object-fit: contain; border-radius: 8px; border: 1px solid #dee2e6; background: white; padding: 5px;" />'
                    '</a>'
                    '<br>'
                    '<a href="{url}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: {color}; color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: 500;">'
                    'Voir en taille reelle'
                    '</a>'
                    '</div>'.format(
                        url=value.url, 
                        width=self.preview_width, 
                        height=self.preview_height,
                        color=self.color
                    )
                )
            except Exception as e:
                pass
        
        # Rendu du widget standard
        output.append(super().render(name, value, attrs, renderer))
        
        return mark_safe(''.join(output))


class AdminLogoPreviewWidget(AdminFileWidget):
    """Widget admin personnalise pour afficher la previsualisation du logo (cercle)"""
    
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        
        if value and hasattr(value, 'url'):
            try:
                output.append(
                    '<div style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 2px solid #e9ecef;">'
                    '<p style="margin: 0 0 10px 0; font-weight: bold; color: #495057;">'
                    'Logo actuel:'
                    '</p>'
                    '<a href="{url}" target="_blank">'
                    '<img src="{url}" style="max-width: 150px; max-height: 150px; object-fit: contain; border-radius: 50%; border: 2px solid #dee2e6; background: white; padding: 10px;" />'
                    '</a>'
                    '<br>'
                    '<a href="{url}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: 500;">'
                    'Voir en taille reelle'
                    '</a>'
                    '</div>'.format(url=value.url)
                )
            except Exception:
                pass
        
        output.append(super().render(name, value, attrs, renderer))
        
        return mark_safe(''.join(output))


class AdminProductImagePreviewWidget(AdminFileWidget):
    """Widget admin personnalise pour les images de produits"""
    
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        
        if value and hasattr(value, 'url'):
            try:
                output.append(
                    '<div style="margin-bottom: 15px; padding: 15px; background: #fff5f5; border-radius: 8px; border: 2px solid #fed7d7;">'
                    '<p style="margin: 0 0 10px 0; font-weight: bold; color: #c53030;">'
                    'Image actuelle:'
                    '</p>'
                    '<a href="{url}" target="_blank">'
                    '<img src="{url}" style="max-width: 250px; max-height: 250px; object-fit: contain; border-radius: 8px; border: 1px solid #feb2b2; background: white; padding: 5px;" />'
                    '</a>'
                    '<br>'
                    '<a href="{url}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: 500;">'
                    'Voir en taille reelle'
                    '</a>'
                    '</div>'.format(url=value.url)
                )
            except Exception:
                pass
        
        output.append(super().render(name, value, attrs, renderer))
        
        return mark_safe(''.join(output))


class AdminHeroSlideImagePreviewWidget(AdminFileWidget):
    """Widget admin personnalise pour les images des slides hero"""
    
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        
        if value and hasattr(value, 'url'):
            try:
                output.append(
                    '<div style="margin-bottom: 15px; padding: 15px; background: #e6fffa; border-radius: 8px; border: 2px solid #b2f5ea;">'
                    '<p style="margin: 0 0 10px 0; font-weight: bold; color: #234e52;">'
                    'Image personnalisee actuelle:'
                    '</p>'
                    '<a href="{url}" target="_blank">'
                    '<img src="{url}" style="max-width: 500px; max-height: 220px; object-fit: contain; border-radius: 8px; border: 1px solid #81e6d9; background: white; padding: 5px;" />'
                    '</a>'
                    '<br>'
                    '<a href="{url}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: 500;">'
                    'Voir en taille reelle'
                    '</a>'
                    '</div>'.format(url=value.url)
                )
            except Exception:
                pass
        
        output.append(super().render(name, value, attrs, renderer))
        
        return mark_safe(''.join(output))


# Anciens widgets pour compatibilité
ImagePreviewWidget = AdminImagePreviewWidget
LogoPreviewWidget = AdminLogoPreviewWidget
ProductImagePreviewWidget = AdminProductImagePreviewWidget
HeroSlideImagePreviewWidget = AdminHeroSlideImagePreviewWidget

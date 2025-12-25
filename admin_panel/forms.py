from django import forms
from shop.models import Category, SubCategory, Type, Product, ProductImage, Brand, HeroSlide
from orders.models import Order, Delivery


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'image', 'description', 'order', 'is_active', 'is_essential', 'show_on_homepage']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_essential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_on_homepage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['brand', 'subcategory', 'name', 'description', 'order', 'is_active']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si on édite un produit existant
        if self.instance and self.instance.pk:
            # Filtrer les sous-catégories selon la catégorie du produit
            if self.instance.category:
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    category=self.instance.category,
                    is_active=True
                ).order_by('name')
            else:
                # Si pas de catégorie, montrer toutes les sous-catégories
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    is_active=True
                ).order_by('name')
            
            # Filtrer les types selon la sous-catégorie ET la marque du produit
            type_queryset = Type.objects.filter(is_active=True)
            
            if self.instance.subcategory:
                type_queryset = type_queryset.filter(subcategory=self.instance.subcategory)
            
            if self.instance.brand:
                type_queryset = type_queryset.filter(brand=self.instance.brand)
            
            self.fields['type'].queryset = type_queryset.order_by('name')
        else:
            # Pour un nouveau produit, montrer toutes les options
            # Le JavaScript les filtrera dynamiquement
            self.fields['subcategory'].queryset = SubCategory.objects.filter(
                is_active=True
            ).order_by('name')
            self.fields['type'].queryset = Type.objects.filter(
                is_active=True
            ).order_by('name')
    
    class Meta:
        model = Product
        fields = [
            'reference', 'name', 'meta_title', 'meta_description',
            'description', 'caracteristiques', 'category', 'subcategory',
            'type', 'collection', 'price', 'discount_price', 'quantity',
            'status', 'is_bestseller', 'is_featured', 'is_new',
            'brand', 'brand_text', 'warranty', 'weight'
        ]
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'caracteristiques': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'collection': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'brand_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optionnel (deprecated)'}),
            'warranty': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_bestseller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['tracking_number', 'status', 'carrier', 'package_count', 'notes', 'shipped_at', 'delivered_at']
        widgets = {
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'carrier': forms.TextInput(attrs={'class': 'form-control'}),
            'package_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'shipped_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'delivered_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = ['title', 'description', 'slide_type', 'category', 'subcategory', 'product', 'custom_image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du slide'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description affichée sur le slide'}),
            'slide_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'custom_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ordre d\'affichage (1, 2, 3...)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'custom_image': 'Dimensions recommandees : 1920x500 pixels | Format : JPG ou PNG | Poids max : 200 KB',
        }

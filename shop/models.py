from django.db import models
from django.utils.text import slugify


class Category(models.Model):
 
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='categories', null=True, blank=True, verbose_name="Collection")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    show_in_ad_slider = models.BooleanField(default=False, verbose_name="Afficher dans le slider de publicité")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_essential = models.BooleanField(default=False, verbose_name="Sous-catégorie essentielle")
    show_on_homepage = models.BooleanField(default=False, verbose_name="Afficher sur la page d'accueil")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """
    Marque de produits
    """
    name = models.CharField(max_length=200, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name="Logo (Upload)")
    logo_url = models.URLField(blank=True, max_length=500, verbose_name="URL du Logo", help_text="URL directe de l'image du logo")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Type(models.Model):

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='types', null=True, blank=True, verbose_name="Marque")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='types', verbose_name="Sous-catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom du modèle")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        ordering = ['order', 'name']

    def __str__(self):
        if self.brand:
            return f"{self.brand.name} - {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Collection(models.Model):
    """
    Collection de produits
    """
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='collections/', blank=True, null=True, verbose_name="Image")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Produit
    """
    STATUS_CHOICES = [
        ('in_stock', 'En Stock'),
        ('out_of_stock', 'Rupture de Stock'),
        ('preorder', 'Précommande'),
        ('discontinued', 'Discontinué'),
    ]

    # Informations de base
    reference = models.CharField(max_length=100, unique=True, verbose_name="Référence")
    name = models.CharField(max_length=300, verbose_name="Nom")
    slug = models.SlugField(max_length=300, unique=True)
    
    # SEO et description
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Titre")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    description = models.TextField(verbose_name="Description")
    caracteristiques = models.TextField(blank=True, verbose_name="Caractéristiques")
    
    # Classification
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Catégorie")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Sous-catégorie")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Type")
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Collection")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Marque")
    brand_text = models.CharField(max_length=100, blank=True, verbose_name="Marque (texte)")
    
    # Prix et stock
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix Promo")
    quantity = models.IntegerField(default=0, verbose_name="Quantité")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock', verbose_name="Statut")
    
    # Caractéristiques spéciales
    is_bestseller = models.BooleanField(default=False, verbose_name="Best Seller")
    is_featured = models.BooleanField(default=False, verbose_name="Produit en vedette")
    is_new = models.BooleanField(default=False, verbose_name="Nouveau")
    show_in_ad_slider = models.BooleanField(default=False, verbose_name="Afficher dans le slider de publicité")
    
    # Images
    main_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image principale (deprecated)")
    
    # Métadonnées
    views_count = models.IntegerField(default=0, verbose_name="Nombre de vues")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Autres attributs (peut être étendu)
    warranty = models.CharField(max_length=200, blank=True, verbose_name="Garantie")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Poids (kg)")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.reference}-{self.name}")
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        """Retourne le prix final (avec ou sans promo)"""
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        """Calcule le pourcentage de réduction"""
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def get_main_image(self):
        """Retourne l'image principale du produit"""
        main_img = self.images.filter(is_main=True).first()
        if main_img:
            return main_img.image
        # Si pas d'image principale, prendre la première image
        first_img = self.images.first()
        if first_img:
            return first_img.image
        # Sinon retourner l'ancienne main_image si elle existe
        return self.main_image if self.main_image else None


class ProductImage(models.Model):
    """
    Images supplémentaires pour les produits
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produit")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Image")
    is_main = models.BooleanField(default=False, verbose_name="Image principale")
    order = models.IntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image du produit"
        verbose_name_plural = "Images des produits"
        ordering = ['order']

    def __str__(self):
        return f"Image de {self.product.name}"


class ProductSpecification(models.Model):
    """
    Caractéristiques du produit (clé-valeur)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name="Produit")
    key = models.CharField(max_length=200, verbose_name="Caractéristique")
    value = models.CharField(max_length=500, verbose_name="Valeur")
    order = models.IntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Spécification du produit"
        verbose_name_plural = "Spécifications des produits"
        ordering = ['order']

    def __str__(self):
        return f"{self.key}: {self.value}"


class HeroSlide(models.Model):
    """
    Slides pour le Hero Slider de la page d'accueil
    """
    SLIDE_TYPE_CHOICES = [
        ('category', 'Catégorie'),
        ('subcategory', 'Sous-catégorie'),
        ('product', 'Produit'),
    ]
    
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre", help_text="Titre affiché sur le slide (optionnel)")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Description affichée sur le slide")
    slide_type = models.CharField(max_length=20, choices=SLIDE_TYPE_CHOICES, verbose_name="Type de slide")
    
    # Relations - Un seul de ces champs doit être rempli selon le type
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='hero_slides', verbose_name="Catégorie")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='hero_slides', verbose_name="Sous-catégorie")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='hero_slides', verbose_name="Produit")
    
    # Image personnalisée (optionnel - sinon utilise l'image de la catégorie/produit)
    custom_image = models.ImageField(upload_to='hero_slides/', blank=True, null=True, verbose_name="Image personnalisée", help_text="Laissez vide pour utiliser l'image du produit/catégorie")
    
    # Paramètres
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage", help_text="Plus petit = affiché en premier")
    is_active = models.BooleanField(default=True, verbose_name="Actif", help_text="Désactiver pour masquer temporairement")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Slide Hero"
        verbose_name_plural = "Slides Hero"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.get_slide_type_display()} - {self.title}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Vérifier qu'un seul champ est rempli selon le type
        if self.slide_type == 'category' and not self.category:
            raise ValidationError({'category': 'Vous devez sélectionner une catégorie pour ce type de slide.'})
        if self.slide_type == 'subcategory' and not self.subcategory:
            raise ValidationError({'subcategory': 'Vous devez sélectionner une sous-catégorie pour ce type de slide.'})
        if self.slide_type == 'product' and not self.product:
            raise ValidationError({'product': 'Vous devez sélectionner un produit pour ce type de slide.'})
        
        # Vérifier que les autres champs sont vides
        if self.slide_type == 'category':
            if self.subcategory or self.product:
                raise ValidationError('Seule la catégorie doit être sélectionnée pour ce type de slide.')
        elif self.slide_type == 'subcategory':
            if self.category or self.product:
                raise ValidationError('Seule la sous-catégorie doit être sélectionnée pour ce type de slide.')
        elif self.slide_type == 'product':
            if self.category or self.subcategory:
                raise ValidationError('Seul le produit doit être sélectionné pour ce type de slide.')
    
    def get_image_url(self):
        """Retourne l'URL de l'image à afficher"""
        if self.custom_image:
            return self.custom_image.url
        
        if self.slide_type == 'category' and self.category and self.category.image:
            return self.category.image.url
        elif self.slide_type == 'subcategory' and self.subcategory and self.subcategory.image:
            return self.subcategory.image.url
        elif self.slide_type == 'product' and self.product:
            main_image = self.product.get_main_image
            if main_image:
                return main_image.url
        
        return None
    
    def get_link(self):
        """Retourne le lien vers l'élément"""
        if self.slide_type == 'category' and self.category:
            return f"/categorie/{self.category.slug}"
        elif self.slide_type == 'subcategory' and self.subcategory:
            return f"/sous-categorie/{self.subcategory.slug}"
        elif self.slide_type == 'product' and self.product:
            return f"/produit/{self.product.slug}"
        return "/"
    
    def get_display_title(self):
        """Retourne le titre à afficher (titre personnalisé ou nom de l'élément)"""
        if self.title:
            return self.title
        
        if self.slide_type == 'category' and self.category:
            return self.category.name
        elif self.slide_type == 'subcategory' and self.subcategory:
            return self.subcategory.name
        elif self.slide_type == 'product' and self.product:
            return self.product.name
        
        return "Découvrez nos produits"

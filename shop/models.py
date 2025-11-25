from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Catégorie principale: Composants, PC, Périphériques, Accessoires
    """
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
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
    """
    Sous-catégorie: Cartes Mères, Cartes Graphiques, Écran PC, Clavier PC, etc.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
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


class Type(models.Model):
    """
    Type/Marque de produit: Carte Mère AMD, Carte Mère Intel, GeForce GTX, etc.
    """
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='types', verbose_name="Sous-catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.subcategory.name} - {self.name}"

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
    
    # Prix et stock
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix Promo")
    quantity = models.IntegerField(default=0, verbose_name="Quantité")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock', verbose_name="Statut")
    
    # Caractéristiques spéciales
    is_bestseller = models.BooleanField(default=False, verbose_name="Best Seller")
    is_featured = models.BooleanField(default=False, verbose_name="Produit en vedette")
    is_new = models.BooleanField(default=False, verbose_name="Nouveau")
    
    # Images
    main_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image principale (deprecated)")
    
    # Métadonnées
    views_count = models.IntegerField(default=0, verbose_name="Nombre de vues")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Autres attributs (peut être étendu)
    brand = models.CharField(max_length=100, blank=True, verbose_name="Marque")
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

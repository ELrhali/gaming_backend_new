from django.db import models
from shop.models import Product


class Customer(models.Model):
    """
    Informations client pour les commandes
    """
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Adresse
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Code postal")
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"


class Order(models.Model):
    """
    Commande
    """
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('preparing', 'En préparation'),
        ('ready', 'Prête à livrer'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Paiement à la livraison (COD)'),
    ]

    # Numéro de commande
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de commande")
    
    # Client
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Client")
    
    # Statut et paiement
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod', verbose_name="Mode de paiement")
    
    # Montants
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais de livraison")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    # Notes
    customer_notes = models.TextField(blank=True, verbose_name="Notes du client")
    admin_notes = models.TextField(blank=True, verbose_name="Notes admin")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de confirmation")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.order_number} - {self.customer}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Générer un numéro de commande unique
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.order_number = f"CMD-{timestamp}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Article de commande
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    
    # Informations au moment de la commande
    product_name = models.CharField(max_length=300, verbose_name="Nom du produit")
    product_reference = models.CharField(max_length=100, verbose_name="Référence")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Calculer le prix total
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Delivery(models.Model):
    """
    Livraison
    """
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_transit', 'En cours de livraison'),
        ('delivered', 'Livré'),
        ('failed', 'Échec de livraison'),
        ('returned', 'Retourné'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery', verbose_name="Commande")
    
    # Informations de livraison
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Numéro de suivi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    
    # Dates
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'expédition")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de livraison")
    
    # Informations de colis
    package_count = models.IntegerField(default=1, verbose_name="Nombre de colis")
    carrier = models.CharField(max_length=100, blank=True, verbose_name="Transporteur")
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-created_at']

    def __str__(self):
        return f"Livraison pour {self.order.order_number}"


class DeliveryHistory(models.Model):
    """
    Historique des livraisons
    """
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='history', verbose_name="Livraison")
    status = models.CharField(max_length=20, verbose_name="Statut")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique de livraison"
        verbose_name_plural = "Historiques de livraison"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.delivery} - {self.status} - {self.created_at}"

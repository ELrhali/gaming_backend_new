from rest_framework import serializers
from .models import Customer, Order, OrderItem, Delivery
from shop.serializers import ProductListSerializer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer pour les clients"""
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'email',
            'address', 'city', 'postal_code', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer pour les articles de commande"""
    product_details = ProductListSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_details', 'product_name', 
            'product_reference', 'unit_price', 'quantity', 'total_price'
        ]
        read_only_fields = ['product_name', 'product_reference', 'total_price']

    def create(self, validated_data):
        # Récupérer les informations du produit au moment de la commande
        product = validated_data['product']
        validated_data['product_name'] = product.name
        validated_data['product_reference'] = product.reference
        validated_data['unit_price'] = float(product.final_price or product.price)
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer pour les commandes"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.IntegerField(write_only=True, required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_id', 'items',
            'status', 'status_display', 'payment_method', 'payment_method_display',
            'subtotal', 'shipping_cost', 'total', 'customer_notes', 'admin_notes',
            'created_at', 'updated_at', 'confirmed_at'
        ]
        read_only_fields = ['order_number', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer pour créer une commande complète"""
    # Informations client
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    # Articles de commande
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    # Mode de paiement
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, default='cod')

    def validate_items(self, value):
        """Valider les articles de commande"""
        if not value:
            raise serializers.ValidationError("La commande doit contenir au moins un article")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Chaque article doit avoir un product_id et une quantité")
            
            try:
                quantity = int(item['quantity'])
                if quantity < 1:
                    raise serializers.ValidationError("La quantité doit être au moins 1")
            except ValueError:
                raise serializers.ValidationError("La quantité doit être un nombre entier")
        
        return value

    def create(self, validated_data):
        """Créer une nouvelle commande avec client et articles"""
        from shop.models import Product
        from decimal import Decimal
        
        # Extraire les items
        items_data = validated_data.pop('items')
        
        # Créer le client
        customer_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'phone': validated_data['phone'],
            'email': validated_data.get('email', ''),
            'address': validated_data['address'],
            'city': validated_data['city'],
            'postal_code': validated_data.get('postal_code', ''),
            'notes': validated_data.get('notes', ''),
        }
        customer = Customer.objects.create(**customer_data)
        
        # Calculer le total
        subtotal = Decimal('0.00')
        order_items = []
        
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = int(item_data['quantity'])
                unit_price = Decimal(str(product.final_price or product.price))
                total_price = unit_price * quantity
                
                order_items.append({
                    'product': product,
                    'product_name': product.name,
                    'product_reference': product.reference,
                    'unit_price': unit_price,
                    'quantity': quantity,
                    'total_price': total_price
                })
                
                subtotal += total_price
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Produit {item_data['product_id']} introuvable")
        
        # Créer la commande
        shipping_cost = Decimal('0.00')  # Livraison gratuite
        total = subtotal + shipping_cost
        
        order = Order.objects.create(
            customer=customer,
            status='pending',
            payment_method=validated_data.get('payment_method', 'cod'),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            customer_notes=validated_data.get('notes', '')
        )
        
        # Créer les articles de commande
        for item_data in order_items:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class DeliverySerializer(serializers.ModelSerializer):
    """Serializer pour les livraisons"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    customer_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'order_number', 'customer_name',
            'tracking_number', 'status', 'status_display',
            'shipped_at', 'delivered_at', 'package_count',
            'carrier', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return f"{obj.order.customer.first_name} {obj.order.customer.last_name}"

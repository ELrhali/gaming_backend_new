from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Customer, Order, OrderItem, Delivery
from .serializers import (
    CustomerSerializer, OrderSerializer, OrderItemSerializer,
    CreateOrderSerializer, DeliverySerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API ViewSet pour les clients
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Recherche par téléphone ou email
        phone = self.request.query_params.get('phone', None)
        email = self.request.query_params.get('email', None)
        
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    """
    API ViewSet pour les commandes
    """
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par statut
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filtrer par numéro de commande
        order_number = self.request.query_params.get('order_number', None)
        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
        
        # Filtrer par téléphone client
        phone = self.request.query_params.get('phone', None)
        if phone:
            queryset = queryset.filter(customer__phone__icontains=phone)
        
        return queryset
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_order(self, request):
        """
        Créer une nouvelle commande complète
        POST /api/orders/create/
        Body: {
            "first_name": "...",
            "last_name": "...",
            "phone": "...",
            "email": "...",
            "address": "...",
            "city": "...",
            "postal_code": "...",
            "notes": "...",
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 3, "quantity": 1}
            ],
            "payment_method": "cod"
        }
        """
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm_order(self, request, pk=None):
        """
        Confirmer une commande
        POST /api/orders/{id}/confirm/
        """
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'confirmed'
            from django.utils import timezone
            order.confirmed_at = timezone.now()
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        return Response(
            {'error': 'La commande ne peut pas être confirmée dans cet état'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        """
        Annuler une commande
        POST /api/orders/{id}/cancel/
        """
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        return Response(
            {'error': 'La commande ne peut pas être annulée dans cet état'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Mettre à jour le statut d'une commande
        PATCH /api/orders/{id}/update-status/
        Body: {"status": "preparing"}
        """
        order = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Statut invalide. Choix valides: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        if new_status == 'confirmed' and not order.confirmed_at:
            from django.utils import timezone
            order.confirmed_at = timezone.now()
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet pour les articles de commande (lecture seule)
    """
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par commande
        order_id = self.request.query_params.get('order', None)
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        return queryset


class DeliveryViewSet(viewsets.ModelViewSet):
    """
    API ViewSet pour les livraisons
    """
    queryset = Delivery.objects.select_related('order__customer').all()
    serializer_class = DeliverySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par statut
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filtrer par numéro de suivi
        tracking = self.request.query_params.get('tracking', None)
        if tracking:
            queryset = queryset.filter(tracking_number__icontains=tracking)
        
        return queryset

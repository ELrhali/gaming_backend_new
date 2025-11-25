from django.contrib import admin
from .models import Customer, Order, OrderItem, Delivery, DeliveryHistory


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'city', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_filter = ['city', 'created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'total', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'customer__first_name', 'customer__last_name', 'customer__phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('order_number', 'customer', 'status', 'payment_method')
        }),
        ('Montants', {
            'fields': ('subtotal', 'shipping_cost', 'total')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'confirmed_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_reference', 'product_name', 'quantity', 'unit_price', 'total_price']
    search_fields = ['product_reference', 'product_name', 'order__order_number']


class DeliveryHistoryInline(admin.TabularInline):
    model = DeliveryHistory
    extra = 1


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'status', 'carrier', 'shipped_at', 'delivered_at']
    list_filter = ['status', 'carrier', 'created_at']
    search_fields = ['tracking_number', 'order__order_number']
    inlines = [DeliveryHistoryInline]
    
    fieldsets = (
        ('Commande', {
            'fields': ('order',)
        }),
        ('Informations de livraison', {
            'fields': ('tracking_number', 'status', 'carrier', 'package_count')
        }),
        ('Dates', {
            'fields': ('shipped_at', 'delivered_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

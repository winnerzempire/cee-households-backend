from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductAttribute, ProductReview, Cart, CartItem, Order, OrderItem, Wishlist, ShippingAddress

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'featured', 'active', 'order', 'created_at']
    list_filter = ['featured', 'active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['featured', 'active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'image', 'parent')
        }),
        ('Settings', {
            'fields': ('featured', 'active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'price', 
        'compare_price', 'stock', 'featured', 'best_seller', 
        'new_arrival', 'active', 'created_at'
    ]
    list_filter = [
        'category', 'featured', 'best_seller', 
        'new_arrival', 'active', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = [
        'price', 'compare_price', 'stock', 'featured', 
        'best_seller', 'new_arrival', 'active'
    ]
    inlines = [ProductImageInline, ProductAttributeInline]
    readonly_fields = ['created_at', 'updated_at', 'view_main_image']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        ('Relationships', {
            'fields': ('category',)
        }),
        ('Inventory', {
            'fields': ('stock', 'low_stock_threshold')
        }),
        ('Flags', {
            'fields': ('featured', 'best_seller', 'new_arrival', 'active', 'on_sale')
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'dimensions')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description')
        }),
        ('Images', {
            'fields': ('main_image', 'view_main_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def view_main_image(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.main_image.url)
        return "-"
    view_main_image.short_description = 'Preview'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['order']

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value']
    list_filter = ['name']
    search_fields = ['product__name', 'name', 'value']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'verified_purchase', 'created_at']
    list_filter = ['rating', 'verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_quantity', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def total_quantity(self, obj):
        return obj.total_quantity
    total_quantity.short_description = 'Items'
    
    def total_price(self, obj):
        return f"KSh {obj.total_price:,.2f}"
    total_price.short_description = 'Total'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'payment_status', 
        'total_amount_display', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'customer_email']
    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 
        'paid_at', 'delivered_at', 'cancelled_at'
    ]
    inlines = [OrderItemInline]
    list_editable = ['status', 'payment_status']
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('customer_email', 'customer_phone')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Payment', {
            'fields': ('transaction_id', 'payment_details')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'delivered_at', 'cancelled_at')
        }),
    )
    
    def total_amount_display(self, obj):
        return f"KSh {obj.total_amount:,.2f}"
    total_amount_display.short_description = 'Total Amount'
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f"{queryset.count()} orders marked as processing.")
    mark_as_processing.short_description = "Mark selected orders as Processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'city', 'is_default', 'created_at']
    list_filter = ['city', 'state', 'country', 'is_default']
    search_fields = ['user__username', 'first_name', 'last_name', 'city']
    list_editable = ['is_default']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'email')
        }),
        ('Address Details', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Settings', {
            'fields': ('is_default',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
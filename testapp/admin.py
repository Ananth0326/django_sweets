# In testapp/admin.py
from django.contrib import admin
from .models import Sweet, Order, OrderItem # <-- Make sure to import OrderItem

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'is_best_seller')
    list_filter = ('category', 'available', 'is_best_seller')
    search_fields = ('name',)

# --- (START) REPLACE YOUR OLD ORDERADMIN WITH THIS ---

# This creates an inline table to show items *inside* the Order page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # These fields will be shown for each item in the order
    readonly_fields = ('sweet_name', 'weight', 'quantity', 'price')
    extra = 0 # Don't show extra blank forms
    can_delete = False # Don't allow deleting items from the admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # These are the fields from your NEW Order model
    list_display = ('id', 'name', 'mobile', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'mobile', 'id')
    
    # This adds the table of items (from above) onto this page
    inlines = [OrderItemInline]

# --- (END) REPLACEMENT ---
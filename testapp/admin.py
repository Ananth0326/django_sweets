# In store/admin.py
from django.contrib import admin
from .models import Sweet, Order, OrderItem

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    # These fields (available, is_best_seller) now exist in your models.py
    list_display = ('name', 'category', 'price', 'available', 'is_best_seller', 'is_featured')
    list_filter = ('category', 'available', 'is_best_seller', 'is_featured')
    search_fields = ('name',)
    list_editable = ('price', 'available', 'is_best_seller', 'is_featured') # Makes them easy to change!

# This creates an inline table to show items *inside* the Order page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
    # --- FIX ---
    # The fields in your OrderItem model are 'name' and 'weight_gm'
    # 'sweet_name' is changed to 'name'
    # 'weight' is changed to 'weight_gm'
    readonly_fields = ('name', 'weight_gm', 'quantity', 'price')
    # --- END FIX ---

    extra = 0 # Don't show extra blank forms
    can_delete = False # Don't allow deleting items from the admin
    
    # Optional: make it so you can't add new items from here
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # These are the fields from your NEW Order model
    list_display = ('id', 'name', 'mobile', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'mobile', 'id')
    readonly_fields = ('name', 'mobile', 'address', 'total_price', 'created_at')
    
    # This adds the table of items (from above) onto this page
    inlines = [OrderItemInline]

    # Don't allow adding new orders from the admin
    def has_add_permission(self, request):
        return False


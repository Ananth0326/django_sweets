from django.db import models
from django.conf import settings # Good practice to import settings

class Sweet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Base price (for 250gm)
    image = models.ImageField(upload_to='sweets/')
    
    # NEW FIELD FOR FEATURED SWEET
    is_featured = models.BooleanField(default=False, help_text="Check this to feature on homepage")
    
    # --- ADDED FIELDS TO FIX ADMIN ERRORS ---
    available = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False, help_text="Check this for best-seller carousel")
    # --- END OF ADDED FIELDS ---

    # This is an example, adjust choices as needed
    CATEGORY_CHOICES = [
        ('dryfruit', 'Dry Fruit Sweets'),
        ('milk', 'Milk Sweets'),
        ('ghee', 'Ghee Sweets'),
        ('ragi', 'Ragi Sweets'),
        ('burfi_halwa', 'Burfi & Halwa'),
        ('sugarfree', 'Sugar Free'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

# --- NEW MODELS TO FIX THE ERROR ---

class Order(models.Model):
    # If you had user accounts, you would link it with:
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    # Customer details (for a simple checkout form)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # You could add a status field
    # STATUS_CHOICES = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    sweet = models.ForeignKey(Sweet, on_delete=models.SET_NULL, null=True, blank=True) # Use SET_NULL so if a sweet is deleted, the order history remains
    
    name = models.CharField(max_length=100) # Store name in case sweet is deleted
    quantity = models.IntegerField(default=1)
    weight_gm = models.IntegerField(default=250) # Store the chosen weight (e.g., 250, 500, 1000)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price for this single line item (quantity * weight_price)

    def __str__(self):
        return f"{self.quantity} x {self.name} ({self.weight_gm}gm) for Order {self.order.id}"



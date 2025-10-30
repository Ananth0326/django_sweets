# In testapp/models.py
from django.db import models

class Sweet(models.Model):
    CATEGORY_CHOICES = [
        ('milk', 'Milk Sweets'),
        ('dryfruit', 'Dry Fruit Sweets'),
        ('ghee', 'Ghee Sweets'),
        ('ragi', 'Ragi Sweets'),
        ('burfi_halwa', 'Burfi & Halwa'),
        ('sugarfree', 'Sugar-Free Sweets'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) # This is your base price (e.g., for 250gm)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='sweet_images/')
    available = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# --- (START) REPLACE YOUR OLD ORDER MODEL WITH THESE TWO ---

# NEW: This model stores the customer's information
class Order(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.name}"

# NEW: This model stores each item *inside* an Order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    sweet_name = models.CharField(max_length=100)
    weight = models.CharField(max_length=50) # e.g., "250gm", "1kg"
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price for this item line (e.g., 1kg of Kaju Katli)

    def __str__(self):
        return f"{self.quantity} x {self.sweet_name} ({self.weight})"

# --- (END) REPLACEMENT ---
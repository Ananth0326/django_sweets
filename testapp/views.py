# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Sweet
from .forms import CheckoutForm
from .models import Sweet, Order, OrderItem
def sweet_list(request):
    category = request.GET.get('category')
    if category and category != 'all':
        sweets = Sweet.objects.filter(category=category, available=True)
    else:
        sweets = Sweet.objects.filter(available=True)
    return render(request, 'testapp/sweet_list.html', {'sweets': sweets})

def sweet_detail(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    return render(request, 'testapp/sweet_detail.html', {'sweet': sweet})

def place_order(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.sweet = sweet
            order.save()
            return redirect('sweet_list')
    else:
        form = OrderForm()
    return render(request, 'testapp/order_form.html', {'form': form, 'sweet': sweet})

def home(request):
    # --- CHANGED THIS LINE ---
    # Gets 10 random sweets from the Sweet model
    best_sellers = Sweet.objects.order_by('?')[:10] 
    # --- END OF CHANGE ---
    return render(request, 'testapp/home.html', {'best_sellers': best_sellers})
def add_to_cart(request, sweet_id):
    """
    Adds a sweet to the cart stored in the session.
    The cart is a dictionary. The key is a unique ID (sweet_id + weight_multiplier).
    """
    sweet = get_object_or_404(Sweet, id=sweet_id)
    
    # Get the cart from the session, or create an empty dict if it doesn't exist
    cart = request.session.get('cart', {})
    
    # Get the data from the form POST
    multiplier = request.POST.get('weight_multiplier') # e.g., "1", "2", or "4"
    quantity = int(request.POST.get('quantity', 1))

    # We need the text ("250gm", "500gm") for the cart page display
    weight_text_map = {'1': '250gm', '2': '500gm', '4': '1kg'}
    weight_text = weight_text_map.get(multiplier, '250gm')
    
    # Create a unique ID for this specific item (e.g., sweet 7 at 500gm)
    cart_item_id = f"{sweet_id}_{multiplier}"
    
    if cart_item_id in cart:
        # If it's already in the cart, just add to the quantity
        cart[cart_item_id]['quantity'] += quantity
    else:
        # If not, add it as a new item
        cart[cart_item_id] = {
            'sweet_id': sweet.id,
            'name': sweet.name,
            'weight': weight_text,
            'multiplier': multiplier,
            'quantity': quantity,
            'price': float(sweet.price), # This is the base price (for 250gm)
        }
    
    # Save the updated cart back into the session
    request.session['cart'] = cart
    
    # Redirect the user to the cart page
    return redirect('cart_view')


def cart_view(request):
    """
    Displays the contents of the cart.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_cart_price = 0
    
    # Loop through the items in the session cart
    for item_id, item_data in cart.items():
        # Calculate the total price for this line item
        total_item_price = item_data['price'] * float(item_data['multiplier']) * item_data['quantity']
        
        # Add to our list to send to the template
        cart_items.append({
            'item_id': item_id,
            'name': item_data['name'],
            'weight': item_data['weight'],
            'quantity': item_data['quantity'],
            'total_price': total_item_price,
        })
        # Add to the grand total
        total_cart_price += total_item_price
        
    return render(request, 'testapp/cart.html', {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price
    })


def checkout_view(request):
    """
    Handles the checkout form and creates the final Order.
    """
    cart = request.session.get('cart', {})
    if not cart:
        # Can't checkout if the cart is empty, redirect to cart page
        return redirect('cart_view') 

    # --- Calculate totals again (so user can't tamper with prices) ---
    cart_items_for_order = []
    total_cart_price = 0
    
    for item_id, item_data in cart.items():
        base_price = float(get_object_or_404(Sweet, id=item_data['sweet_id']).price)
        multiplier = float(item_data['multiplier'])
        quantity = int(item_data['quantity'])
        
        price_per_unit = base_price * multiplier
        total_item_price = price_per_unit * quantity

        cart_items_for_order.append({
            'name': item_data['name'],
            'weight': item_data['weight'],
            'quantity': quantity,
            'price_per_unit': price_per_unit, # The price for one item (e.g., 1kg)
        })
        total_cart_price += total_item_price
    # --- End calculation ---

    if request.method == 'POST':
        # User submitted the form
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # 1. Create the main Order object
            order = form.save(commit=False)
            order.total_price = total_cart_price
            order.save()
            
            # 2. Create an OrderItem for each item in the cart
            for item in cart_items_for_order:
                OrderItem.objects.create(
                    order=order,
                    sweet_name=item['name'],
                    weight=item['weight'],
                    quantity=item['quantity'],
                    price=item['price_per_unit'] # Save the price per unit
                )
            
            # 3. Clear the cart from the session
            del request.session['cart']
            
            # 4. Redirect to a success page
            return redirect('order_success', order_id=order.id)
    else:
        # User is just visiting the page, show a blank form
        form = CheckoutForm()

    return render(request, 'testapp/checkout.html', {'form': form})


def order_success_view(request, order_id):
    """
    Displays the "Thank You" page after a successful order.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'testapp/order_success.html', {'order': order})
def remove_from_cart(request, item_id):
    """
    Removes an item from the cart in the session.
    """
    cart = request.session.get('cart', {})
    
    # Check if the item is in the cart and remove it if it exists
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        
    # Redirect back to the cart page
    return redirect('cart_view')
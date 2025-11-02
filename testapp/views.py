from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Sweet, Order, OrderItem
from .forms import CheckoutForm


# ---------------------------
# 🏠 HOME PAGE
# ---------------------------
def home(request):
    best_sellers = Sweet.objects.filter(is_best_seller=True, available=True)
    featured_sweet = Sweet.objects.filter(is_featured=True, available=True).first()
    
    return render(request, 'testapp/home.html', {
        'best_sellers': best_sellers,
        'featured_sweet': featured_sweet
    })


# ---------------------------
# 🍬 SWEET LIST
# ---------------------------
def sweet_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('q')

    sweets = Sweet.objects.filter(available=True)

    if search_query:
        sweets = sweets.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category and category != 'all':
        sweets = sweets.filter(category=category)

    return render(request, 'testapp/sweet_list.html', {
        'sweets': sweets,
        'search_query': search_query
    })


# ---------------------------
# 🍭 SWEET DETAIL
# ---------------------------
def sweet_detail(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    return render(request, 'testapp/sweet_detail.html', {'sweet': sweet})


# ---------------------------
# 🛒 CART (Non-AJAX Version)
# ---------------------------
def add_to_cart(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    cart = request.session.get('cart', {})

    multiplier = request.POST.get('weight_multiplier', '1')
    quantity = int(request.POST.get('quantity', 1))
    weight_text_map = {'1': '250gm', '2': '500gm', '4': '1kg'}
    weight_text = weight_text_map.get(multiplier, '250gm')

    cart_item_id = f"{sweet_id}_{multiplier}"

    if cart_item_id in cart:
        cart[cart_item_id]['quantity'] += quantity
    else:
        cart[cart_item_id] = {
            'sweet_id': sweet.id,
            'name': sweet.name,
            'weight': weight_text,
            'multiplier': multiplier,
            'quantity': quantity,
            'price': float(sweet.price),
        }

    request.session['cart'] = cart
    return redirect('cart_view')


# ---------------------------
# 🧺 CART VIEW
# ---------------------------
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_cart_price = 0

    for item_id, item_data in cart.items():
        total_item_price = (
            item_data['price']
            * float(item_data['multiplier'])
            * item_data['quantity']
        )
        cart_items.append({
            'item_id': item_id,
            'name': item_data['name'],
            'weight': item_data['weight'],
            'quantity': item_data['quantity'],
            'total_price': total_item_price,
        })
        total_cart_price += total_item_price

    return render(request, 'testapp/cart.html', {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price
    })


# ---------------------------
# 💳 CHECKOUT VIEW (FIXED)
# ---------------------------
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')

    cart_items_for_order = []
    total_cart_price = 0

    # 🧮 Recalculate securely from DB
    for item_id, item_data in cart.items():
        try:
            sweet = Sweet.objects.get(id=item_data['sweet_id'])
            base_price = float(sweet.price)
        except Sweet.DoesNotExist:
            continue

        multiplier = float(item_data['multiplier'])
        quantity = int(item_data['quantity'])
        price_per_unit = base_price * multiplier
        total_item_price = price_per_unit * quantity

        cart_items_for_order.append({
            'name': item_data['name'],
            'weight': item_data['weight'],  # e.g. "250gm"
            'quantity': quantity,
            'price_per_unit': price_per_unit,
            'total_price': total_item_price,
        })
        total_cart_price += total_item_price

    # 🧾 Handle form submit
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_cart_price
            order.save()

            # 🧠 Convert weight "250gm" → 250 before saving
            for item in cart_items_for_order:
                weight_value = item['weight']
                if isinstance(weight_value, str):
                    weight_value = ''.join(filter(str.isdigit, weight_value)) or 0

                OrderItem.objects.create(
                    order=order,
                    name=item['name'],
                    weight_gm=int(weight_value),
                    quantity=item['quantity'],
                    price=item['price_per_unit']
                )

            # 🧹 Clear cart after success
            if 'cart' in request.session:
                del request.session['cart']

            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'testapp/checkout.html', {
        'form': form,
        'cart_items': cart_items_for_order,
        'total_cart_price': total_cart_price
    })


# ---------------------------
# ✅ ORDER SUCCESS
# ---------------------------
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'testapp/order_success.html', {'order': order})


# ---------------------------
# ❌ REMOVE FROM CART
# ---------------------------
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('cart_view')


# ---------------------------
# ⚡ AJAX API: Add to Cart
# ---------------------------
def add_to_cart_ajax(request, sweet_id):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    try:
        sweet = get_object_or_404(Sweet, id=sweet_id)
        cart = request.session.get('cart', {})

        multiplier = request.POST.get('weight_multiplier', '1')
        quantity = int(request.POST.get('quantity', 1))
        weight_text_map = {'1': '250gm', '2': '500gm', '4': '1kg'}
        weight_text = weight_text_map.get(multiplier, '250gm')

        cart_item_id = f"{sweet_id}_{multiplier}"

        if cart_item_id in cart:
            cart[cart_item_id]['quantity'] += quantity
        else:
            cart[cart_item_id] = {
                'sweet_id': sweet.id,
                'name': sweet.name,
                'weight': weight_text,
                'multiplier': multiplier,
                'quantity': quantity,
                'price': float(sweet.price),
            }

        request.session['cart'] = cart

        new_cart_count = sum(item['quantity'] for item in cart.values())
        return JsonResponse({'status': 'success', 'new_cart_count': new_cart_count})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# ---------------------------
# ⚡ AJAX API: Cart Count
# ---------------------------
def get_cart_count_api(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': count})

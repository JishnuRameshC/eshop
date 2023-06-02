from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem,Order, OrderItem, Customer
from datetime import datetime
from django.db.models import F, Sum
from django .urls import reverse
from decimal import Decimal
from .forms import OrderForm
from django.contrib.auth.decorators import login_required


from django.contrib import messages
# Create your views here.
def calculate_total(price, quantity):
    return price * quantity


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app1/product.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request,'app1/product_list.html',{'products':products})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product already exists in the cart
    try:
        cart_item = cart.cartitem_set.get(product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the product doesn't exist, create a new CartItem
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    
    return redirect('view-cart')




def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()

    # Update the total price of the cart
    cart = item.cart
    cart.total_price = cart.calculate_total_price()
    cart.save()

    return redirect('view-cart')





def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        
        # Update the total price of the cart
        cart = item.cart
        cart.total_price -= cart.calculate_total_price()
        cart.save()
    else:
        item.delete()

    return redirect('view-cart')



def view_cart(request):
    # Retrieve the cart for the current user
    cart = get_object_or_404(Cart, user=request.user)

    # Retrieve the items in the cart and order them by their ID or any other desired criteria
    items = cart.cartitem_set.all().order_by('id')

    # Calculate the total price for each item
    for item in items:
        item.total_price = item.product.price * item.quantity

    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'app1/cart.html', context)


def order(request, product_id):
    # Retrieve the product
    product = get_object_or_404(Product, pk=product_id)

    # Create a new cart or retrieve the existing cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create a new cart item and associate it with the product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Increase the quantity of the cart item by 1
    cart_item.quantity += 1
    cart_item.save()

    # Calculate the total price of the cart
    cart.total_price += product.price
    cart.save()

    # Redirect to the cart view
    return redirect('view-cart')


from django.shortcuts import render, redirect
from .forms import OrderForm

def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process the order and save it to the database
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            order = Order(
                name=name,
                email=email,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                total_price=total_price  # Assuming you have a total_price field in your Order model
            )
            order.save()

            # Redirect to a success page or return a response
            return redirect('success_page')  # Replace 'success_page' with the URL name of your success page

    else:
        form = OrderForm()

    context = {'form': form, 'total_price': total_price}
    return render(request, 'app1/place_order.html', context)



@login_required
def submit_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Get the current user
            user = request.user
            
            # Create a new customer object
            customer = Customer(user=user)
            customer.name = form.cleaned_data['name']
            customer.email = form.cleaned_data['email']
            customer.address = form.cleaned_data['address']
            customer.city = form.cleaned_data['city']
            customer.state = form.cleaned_data['state']
            customer.zipcode = form.cleaned_data['zipcode']
            customer.save()

            # Process the order
            # ...

            return redirect('order-success')  # Replace with your success URL

    else:
        form = OrderForm()

    context = {
        'form': form,
        'total_price': cart.total_price(),
    }
    return render(request, 'submit_order.html', context)



def order_success(request):
    order = Order.objects.last() 
    return render(request, 'app1/order_success.html', {'order': order})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'app1/order_confirmation.html', {'order': order})


def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')
    context = {'orders': orders}
    return render(request, 'order_history.html', context)

def thank_you(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'app1/thank_you.html', {'order': order})




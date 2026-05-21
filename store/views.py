from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitem_set.all()
    return render(request, 'store/cart.html', {'items': items, 'order': order})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def checkout(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    if request.method == 'POST':
        order.complete = True
        order.save()
        return redirect('home')
    return render(request, 'store/checkout.html', {'order': order})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

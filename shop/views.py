from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404

from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    men_categories = Category.objects.filter(gender='men')
    women_categories = Category.objects.filter(gender='women')
    trending_products = Product.objects.filter(is_trending=True)

    return render(request, 'shop/index.html', {
        'men_categories': men_categories,
        'women_categories': women_categories,
        'trending_products': trending_products,
    
    })


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
        if results.exists():
            return render(request, 'shop/search_results.html', {'results': results, 'query': query})
        else:
            return redirect('home')  # Redirect if no products found
    return redirect('home')  # Redirect if query is empty

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout successful')
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/login')
    return render(request,'shop/login.html')

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful you can login now')
            return redirect('/login')
    return render(request,'shop/register.html',{
        'form': form
    })


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'product_qty': 1}
        )
        if not created:
            cart_item.product_qty += 1
            cart_item.save()
        return redirect('cart')
    else:
        return redirect('login')
    
def remove_from_cart(request, cart_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart_item.delete()
        return redirect('cart')
    else:
        return redirect('login')
    

def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_total = sum(item.product.price * item.product_qty for item in cart_items)
        return render(request, 'shop/cart.html', {
            'cart_items': cart_items,
            'cart_total': cart_total
        })
    else:
        return redirect('login')
    
    
def cart_items_processor(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []
    return {'cart_items': cart_items}


def cart_products_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    for item in cart_items:
        item.subtotal = item.product.price * item.product_qty
    return render(request, 'shop/cart_products.html', {'cart_items': cart_items})


def men_store(request):
    men_categories = Category.objects.filter(gender='men')
    return render(request,'shop/men_store.html',{
        'men_categories': men_categories,})

def women_store(request):
    women_categories = Category.objects.filter(gender='women')
    return render(request,'shop/women_store.html',{
        'women_categories': women_categories,})

def collectionsView(request,name,):
    if (Category.objects.filter(name=name)):
        Products = Product.objects.filter(category__name=name)
        return render(request,'shop/products/index.html',{
            'products': Products,
            'category_name': name,})
    else:
        messages.warning(request,'Category Not Found')
        return redirect(request,'/')
    
def product_details(request, cname, pname):
    category = Category.objects.filter(name=cname).first()
    if not category:
        messages.error(request, 'Category not found')
        return redirect('/')

    product = Product.objects.filter(name=pname, category=category).first()
    if not product:
        messages.error(request, 'Product not found')
        return redirect('/')

    similar_products = Product.objects.filter(category=category).exclude(name=pname)[:4]

    return render(request, 'shop/products/product_details.html', {
        'product': product,
        'similar_products': similar_products,
        'category_name': category.name,
    })



def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})





@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    products = wishlist.products.all() if wishlist else []
    return render(request, 'shop/wishlist.html', {'products': products})


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.filter(id=product_id).first()
    if not product:
        messages.error(request, "The product does not exist.")
        return redirect('wishlist')

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)

    messages.success(request, "Product added to your wishlist.")
    return redirect('wishlist')


def remove_from_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/?next={request.META.get("HTTP_REFERER", "/")}')

    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    if wishlist:
        wishlist.products.remove(product)

    # 🔁 Return to the page the user was on
    return redirect('wishlist')
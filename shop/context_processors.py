from .models import Cart  # Use the correct name

def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        return {'cart_items': cart_items}
    return {'cart_items': []}

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('cart_products/', views.cart_products_view, name='cart_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('men_store', views.men_store, name='men_store'),
    path('women_store', views.women_store, name='women_store'),
    path('men_store/<str:name>', views.collectionsView, name='men_store'),
    path('women_store/<str:name>', views.collectionsView, name='women_store'),
    path('product/<str:cname>/<str:pname>/', views.product_details, name='product_details'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

   
 ]

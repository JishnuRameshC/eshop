from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name="product-list"),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease-quantity'),
    path('order-history/', views.order_history, name='order-history'),
    path('place-order/', views.place_order, name='place-order'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('thank-you/<int:order_id>/<int:total_price>/<str:order_date>/', views.thank_you, name='thank-you'),
    path('order/<int:product_id>/', views.order, name='order'), 
    path('order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/success/', views.order_success, name='order-success'),

    path('login/',views.login_page,name='login'),
    path('logout/',views.LogoutPage,name='logout'), 
    path('signup/',views.signup_page,name="signup"),
]


from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.home),
    path('add_category/',views.add_category, name='add_cat'),
    path('view_category/',views.category_view,name='view_cat'),
    path('edit_cate/<int:id>/', views.edit_category, name='edit_cate'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('add_menu/',views.add_menu,name='add_menu'),
    path('view_menu/',views.view_menu,name='view_menu'),
    path('edit_menu/<int:id>/',views.edit_menu,name='edit_menu'),
    path('delete_menu/<int:id>/', views.delete_menu, name='delete_menu'),
    path('a_view_review/', views.a_view_review, name='a_view_review'),
    path('view_orders/', views.view_orders, name='view_orders'), 
   
    path('view_pending_orders/', views.view_pending_orders, name='view_pending_orders'),
    path( 'view_delivered_orders/',views.view_delivered_orders,name='view_delivered_orders'),

    path('add_table/', views.add_table, name='add_table'),

    path('view_table_booking/', views.view_table_booking, name='view_table_booking'),   
    path(
    'update-order-status/<int:order_id>/',
    views.update_order_status,
    name='update_order_status'
),
path(
    'update-booking-status/<int:booking_id>/',
    views.update_booking_status,
    name='update_booking_status'
),
    path('delete_table/<int:id>/', views.delete_table, name='delete_table'),


    ######################### dashbord  ####################################################################################################################

path(
    'admin_dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
    #######################################################################################################################################################

       ##USER
       #     
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('',views.user_home,name='u_home'),
    path('menu/', views.menu, name='menu'),
    path('product/<int:id>/',views.product_details, name='product_details'),

    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),

   path('cart/',views.cart,name='cart'),
   path('remove-cart-item/<int:id>/',views.remove_cart_item, name='remove_cart_item'),

   path( 'increase-quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),

   path('decrease-quantity/<int:id>/', views.decrease_quantity,  name='decrease_quantity'),
   path( 'checkout/', views.checkout, name='checkout'),
   path('payment/<int:order_id>/', views.payment_gateway, name='payment_gateway'),

    path('my_orders/',views.my_orders,name='my_orders'),
    path( 'order_success/', views.order_success,name='order_success'),

    path(  'book_table/', views.book_table, name='book_table'),

    path( 'my_bookings/',   views.my_bookings,    name='my_bookings'),

path('add-review/<int:id>/', views.add_review, name='add_review'),

path( 'profile/', views.profile,  name='profile'),
path('review/',views.view_review,name='review')

   
            ]

# cafe_app (addmin)/urls.py

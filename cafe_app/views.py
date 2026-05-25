import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import timedelta
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
#category

#add category
def add_category(request):

    if request.method == 'POST':

        category = request.POST.get('category')

        Category.objects.create(name=category)
        

    return render(request, 'c_admin/add_category.html')    

#view category
def category_view(request):

    categories = Category.objects.all()

    return render(request, 'c_admin/view_category.html', {'categories': categories})

#edit category
def edit_category(request, id):

    cate = Category.objects.get(id=id)

    if request.method == 'POST':

        new_name = request.POST.get('category')
        cate.name = new_name
        cate.save()

        return redirect('view_cat')

    return render(request, 'c_admin/edit_category.html', {'cate': cate})

#delect category

#def delete_category(request, id):
 #   cate = get_object_or_404(Category, id=id)
  #  cate.delete()
   # return redirect('view_cat')
def delete_category(request, id):
    cate = get_object_or_404(Category, id=id)
    cate.delete()
    return redirect('view_cat')

#Menu
def add_menu(request):

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        photo = request.FILES.get('photo')


        category = Category.objects.get(id=category_id)

        obj3 = Product()
        obj3.name = name
        obj3.price = price
        obj3.description = description
        obj3.category = category

        obj3.photo = photo

        obj3.save()


        return redirect('view_menu')

    return render(request, 'c_admin/add_menu.html', {'categories': categories})

def view_menu(request):

    products = Product.objects.all()

    return render(request, 'c_admin/view_menu.html', {'products': products})

def edit_menu(request, id):

    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == 'POST':

        product.category_id = request.POST.get('category')
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        # for image update
        if 'photo' in request.FILES:
            product.photo = request.FILES['photo']

        product.save()

        return redirect('view_menu')

    return render(request, 'c_admin/edit_menu.html', {
        'product': product,
        'categories': categories
    })
def delete_menu(request, id):

    product = Product.objects.get(id=id)

    product.delete()

    return redirect('view_menu')
#review
def a_view_review(request):
    

    reviews = Review.objects.all()

    return render(request, 'c_admin/a_view_review.html', { 'reviews': reviews })    
#oder
def view_orders(request):

    orders = Order.objects.prefetch_related(
        'orderitem_set'
    ).all().order_by('-ordered_at')

    return render(
        request,
        'c_admin/view_orders.html',
        {
            'orders': orders
        }
    )


def view_pending_orders(request):

    orders = Order.objects.prefetch_related(
        'orderitem_set'
    ).filter(
        status__in=[
            'Pending',
            'Preparing',
            'Packing',
            'Out for Delivery'
        ]
    ).order_by('-ordered_at')

    return render(
        request,
        'c_admin/oder_statues.html',
        {
            'orders': orders
        }
    )


def view_delivered_orders(request):

    orders = Order.objects.filter(
        status='Delivered'
    ).order_by('-ordered_at')

    return render(
        request,
        'c_admin/view_delivered_orders.html',
        {
            'orders': orders
        }
    )


def update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        order.status = new_status

        order.save()

    return redirect('view_pending_orders')


#table

# ADD TABLES

def add_table(request):

    if request.method == 'POST':
         table_number = request.POST.get('table_number')
         seats = request.POST.get('seats')
         CafeTable.objects.create( table_number=table_number, seats=seats ) 
         return redirect('view_table_booking')
    return render(request, 'c_admin/add_table.html')
# VIEW TABLES

# VIEW TABLES + BOOKINGS

def view_table_booking(request):
    tables = CafeTable.objects.all()

    today = timezone.now().date()

    # TODAY BOOKINGS
    bookings = TableBooking.objects.filter(
        booking_date=today,
        status='Reserved'
    )

    # ALL BOOKINGS
    all_bookings = TableBooking.objects.all().order_by('-booking_date')

    total_tables = tables.count()

    total_seats = sum(table.seats for table in tables)

    reserved_seats = sum(
        booking.guests for booking in bookings
    )

    available_seats = total_seats - reserved_seats

    context = {

        'tables': tables,

        'bookings': bookings,

        'all_bookings': all_bookings,

        'total_tables': total_tables,
        'total_seats': total_seats,
        'reserved_seats': reserved_seats,
        'available_seats': available_seats,

    }

    return render(request, 'c_admin/view_table_booking.html', context)

def update_booking_status(request, booking_id):

    booking = get_object_or_404(
        TableBooking,
        id=booking_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        booking.status = new_status

        booking.save()

    return redirect('view_table_booking')

def delete_table(request, id):
    table = get_object_or_404(CafeTable, id=id)
    table.delete()
    return redirect('view_table_booking')
################################################        dashbord for admin     ########################################################################

def admin_dashboard(request):

    filter_type = request.GET.get('filter')

    orders = Order.objects.all()

    today = timezone.now().date()


    # TODAY FILTER

    if filter_type == 'today':

        orders = orders.filter(
            ordered_at__date=today
        )

    # THIS WEEK FILTER

    elif filter_type == 'week':

        week_ago = today - timedelta(days=7)

        orders = orders.filter(
            ordered_at__date__gte=week_ago
        )

    # ORDER DATA

    total_orders = orders.count()

    total_sales = orders.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    pending_orders = orders.filter(
        status='Pending'
    ).count()

    delivered_orders = orders.filter(
        status='Delivered'
    ).count()

    total_products = Product.objects.count()

    total_users = User.objects.count()
    #catgory

    total_category=Category.objects.count()


    # TABLE DATA

    total_tables = CafeTable.objects.count()

    total_seats = sum(
        table.seats for table in CafeTable.objects.all()
    )

    today_bookings = TableBooking.objects.filter(
        booking_date=today
    ).count()

    reserved_tables = TableBooking.objects.filter(
        booking_date=today
    ).count()

    context = {
        'total_category': total_category,

        'total_orders': total_orders,

        'total_sales': total_sales,

        'pending_orders': pending_orders,

        'delivered_orders': delivered_orders,

        'total_products': total_products,

        'total_users': total_users,

        'total_tables': total_tables,

        'total_seats': total_seats,

        'today_bookings': today_bookings,

        'reserved_tables': reserved_tables,

    }

    return render(
        request,
        'c_admin/dashboard.html',
        context
    )

###################################################################################################################################################
#####################                        user                             ########################################
###################################################################################################################################################

# USER REGISTER

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # CHECK USERNAME EXISTS

        if User.objects.filter(username=username).exists():

            return render(request, 'user/register.html', {
                'error': 'Username already exists'
            })

        # CREATE USER

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect('login')

    return render(request, 'user/register.html')
# USER LOGIN

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('u_home')

        else:

            return render(request, 'user/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'user/login.html')
# USER LOGOUT

def user_logout(request):

    logout(request)

    return redirect('login')

@login_required
def user_home(request):

    return render(request, 'user/home.html')

def menu(request):

    categories = Category.objects.filter(product__isnull=False).distinct()
    products = Product.objects.all()

    # SEARCH

    search = request.GET.get('search')

    if search:

        products = products.filter(
            name__icontains=search
        )

    # CATEGORY FILTER

    category_id = request.GET.get('category')

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    context = {

        'categories': categories,

        'products': products,

    }

    return render(
        request,
        'user/menu.html',
        context
    )
@login_required

def product_details(request, id):

    product = Product.objects.get(id=id)

    context = {
        'product': product
    }

    return render(request, 'user/product_details.html', context)

##Add to cart
@login_required
def add_to_cart(request, id):

    product = Product.objects.get(id=id)

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:

        cart = Cart.objects.create(
            user=request.user
        )

    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product
    ).first()

    if cart_item:

        cart_item.quantity += 1
        cart_item.save()

    else:

        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )

    return redirect(request.META.get('HTTP_REFERER', 'menu'))

#Cart view
@login_required
def cart(request):

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    cart_items = []

    total = 0

    if cart:

        cart_items = CartItem.objects.filter(
            cart=cart
        )

        for i in cart_items:

            total += i.total_price
            

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'user/cart.html', context)

@login_required
def remove_cart_item(request, id):

    item = CartItem.objects.get(id=id)

    item.delete()

    return redirect('cart')
@login_required
def increase_quantity(request, id):

    item = CartItem.objects.get(id=id)

    item.quantity += 1

    item.save()

    return redirect('cart')
@login_required
def decrease_quantity(request, id):

    item = CartItem.objects.get(id=id)

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    else:

        item.delete()

    return redirect('cart')

@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user ).first()

    if not cart:

        return redirect('cart')

    cart_items = CartItem.objects.filter(cart=cart )

    total = 0

    for item in cart_items:

        total += item.total_price

    # USER PROFILE

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # PLACE ORDER

    if request.method == 'POST':

        name = request.POST.get('name')

        phone = request.POST.get('phone')

        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # SAVE USER ADDRESS

        profile.phone = phone
        profile.address = address
        profile.save()

        # CREATE ORDER

        order = Order.objects.create(

        user=request.user,

        customer_name=name,

        phone=phone,

        address=address,

        total_amount=total,

        payment_method=payment_method,

        )

        # CREATE ORDER ITEMS

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )

        # CLEAR CART

        cart_items.delete()

        return redirect('order_success')

    context = {

        'cart_items': cart_items,

        'total': total,

        'profile': profile,

    }
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        return redirect('cart')

    cart_items = cart.cartitem_set.all()
    total = sum(item.total_price for item in cart_items)

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, "Please select a valid payment method.")
            return render(request, 'user/checkout.html', {'cart_items': cart_items, 'total': total, 'profile': profile})

        # Save delivery details to profile
        profile.phone = phone
        profile.address = address
        profile.save()

        # CREATE ORDER (Marked as pending/ unpaid initially)
        order = Order.objects.create(
            user=request.user,
            customer_name=name,
            phone=phone,
            address=address,
            total_amount=total,
            payment_method=payment_method,
        )

        # CREATE ORDER ITEMS
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 🔀 THE ROUTING LOGIC
        if payment_method == 'Cash on Delivery':
            # Complete immediately for COD
            cart_items.delete()
            cart.delete()
            return redirect('order_success')
        else:
            # Send them to the gateway view for online payments (UPI or Card)
            return redirect('payment_gateway', order_id=order.id)

    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'total': total, 'profile': profile})


@login_required
def payment_gateway(request, order_id):
    from django.shortcuts import get_object_or_404
    # Grab the order we just created
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = Cart.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # Simulate a successful transaction check here!
        if cart:
            cart.cartitem_set.all().delete()
            cart.delete()
        
        messages.success(request, f"Payment of ₹{order.total_amount} verified successfully via {order.payment_method}!")
        return redirect('order_success')

    return render(request, 'user/payment_gateway.html', {'order': order})

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_at')

    context = {
        'orders': orders
    }

    return render(
        request,
        'user/my_orders.html',
        context
    )
@login_required
def order_success(request):

    return render(
        request,
        'user/order_success.html'
    )

@login_required
def book_table(request):
    if request.method == 'POST':
        # If the user clicked "Accept Combination Options" from the pending screen
        if 'accept_combination' in request.POST:
            pending = request.session.get('pending_booking')
            if pending:
                # Retrieve selected split tables
                table_ids = request.session.get('combination_table_ids', [])
                
                parsed_time = datetime.datetime.strptime(pending['booking_time'], '%H:%M')
                calculated_end_time = (parsed_time + datetime.timedelta(hours=2)).time()

                booking = TableBooking.objects.create(
                    user=request.user,
                    customer_name=request.user.username,
                    phone=getattr(request.user.userprofile, 'phone', 'No Phone'),
                    booking_date=pending['booking_date'],
                    booking_time=pending['booking_time'],
                    end_time=calculated_end_time,
                    guests=pending['guests'],
                    special_request=pending['special_request'],
                    status='Reserved'
                )
                
                # Attach all tables in the combination
                for t_id in table_ids:
                    booking.tables.add(t_id)
                
                # Clean up session
                request.session.pop('pending_booking', None)
                request.session.pop('combination_table_ids', None)
                return redirect('my_bookings')

        # Normal form submission
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        guests = int(request.POST.get('guests'))
        special_request = request.POST.get('special_request', '')

        # Calculate times for checking availability
        parsed_time = datetime.datetime.strptime(booking_time, '%H:%M')
        calculated_end_time = (parsed_time + datetime.timedelta(hours=2)).time()

        # Step A: Find tables already booked in this time slot
        overlapping_bookings = TableBooking.objects.filter(
            booking_date=booking_date,
            booking_time__lt=calculated_end_time,
            end_time__gt=booking_time,
            status='Reserved'
        )
        booked_table_ids = []
        for b in overlapping_bookings:
            booked_table_ids.extend(b.tables.values_list('id', flat=True))

        # Step B: Get all currently free tables
        available_tables = CafeTable.objects.exclude(id__in=booked_table_ids).order_by('seats')
        # Strategy 1: Look for a single perfect table that fits them comfortably
        perfect_single_table = available_tables.filter(seats__gte=guests).first()

        if perfect_single_table:
            # Automatic instant booking!
            booking = TableBooking.objects.create(
                user=request.user,
                customer_name=request.user.username,
                phone=getattr(request.user.userprofile, 'phone', 'No Phone'),
                booking_date=booking_date,
                booking_time=booking_time,
                end_time=calculated_end_time,
                guests=guests,
                special_request=special_request,
                status='Reserved'
            )
            booking.tables.add(perfect_single_table)
            return redirect('my_bookings')

        # Strategy 2: No single table fits. Let's find a combination of 2 tables!
        found_combination = None
        
        for i in range(len(available_tables)):
            for j in range(i + 1, len(available_tables)):
                t1 = available_tables[i]
                t2 = available_tables[j]
                
                # Check if combining these two accommodates the guest count
                if (t1.seats + t2.seats) >= guests:
                    found_combination = (t1, t2)
                    break
            if found_combination:
                break

        if found_combination:
            # Stash booking specifics in session variables temporarily
            request.session['pending_booking'] = {
                'booking_date': booking_date,
                'booking_time': booking_time,
                'guests': guests,
                'special_request': special_request
            }
            request.session['combination_table_ids'] = [found_combination[0].id, found_combination[1].id]

            # Render a choice screen to offer the proposal to the user
            context = {
                'show_proposal': True,
                'guests': guests,
                'table1': found_combination[0],
                'table2': found_combination[1],
                'total_seats': found_combination[0].seats + found_combination[1].seats
            }
            return render(request, 'user/book_table.html', context)

        # Strategy 3: Absolutely full capacity (No table combinations are big enough)
        context = {
            'error_message': f"Sorry, we are fully booked for {guests} guests at that time. No combinations available.",
            'tables': CafeTable.objects.all()
        }
        return render(request, 'user/book_table.html', context)

    # Simple GET request to load the clean template
    context = {
        'tables': CafeTable.objects.all()
    }
    return render(request, 'user/book_table.html', context)
@login_required
def my_bookings(request):

    bookings = TableBooking.objects.filter(
        user=request.user
    ).order_by('-booking_date')

    context = {
        'bookings': bookings
    }

    return render(
        request,
        'user/my_bookings.html',
        context
    )

@login_required
def add_review(request, id):

    product = Product.objects.get(id=id)

    if request.method == 'POST':

        rating = request.POST.get('rating')

        comment = request.POST.get('comment')

        Review.objects.create(

            customer_name=request.user.username,

            product=product,

            rating=rating,

            comment=comment

        )

        return redirect('menu')

    context = {
        'product': product
    }

    return render(
        request,
        'user/add_review.html',
        context
    )

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        'profile': profile
    }

    return render(
        request,
        'user/profile.html',
        context
    )

def view_review(request):
    

    reviews = Review.objects.all()

    return render(request, 'user/view_review.html', { 'reviews': reviews })  
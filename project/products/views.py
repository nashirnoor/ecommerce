from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.cache import cache_control,never_cache
from .models import Product,Category,Wishlist,Cart,Order,OrderItem,Wallet
from user.models import Customer,Address
from django.contrib.auth.models import AnonymousUser
from . models import ProductImage
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404    
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Brand



def display_brands(request):
    brands = Brand.objects.all()
    return render(request, 'dashboard/brand.html', {'brands': brands})



def add_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('bname')
        brand_desc = request.POST.get('bdesc')
        Brand.objects.create(name=brand_name, description=brand_desc)
        return redirect('display_brands')
    return render(request, 'dashboard/brand.html')

def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        brand.delete()
        return redirect('display_brands')
    return redirect('display_brands') 



def arr(request):
    return render(request,'main/order_view.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def product(request):
    if 'admin' in request.session:       
        products = Product.objects.all().order_by('id').filter(is_deleted = False)                
        paginator = Paginator(products,6 )  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,          
        }
        return render(request, 'dashboard/all_products.html', context)
    else:
        return redirect('admin')
    


def search(request):
    if "email" in request.session:
        query = request.GET.get("q")

        if query:
            results = Product.objects.filter(product_name__icontains=query)
            print("Query:", query)
            print("Results:", results)
        else:
            results = []
            print("No Query")

        paginator = Paginator(results, 10)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            "page_obj": page_obj,
            "data": results,
        }

        if not results:
            messages.info(request, 'No products found.')

        return render(request, "main/product_list.html", context)
    return redirect("login")





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache  
def add_product(request):
    if 'admin' in request.session:
        # offer = None
        brands = Brand.objects.all()
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            category_name = request.POST.get('category')
            category = get_object_or_404(Category, category_name=category_name) 
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            image = request.FILES.get('image')  
            images = request.FILES.getlist('mulimage')
            is_listed = request.POST.get('is_listed') == 'on'
            brand_id = request.POST.get('brand')
            product_offer = request.POST.get('offer')
            selected_brand = Brand.objects.get(id=brand_id)
            
            # Get the category percentage discount
            category_percentage = category.category_offer

            

             # Check if the 'image' field has a valid file format
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                error_message = "Invalid file format for the main image. Please upload images only."
                categories = Category.objects.all()
                context = {'categories': categories, 'error_message': error_message}
                return render(request, 'dashboard/add_product.html', context)

            # Check if each file in the 'images' field has a valid file format
            for img in images:
                if not img.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    error_message = "Invalid file format for additional images. Please upload images only."
                    categories = Category.objects.all()
                    context = {'categories': categories, 'error_message': error_message}
                    return render(request, 'dashboard/add_product.html', context)

            
            if not (product_name and description and category_name and price and image and stock and images):
                error_message = "Please fill in all the required fields."
                messages.error(request, error_message)
                categories = Category.objects.all()
                context = {'categories': categories, 'error_message': error_message}
                return render(request, 'dashboard/add_product.html', context)
            
             # Check for whitespace-only values
            if any(value.strip() == '' for value in [product_name, description, category_name, stock, price]):
                error_message = "Whitespace-only values are not allowed."
                messages.error(request, error_message)
                categories = Category.objects.all()
                context = {'categories': categories, 'error_message': error_message}
                return render(request, 'dashboard/add_product.html', context)

            try:
                # Attempt to convert the price to Decimal
                price = Decimal(price)
            except (TypeError, ValueError):
                # Handle the case where conversion fails
                print("Conversion to Decimal failed. Value:", price)
                price = Decimal('0')  # Default to 0 or any other appropriate value

            print("Price after conversion:", price)

            # Calculate discounted price based on category offer
            if category_percentage is not None:
                category_discount = (category_percentage / 100) * price
                discounted_price = price - category_discount
                # Ensure discounted price is not negative
                discounted_price = max(discounted_price, Decimal(0))
                print("Discounted Price:", discounted_price)
            else:
                discounted_price = price
                print("Original Price (no discount):", discounted_price)

            # Create the product instance with the calculated price
            product = Product.objects.create(
                product_name=product_name,
                description=description,
                category=category,
                stock=stock,
                price=price,  # Use the original price
                discounted_price=discounted_price,
                product_offer=product_offer,  # Use the calculated price
                image=image,
                is_listed=is_listed,
            )

            # Save additional images
            for img in images:
                ProductImage.objects.create(product=product, image=img)

            # Update the discounted price and save the product again
            product.discounted_price = discounted_price
            product.save()

            return redirect('products') 

        categories = Category.objects.all()
        context = {
            'categories': categories,
            # 'product_offer': offer,
              'brands': brands,  # Add product_offer to the context
        }
        return render(request, 'dashboard/add_product.html', context)
    else:
        return redirect('admin')





from django.db.models import F

from django.db.models import F

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache    
def userproductpage(request): 
    sort_option = request.GET.get("sort", "all")

    if sort_option == "all":
        data = Product.objects.filter(is_listed=True).order_by("price")
    elif sort_option == "high":
        data = Product.objects.filter(is_listed=True).order_by(F("price").desc())
    else:
        # Handle other sorting options or set a default sorting
        data = Product.objects.filter(is_listed=True).order_by("price")

    paginator = Paginator(data, 9)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    for product in page_obj:
        if product.category.category_offer is not None:
            category_discount = (product.category.category_offer / 100) * product.price
            discounted_price = product.price - category_discount
            # Ensure discounted price is not negative
            discounted_price = max(discounted_price, Decimal(0))
            product.discounted_price = discounted_price
            product.save()

    categories = Category.objects.all()

    context = {
        'data': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'sort_option': sort_option,
        'total_product_count': paginator.count,
    }

    return render(request, 'main/product_list.html', context)


@never_cache
def single_product(request, id):
    product = Product.objects.get(id=id)
    # offer_price = int(product.price * (1 - product.product_offer / 100))
    context = {
        "product": product,
        # "offer_price": offer_price,
    }
    return render(request, "main/single_product.html", context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def editproduct(request, product_id):
    if 'admin' in request.session:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:        
            return render(request, 'product_not_found.html')
        
        categories = Category.objects.all()
        context = {
            'product'    : product,
            'categories' : categories,
        }

        return render(request, 'dashboard/update_product.html', context)
    else:
        return redirect('admin')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update(request, id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        category_name = request.POST.get('category')
        category = Category.objects.get(category_name=category_name)
        product.category = category
        product.stock = request.POST.get('stock')
        product.price = request.POST.get('price')
        # product.product_offer = request.POST.get('offer')
        replace_image = request.FILES.get('replace_image')
        images = request.FILES.getlist('mulimage')

        for img in images:
            if not img.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                error_message = "Invalid file format. Please upload images only."
                context = {'product': product, 'categories': categories, 'error_message': error_message}
                return render(request, 'dashboard/update_product.html', context)

        for existing_image in product.additional_images.all():
            if existing_image.image and not existing_image.image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                error_message = "Invalid file format. Please upload images only."
                context = {'product': product, 'categories': categories, 'error_message': error_message}
                return render(request, 'dashboard/update_product.html', context)

        if not all([product.product_name, product.description, category_name, product.stock, product.price]):
            error_message = "Please fill in all the required fields."
            context = {'product': product, 'error_message': error_message}
            return render(request, 'dashboard/update_product.html', context)
        
        if any(value.strip() == '' for value in [product.product_name, product.description, category_name, product.stock, product.price]):
            error_message = "Whitespace-only values are not allowed."
            messages.error(request, error_message)
            context = {'categories': categories, 'error_message': error_message}
            return render(request, 'dashboard/add_product.html', context)

        if replace_image:
            product.image = replace_image

        is_listed = request.POST.get('is_listed')
        product.is_listed = is_listed == 'on'
        product.save()

        for img in images:
            ProductImage.objects.create(product=product, image=img)
        
        for existing_image in product.additional_images.all():
          remove_image_key = f"remove_image_{existing_image.id}"
          if remove_image_key in request.POST:
              existing_image.delete()

        for existing_image in product.additional_images.all():
          replace_image_key = f"replace_image_{existing_image.id}"
          if replace_image_key in request.FILES:
             new_image = request.FILES.get(replace_image_key)
             existing_image.image = new_image
             existing_image.save()

        return redirect('products')

    else:
        context = {'product': product}
        return render(request, 'dashboard/update_product.html', context)



###### CART ######################################################   

from decimal import Decimal

# Import other necessary modules and classes

def calculate_effective_offer(product):
    # Calculate the effective offer by comparing category and product offers
    effective_offer = max(product.category.category_offer, product.product_offer)
    return effective_offer





def update_cart(request, product_id):
    print(f"Updating cart for product ID: {product_id}")
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'message': 'Invalid quantity.'}, status=400)
    if quantity < 1:
        return JsonResponse({'message': 'Quantity must be at least 1.'}, status=400)

    user = request.user
    cart_item = get_object_or_404(Cart, product_id=product_id, user=user)
    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'message': 'Cart item updated.'}, status=200)


@login_required(login_url='login') 
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')

    quantity = request.POST.get('quantity', 1)
    if not quantity:
        quantity = 1
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if created:
        cart_item.quantity = int(quantity)
    else:
        cart_item.quantity += int(quantity)
    cart_item.save()
    return redirect('cart')



@login_required
def remove_from_cart(request, cart_item_id):
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()

        except Cart.DoesNotExist:
            print("hhhhhhhhhhhh")
        
        return redirect('cart')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

@login_required(login_url='login') 
def wishlist(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return redirect('login')  # Redirect to the login page
    else:
        wishlist_items = Wishlist.objects.filter(user=user)
        wishlist_count = wishlist_items.count()

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
    }

    return render(request, 'main/wishlist.html', context)





def wishlist_count(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    wishlist_count = wishlist_items.count()

    return {'wishlist_count': wishlist_count}



def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')
    user = request.user
    if isinstance(user, AnonymousUser):
            return redirect('login')
    else:
        wishlist, created = Wishlist.objects.get_or_create(product=product, user=user)
    wishlist.save()

    return redirect('wishlist')



def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')



############## PAYMENT AND ORDERS ####################


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    if 'email' in request.session:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        subtotal = 0

        for cart_item in cart_items:
            if cart_item.product.category.category_offer:
                itemprice2 = (cart_item.product.price - cart_item.product.category.category_offer) * (cart_item.quantity)
                subtotal += itemprice2  # Accumulate subtotal for each item
                print(subtotal,"hhhhhhhhhhhh")
            else:
                itemprice2 = (cart_item.product.price) * (cart_item.quantity)
                subtotal += itemprice2  # Accumulate subtotal for each item
                print(subtotal,"hhhhhhhhhhhh")

        shipping_cost = 10 
        discount = request.session.get('discount', 0)
        if discount:
            total = subtotal + shipping_cost - discount if subtotal else 0
        else:
            total = subtotal + shipping_cost  if subtotal else 0
        
        subtotal = Decimal(request.session.get('cart_subtotal', 0))
        total = Decimal(request.session.get('cart_total', 0))
        print(subtotal)
        print(total)
        request.session['subtotal'] = str(subtotal)
        request.session['total'] = str(total)

        user_addresses = Address.objects.filter(user=request.user)

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'total': total,
            'user_addresses': user_addresses,
            'discount_amount': discount,
            'itemprice': itemprice2  # This will be the itemprice2 of the last item in the loop
        }
        return render(request, 'main/checkout.html', context)
    else:
        return redirect('signup')

def calculate_effective_offer(product):
    # Calculate the effective offer by comparing category and product offers
    effective_offer = max(product.category.category_offer, product.product_offer)
    return effective_offer
@login_required
def placeorder(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    shipping_cost = 10
    discount = request.session.get("discount", 0)
    subtotal = 0

    address_id = request.POST.get("addressId")

    if not address_id:
        messages.info(request, "Input Address!!!")
        return redirect("checkout")

    # Retrieve the selected address from the database
    address = Address.objects.get(id=address_id)
    payment = request.POST.get("payment")

    for cart_item in cart_items:
        # Check if the requested quantity is available in stock
        product = cart_item.product

        if cart_item.quantity > product.stock:
            messages.error(request, f"Insufficient stock for {product.product_name}.")
            return redirect("checkout")

        effective_offer = calculate_effective_offer(product)
        item_price = product.price * cart_item.quantity

        if effective_offer > 0:
            # Apply the effective offer as a percentage
            discount_amount = (effective_offer / Decimal('100.0')) * item_price
            item_price -= discount_amount

        subtotal += item_price
        

        # Create a separate order for each product in the cart
        order = Order.objects.create(
            user=user,
            address=address,
            amount=subtotal + shipping_cost,
            payment_type=payment,
        )

        product.stock -= cart_item.quantity
        product.save()

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            image=product.image,
        )

    if discount:
        total = subtotal + shipping_cost - discount
    else:
        total = subtotal + shipping_cost

    cart_items.delete()
    return redirect("success")


def razorpay(request, address_id):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    subtotal = 0
    for cart_item in cart_items:
        if cart_item.quantity > product.stock:
            messages.error(request, f"Insufficient stock for {product.product_name}.")
            return redirect("checkout")

        product = cart_item.product
        effective_offer = calculate_effective_offer(product)
        item_price = product.price * cart_item.quantity

        if effective_offer > 0:
            # Apply the effective offer as a percentage
            discount_amount = (effective_offer / Decimal('100.0')) * item_price
            item_price -= discount_amount

        subtotal += item_price

    shipping_cost = 10
    total = subtotal + shipping_cost if subtotal else 0

    subtotal = Decimal(request.session.get('cart_subtotal', 0))
    total = Decimal(request.session.get('cart_total', 0))

    discount = request.session.get("discount", 0)

    if discount:
        total -= discount

    payment = "razorpay"
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    address = Address.objects.get(id=address_id)

    order = Order.objects.create(
        user=user,
        address=address,
        amount=total,
        payment_type=payment,
    )
    print(total,"ttttttotal")

    for cart_item in cart_items:
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()

        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            image=cart_item.product.image,
        )

    cart_items.delete()
    return redirect("success")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def order(request):
    user = request.user
    if "admin" in request.session:
        orders = Order.objects.all().order_by("-id")

        paginator = Paginator(orders, per_page=15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "orders": page_obj,
            'user':user
        }
        return render(request, "dashboard/orders.html", context)
    else:
        return redirect("admin")


def success(request):
    orders = Order.objects.order_by("-id")[:1]
    context = {
        "orders": orders,
    }
    return render(request, "main/placeorder.html", context)


def cancel_success(request):
    print("successsssssssssssssssssss")
    orders = Order.objects.order_by("-id")[:1]
    context = {
        "orders": orders,
    }
    return render(request, "main/cancel_order.html", context)


def customer_order(request):
    if "email" in request.session:
        user = request.user
        orders = Order.objects.filter(user=user).order_by("-id")
        for order in orders:
            order_items = order.order_items.all()
            for order_item in order_items:
                print(f"Order ID: {order.id}")
                print(f"Order Item ID: {order_item.id}")
                print(f"Amount: {order.amount}")
                print(f"Payment Type: {order.payment_type}")
                print(f"Status: {order.status}")
                print(f"Date: {order.date}")
                print(f"Order Item Quantity: {order_item.quantity}")
                print(f"Order Item Image: {order_item.image}")
                print("---")
           
        context = {
            "orders": orders,
        }
        return render(request, "main/customer_order.html", context)
    else:
        return redirect("home")


def updateorder(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        new_status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return redirect("order")
        if new_status == 'cancelled':
            handle_cancellation(order)

        order.status = status
        order.save()
        messages.success(request, "Order status updated successfully.")

        return redirect("order")

    return redirect("admin")


from decimal import Decimal
from django.utils import timezone

def handle_cancellation(order):
    # Check if the payment type is 'razorpay'
    if order.payment_type == 'razorpay':
        # Get the related order items
        order_items = order.order_items.all()

        # Calculate the total amount to be credited
        total_amount = sum(order_item.product.price * order_item.quantity for order_item in order_items)

        # Create a Wallet entry and credit the amount to the user's wallet
        wallet = Wallet.objects.create(
            user=order.user,
            order=order,
            amount=total_amount,
            status="Credited",
            created_at=timezone.now(),
        )
        wallet.save()

        # Restock the products and update user's wallet balance
        for order_item in order_items:
            product = order_item.product
            product.stock += order_item.quantity
            product.save()

            order.user.wallet_bal += order_item.product.price * order_item.quantity
            order.user.save()









def restock_products(order):
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save()


def cancel_order(request, order_id, order_item_id):
    print("hhhhhhhhhhhhhhhhhhhhhhh")
    user = request.user
    usercustm = Customer.objects.get(email=user)
    try:
        order = Order.objects.get(id=order_id)
        order_item = OrderItem.objects.get(id=order_item_id, order=order)
    except Order.DoesNotExist or OrderItem.DoesNotExist:
        return render(request, 'order_not_found.html')

    if order.status in ["completed", "processing","pending"]:
        # Create a Wallet entry and credit the amount to the user's wallet
        wallet = Wallet.objects.create(
            user=user,
            order=order,
            amount=order_item.product.price * order_item.quantity,
            status="Credited",
        )
        wallet.save()
        # Restock the product
        product = order_item.product
        product.stock += order_item.quantity
        product.save()
        # Update user's wallet balance
        usercustm.wallet_bal += order_item.product.price * order_item.quantity
        usercustm.save()
    # Delete the order item
    order_item.delete()
    # If there are no more items in the order, set the order status to cancelled
    if order.order_items.count() == 0:
        order.status = "cancelled"
        order.save()

    return redirect("order_details", order_id)

def return_order(request, order_id, order_item_id):
    print("RRRRRRRRRRRRRRRRRRRRRRRRRRR")
    user = request.user
    usercustm = Customer.objects.get(email=user)
    try:
        order = Order.objects.get(id=order_id)
        order_item = OrderItem.objects.get(id=order_item_id, order=order)
    except Order.DoesNotExist or OrderItem.DoesNotExist:
        return render(request, 'order_not_found.html')

    if order.status in ["completed", "delivered"]:
        # Create a Wallet entry and credit the amount to the user's wallet
        wallet = Wallet.objects.create(
            user=user,
            order=order,
            amount=order_item.product.price * order_item.quantity,
            status="Credited",
        )
        wallet.save()
        # Restock the product
        product = order_item.product
        product.stock += order_item.quantity
        product.save()
        # Update user's wallet balance
        usercustm.wallet_bal += order_item.product.price * order_item.quantity
        usercustm.save()
    # Delete the order item
    order_item.delete()
    # If there are no more items in the order, set the order status to cancelled
    if order.order_items.count() == 0:
        order.status = "Return successful"
        order.save()

    return redirect("order_details", order_id)






def wallet(request):
    if "email" in request.session:
        user = request.user
        customer = Customer.objects.get(email=user)
        wallets = Wallet.objects.filter(user=user).order_by("-created_at")

        context = {
            "customer": customer,
            "wallets": wallets,
        }
        return render(request, "main/wallet.html", context)
    else:
        return redirect("home")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def order_details(request, id):
    orders = Order.objects.filter(id=id)
    print(orders)
    context = {
        "orders": orders,
    }
    return render(request, "main/order_details.html", context)


def proceedtopay(request):
    cart = Cart.objects.filter(user=request.user)
    total = 0
    shipping = 10
    subtotal = 0
    for cart_item in cart:
        if cart_item.product.category.category_offer:
            itemprice2 = (
                cart_item.product.price - cart_item.product.category.category_offer
            ) * (cart_item.quantity)
            subtotal = subtotal + itemprice2

        else:
            itemprice = (cart_item.product.price) * (cart_item.quantity)

            subtotal = subtotal + itemprice
    for item in cart:
        discount = request.session.get("discount", 0)
    total = subtotal + shipping
    if discount:
        total -= discount
    
    return JsonResponse({"total": total})


from . models import Coupon

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coupon(request):
    if "admin" in request.session:
        coupons = Coupon.objects.all().order_by("id")
        context = {"coupons": coupons}
        return render(request, "dashboard/coupon.html", context)
    else:
        return redirect("admin")


def addcoupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("Couponcode")
        discount_price = request.POST.get("dprice")
        minimum_amount = request.POST.get("amount")

        coupon = Coupon(
            coupon_code=coupon_code,
            discount_price=discount_price,
            minimum_amount=minimum_amount,
        )
        coupon.save()

        return redirect("coupon")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart, Coupon
from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required(login_url='login') 
def cart(request):
    if isinstance(request.user, AnonymousUser):
        device_id = request.COOKIES.get("device_id")
        cart_items = Cart.objects.filter(device=device_id).order_by("id")
    else:
        user = request.user
        cart_items = Cart.objects.filter(user=user).order_by("id")

    if request.method == "POST":
        print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        coupon_code = request.POST.get("coupon_code")

        # Validate the coupon
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, expired=False)
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code")
            return redirect("cart")

        # Apply the coupon to each cart item
        for cart_item in cart_items:
            cart_item.coupon = coupon
            cart_item.save()

        messages.success(request, "Coupon applied successfully")

    subtotal = 0
    total_dict = {}

    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            messages.warning(
                request, f"{cart_item.product.product_name} is out of stock."
            )
            cart_item.quantity = cart_item.product.stock
            cart_item.save()

        # Calculate item price considering category offer as a percentage
        item_price = cart_item.product.price * cart_item.quantity
        effective_offer = calculate_effective_offer(cart_item.product)
        if effective_offer > 0:
            # Apply the effective offer as a percentage
            discount_amount = (effective_offer / Decimal('100.0')) * item_price
            item_price -= discount_amount

        total_dict[cart_item.id] = item_price
        subtotal += item_price

    for cart_item in cart_items:
       cart_item.total_price = total_dict.get(cart_item.id, 0)
       print(cart_item.total_price)
       cart_item.save()

    shipping_cost = 10
    total = subtotal + shipping_cost if subtotal else 0

    total_discount = sum(cart_item.coupon.discount_price for cart_item in cart_items if cart_item.coupon)
    total = subtotal - total_discount + shipping_cost

    request.session['cart_subtotal'] = str(subtotal)  # Convert to string to handle Decimal serialization
    request.session['cart_total'] = str(total)

    coupons = Coupon.objects.all()

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total,
        "coupons": coupons,
    }
    return render(request, "main/cart.html", context)





def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")

        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code")
            return redirect("checkout")

        user = request.user
        cart_items = Cart.objects.filter(user=user)
        subtotal = 0
        shipping_cost = 10
        total_dict = {}
        coupons = Coupon.objects.all()

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                messages.warning(
                    request, f"{cart_item.product.product_name} is out of stock."
                )
                cart_item.quantity = cart_item.product.stock
                cart_item.save()

            if cart_item.product.category.category_offer:
                item_price = (
                    cart_item.product.price - cart_item.product.category.category_offer
                ) * (cart_item.quantity)
                total_dict[cart_item.id] = item_price
                subtotal += item_price

            elif cart_item.product.product_offer:
                item_price = (
                    cart_item.product.price
                    - (cart_item.product.price * cart_item.product.product_offer / 100)
                ) * cart_item.quantity
                total_dict[cart_item.id] = item_price
                subtotal += item_price

            else:
                item_price = cart_item.product.price * cart_item.quantity
                total_dict[cart_item.id] = item_price
                subtotal += item_price

        if subtotal >= coupon.minimum_amount:
            messages.success(request, "Coupon applied successfully")
            request.session["discount"] = coupon.discount_price
            total = subtotal - coupon.discount_price + shipping_cost
        else:
            messages.error(request, "Coupon not available for this price")
            total = subtotal + shipping_cost

        for cart_item in cart_items:
            cart_item.total_price = total_dict.get(cart_item.id, 0)
            cart_item.save()

        context = {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "total": total,
            "coupons": coupons,
            "discount_amount": coupon.discount_price,
        }

        return render(request, "cart.html", context)

    return redirect("cart")








def generate_invoice(request, order_id):
    # Fetch the order and related order items
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    # Retrieve the user's address
    user_address = Address.objects.filter(user=request.user, default=True).first()

    # Calculate total amount
    cart_total_amount = order.amount
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name

    # Calculate subtotal and total based on order items
    subtotal = sum(item.product.price * item.quantity for item in order_items)
    total = subtotal  # Add shipping cost or other adjustments if needed

    # Prepare context for rendering the template
    context = {
        'order': order,
        'order_items': order_items,
        'cart_total_amount': cart_total_amount,
        'user_address': user_address,  # Add the user's address to the context
        'user_first_name': user_first_name,
        'user_last_name': user_last_name,
        'subtotal': subtotal,
        'total': total,
    }

    return render(request, 'main/invoice.html', context)


    

def download_invoice(request, order_id):
    # Implement logic to generate/download the invoice content
    # For demonstration purposes, return a simple response
    return HttpResponse("This is the invoice content.", content_type='application/pdf')


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def searchproduct(request):
    if "admin" in request.session:
        query = request.GET.get("q")

        if query:
            results = Product.objects.filter(product_name__icontains=query)

        else:
            results = []

        paginator = Paginator(results, per_page=3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "query": query,
            "data":results,
        }
        if not results:
            messages.info(request, 'No products found.')
            
        return render(request, "dashboard/all_products.html", context)
    else:
        return redirect("admin")


def search(request):
        query = request.GET.get("q")
        print(query)

        if query:
            results = Product.objects.filter(product_name__icontains=query)
            print("Query:", query)
            print("Results:", results)
        else:
            results = []
            print("No Query")

        paginator = Paginator(results, 10)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            "page_obj": page_obj,
            "data": results,
        }

        if not results:
            messages.info(request, 'No products found.')

        return render(request, "main/product_list.html", context)


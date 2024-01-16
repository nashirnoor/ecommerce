from category.models import Category
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from .models import Customer,Address
from django.core.exceptions import ValidationError
from django.contrib import messages,auth
import secrets
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import smtplib
import json
from django.utils import timezone
from django.db.models import Sum, F, FloatField, DateField
from django.db.models.functions import Cast
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import string,random
from django.contrib import messages
from django.urls import reverse
from django.core.validators import RegexValidator
from products.models import Order, Product
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from products.models import OrderItem


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',  # Customize the regex pattern as needed
    message='Enter a valid phone number.',
)

def asdf(request):
    return render(request,'main/profile.html')

@never_cache
def loginPage(request):
    context = {
        'messages': messages.get_messages(request)
    }
    if 'email' and 'otp' in request.session:
        request.session.flush()
        return redirect('login')

    if 'email' in request.session:
        return redirect('home')

    if 'admin' in request.session:
        return redirect('admin')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        # Check if the user is blocked before attempting authentication
        try:
            blocked_user = Customer.objects.get(email=email, is_active=False)
            messages.warning(request, "Your account is blocked")
            return redirect('login')
        except Customer.DoesNotExist:
            pass

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            request.session['email'] = email
            login(request, user)
            messages.success(request, "Login successful. Welcome back!")
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")
            return render(request, 'main/login.html', context)
    else:
        return render(request, 'main/login.html', context)
     

@never_cache
def signupPage(request):
    if 'email' in request.session:
        return redirect('home')

    if request.method == 'POST':
        email     =    request.POST.get('email')
        number    =    request.POST.get('number')
        username  =    request.POST.get('username')
        pass1     =    request.POST.get('password1')
        pass2     =    request.POST.get('password2')
        refferal  =    request.POST.get('refferal')

        # Check if all fields except username contain only whitespace
        if all(not field.strip() for field in [email, number, pass1, pass2]) or not username.strip():
          messages.error(request, 'Please input non-whitespace characters in all fields.')
          return redirect('signup')
  
        if not email or not username or not pass1 or not pass2:
            messages.error(request, 'Please input all the details.')
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email address.')
            return redirect('signup')

        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exist')
            return redirect('signup')
        if Customer.objects.filter(number=number).exists():
            messages.error(request, 'Number already exist')
            return redirect('signup')

        message = generate_otp()
        print(message)
        sender_email = "nashirnoor2002@gmail.com"
        receiver_mail = email
        password = "qzyrtqxbcrdoqlpm"


        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_mail, message)

        except smtplib.SMTPAuthenticationError:
            messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
            return redirect('signup')
        referral_codes = generate_referral_code()
        user = Customer.objects.create_user(username=username, password=pass1, email=email,number=number,referral_code=referral_codes)
        user.save()

        if refferal:
            referrer = Customer.objects.get(referral_code = refferal)
            if referrer:
                referrer.referral_amount += 100
                referrer.save()


        request.session['email'] =  email
        request.session['otp']   =  message
        messages.success (request, 'OTP is sent to your email')
        return redirect('verify_signup')

    return render(request, 'main/signup.html')

def generate_otp(length = 6):
    return ''.join(secrets.choice("0123456789") for i in range(length)) 

def generate_referral_code():
    letters = string.ascii_letters + string.digits
    referral_code = ''.join(random.choice(letters) for i in range(10))
    return referral_code


def validate_email(email):
    return '@' in email and '.' in email

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def verify_signup(request):
    context = {
        'messages': messages.get_messages(request)
    }
    if request.method == "POST":
        
        user      =  Customer.objects.get(email=request.session['email'])
        x         =  request.session.get('otp')
        OTP       =  request.POST['otp']
      
        if OTP == x:
            user.is_verified = True
            user.save()
            del request.session['email'] 
            del request.session['otp']
        
            auth.login(request,user)
            messages.success(request, "Signup successful!")
        else:
            user.delete()
            messages.info(request,"invalid otp")
            del request.session['email']
            return redirect('signup')
        return redirect('login')
        
    return render(request,'main/otp.html',context)





@never_cache    
def logoutPage(request):
    if 'email' in request.session:
        request.session.flush()
    logout(request)
    return redirect('home')

    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def admin_login(request):
    if 'email' in request.session:
        return redirect('home')
    elif 'admin' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            username      =  request.POST.get('username')
            pass1         =  request.POST.get('pass')
            user          =  authenticate(request,username=username,password = pass1)
            print(user)

            if user is not None and user.is_superuser:
                login(request,user)
                request.session['admin']=username
                return redirect('dashboard')
            else:
                messages.error(request,"username or password is not same")
                return render(request, 'dashboard/login.html') 
        else:
             return render (request,'dashboard/login.html')
        


from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal to string
        return super().default(obj)
    


from django.db.models import Sum, F, FloatField
from django.utils import timezone

from django.http import JsonResponse
from django.db.models.functions import TruncMonth, TruncYear
from django.views.decorators.cache import never_cache
from django.http.request import HttpHeaders
from datetime import date

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def dashboard(request):
    orders = Order.objects.order_by("-id")
    labels = []
    data = []
    for order in orders:
        labels.append(str(order.id))
        data.append(float(order.amount))  # Convert Decimal to float

    total_customers = Customer.objects.count()

    # Calculate the count of new users in the last one week
    one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
    new_users_last_week = Customer.objects.filter(date_joined__gte=one_week_ago).count()

    # Get the total number of orders
    total_orders = Order.objects.count()

    # Calculate the count of orders in the last one week
    orders_last_week = Order.objects.filter(date__gte=one_week_ago).count()

    # Calculate the total amount received
    total_amount_received = Order.objects.aggregate(
        total_amount_received=Cast(Sum(F('amount')), FloatField())
    )['total_amount_received'] or 0

    # Calculate the total amount received in the last week
    total_amount_received_last_week = Order.objects.filter(date__gte=one_week_ago).aggregate(
        total_amount_received=Cast(Sum(F('amount')), FloatField())
    )['total_amount_received'] or 0
    print(total_amount_received_last_week)


    categories = Category.objects.annotate(num_products=Count('product'))
    category_labels = [category.category_name for category in categories]
    category_data = [category.num_products for category in categories]

    total_products = Product.objects.count()

    time_interval = request.GET.get('time_interval', 'all')  # Default to 'all' if not provided
    if time_interval == 'yearly':
        orders = Order.objects.annotate(date_truncated=TruncYear('date', output_field=DateField()))
        orders = orders.values('date_truncated').annotate(total_amount=Sum('amount'))
    elif time_interval == 'monthly':
        orders = Order.objects.annotate(date_truncated=TruncMonth('date', output_field=DateField()))
        orders = orders.values('date_truncated').annotate(total_amount=Sum('amount'))
    else:
        # Default to 'all' or handle other time intervals as needed
        orders = Order.objects.annotate(date_truncated=F('date'))
        orders = orders.values('date_truncated').annotate(total_amount=Sum('amount'))

    # Calculate monthly sales
    monthly_sales = Order.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total_amount=Sum('amount')).order_by('month')

    # Extract data for the monthly sales chart
    monthly_labels = [entry['month'].strftime('%B %Y') for entry in monthly_sales]
    monthly_data = [float(entry['total_amount']) for entry in monthly_sales]

    # Add this block to handle AJAX request for filtered data
    headers = HttpHeaders(request.headers)
    is_ajax_request = headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax_request and request.method == 'GET':
        time_interval = request.GET.get('time_interval', 'all')
        filtered_labels = []
        filtered_data = []

        if time_interval == 'yearly':
            filtered_orders = Order.objects.annotate(
                date_truncated=TruncYear('date', output_field=DateField())
            )
        elif time_interval == 'monthly':
            filtered_orders = Order.objects.annotate(
                date_truncated=TruncMonth('date', output_field=DateField())
            )
        else:
            # Default to 'all' or handle other time intervals as needed
            filtered_orders = Order.objects.annotate(date_truncated=F('date'))

        filtered_orders = filtered_orders.values('date_truncated').annotate(total_amount=Sum('amount')).order_by('date_truncated')

        filtered_labels = [entry['date_truncated'].strftime('%B %Y') for entry in filtered_orders]
        filtered_data = [float(entry['total_amount']) for entry in filtered_orders]

        return JsonResponse({"labels": filtered_labels, "data": filtered_data})
    context = {
        "labels": json.dumps(labels),
        "data": json.dumps(data),
        "total_customers": total_customers,
        "new_users_last_week": new_users_last_week,
        "total_orders": total_orders,
        "orders_last_week": orders_last_week,
        "total_amount_received": total_amount_received,
        "total_amount_received": total_amount_received_last_week,
        "total_products": total_products,
        "category_labels": json.dumps(category_labels),
        "category_data": json.dumps(category_data),
    }
    context.update({
        "monthly_labels": json.dumps(monthly_labels),
        "monthly_data": json.dumps(monthly_data),
    })

    if "admin" in request.session:
        return render(request, "dashboard/home.html", context)
    else:
        return redirect("admin")
    

from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear, Cast
from django.db.models.functions import TruncDate
from django.views.decorators.http import require_GET

@require_GET
def filter_sales(request):
    time_interval = request.GET.get('time_interval', 'all')

    if time_interval == 'yearly':
        # Filter data for yearly sales
        filtered_data = Order.objects.annotate(
            date_truncated=TruncYear('date')
        ).values('date_truncated').annotate(total_amount=Sum('amount')).order_by('date_truncated')

    elif time_interval == 'monthly':
        # Filter data for monthly sales
        filtered_data = Order.objects.annotate(
            date_truncated=TruncMonth('date')
        ).values('date_truncated').annotate(total_amount=Sum('amount')).order_by('date_truncated')

    else:
        # Default to 'all' or handle other time intervals as needed
        # Here, we are using DateTrunc to truncate the date to a day
        filtered_data = Order.objects.annotate(
            date_truncated=TruncDate('day', 'date')
        ).values('date_truncated').annotate(total_amount=Sum('amount')).order_by('date_truncated')

    # Extract data for the filtered chart
    filtered_labels = [entry['date_truncated'].strftime('%B %Y') for entry in filtered_data]
    filtered_data = [float(entry['total_amount']) for entry in filtered_data]

    return JsonResponse({"labels": filtered_labels, "data": filtered_data})






def report_generator(request, orders):
    from_date_str = request.POST.get('from_date')
    to_date_str = request.POST.get('to_date')

    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    if from_date > date.today() or to_date > date.today():
            # Return an error response or show a message
            return HttpResponse('Please enter a valid date.')
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    story = []

    data = [["Order ID", "Total Quantity", "Product IDs", "Product Names", "Amount"]]

    total_sales_amount = 0  # Initialize total sales amount sum

    for order in orders:
        # Retrieve order items associated with the current order
        order_items = OrderItem.objects.filter(order=order)
        total_quantity = sum(item.quantity for item in order_items)

        if order_items.exists():
            product_ids = ", ".join([str(item.product.id) for item in order_items])
            product_names = ", ".join([str(item.product.product_name) for item in order_items])
        else:
            product_ids = "N/A"
            product_names = "N/A"

        order_amount = order.amount
        total_sales_amount += order_amount  # Accumulate total sales amount

        data.append([order.id, total_quantity, product_ids, product_names, order_amount])

    # Add a row for the total sales amount at the end of the table
    data.append(["Total Sales", "", "", "", total_sales_amount])

    # Create a table with the data
    table = Table(data, colWidths=[1 * inch, 1.5 * inch, 2 * inch, 3 * inch, 1 * inch])

    # Style the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    table.setStyle(table_style)

    # Add the table to the story and build the document
    story.append(table)
    doc.build(story)

    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='orders_report.pdf')






def report_pdf_order(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse('Invalid date format.')
        orders = Order.objects.filter(date__range=[from_date, to_date]).order_by('-id')
        return report_generator(request, orders)
    
    



    

from products.models import Wishlist

@never_cache   
def admin_logout(request):
    if 'admin' in request.session:
        request.session.flush()
    logout(request)
    return redirect('admin')

from banner.models import Banner

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def home(request):
    user_id = None  # Default value when the user is not authenticated

    if request.user.is_authenticated:
        user_id = request.user.id

    categories = Category.objects.all()
    banners = Banner.objects.all()
    wishlist = Wishlist.objects.all()

    for category in categories:
        category.product_count = category.product_set.count()

    context = {
        'categories': categories,
        'banners': banners,
        'wishlist': wishlist,
        'user_id': user_id,
    }

    return render(request, 'main/home.html', context)

   


@never_cache 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def customers(request):
    if 'admin' in request.session:    
        customer_list =  Customer.objects.filter(is_staff=False).order_by('id')

        paginator = Paginator(customer_list,10)  

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }
        return render(request, 'dashboard/customer.html', context)
    else:
        return redirect('admin')


def unblock_customer(request,customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except ObjectDoesNotExist:
        return redirect('customer')  
    
    customer.is_active = True
    customer.save()

    return redirect('customer')


def block_customer(request,customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return redirect('customer')  
    customer.is_active = False
    customer.save()
    return redirect('customer')


#################  USER PROFILE & ADDRESS  #####################

# def profile(request):
#     customer = request.user
#     default_address = Address.objects.filter(user=customer, default=True).first()
#     return render(request, 'main/profile.html', {'customer': customer, 'default_address': default_address})


@login_required
def profile(request):
    customer = request.user
    default_address = None

    # Check if the user is authenticated before accessing user-related data
    if request.user.is_authenticated:
        default_address = Address.objects.filter(user=customer, default=True).first()

    return render(request, 'main/profile.html', {'customer': customer, 'default_address': default_address})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get user object
        user = request.user

        # Get user input
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Check for empty fields
        if not (first_name and last_name and email and phone):
            messages.error(request, 'Please fill in all the required fields.')
            return redirect(reverse('user:edit_profile'))
        
        # Validate phone number
        try:
            phone_validator(phone)
        except ValidationError:
            messages.error(request, 'Invalid phone number format.')
            return redirect(reverse('user:edit_profile'))

        # Update user profile information
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.number = phone

        # Update user model
        user.save()
    

        messages.success(request, 'Profile updated successfully!')
        return redirect(reverse('user:profile'))

    return render(request, 'main/update_profile.html', {'user': request.user})


def address(request):
    data = Address.objects.filter(user=request.user)
    return render(request, 'main/address.html', {'data': data})


def add_address(request):
    if request.method == 'POST':
        user = request.user
        default = request.POST.get('default', False) == 'True'
        address_name = request.POST['address_name']
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        pin = request.POST['pin']

        # Check for whitespace-only values
        if any(value.strip() == '' for value in [address_name, address_1, address_2, country, state, city, pin]):
            messages.error(request, 'Whitespace-only values are not allowed.')
            return redirect('user:add_address')

        # Check for empty values
        if not address_name or not address_1 or not country or not state or not city or not pin:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('user:add_address')

        query = Address.objects.create(
            user=user,
            default=default,
            address_name=address_name,
            address_1=address_1,
            address_2=address_2,
            country=country,
            state=state,
            city=city,
            pin=pin,
        )
        query.save()
        return redirect('user:address')
    
    return render(request, 'main/add_address.html')

def update_address(request, id):
    data = Address.objects.all()
    address = Address.objects.get(id = id)
    default = request.POST.get('default')
    if request.method == 'POST':
        default = request.POST.get('default', False) == 'True'
        address_name = request.POST['address_name']
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        pin = request.POST['pin']
        user = request.user

        if default:
            Address.objects.filter(user=user, default=True).update(default=False)

        edit = Address.objects.get(id = id)
        edit.default = default
        edit.address_name = address_name
        edit.address_1 = address_1
        edit.address_2 = address_2
        edit.country = country
        edit.state = state
        edit.city = city
        edit.pin = pin
        edit.save()
        
        return redirect('user:address')
    context = {
           "address": address,
            "data" : data
            }

    return render(request, 'main/update_address.html', context)


def delete_address(request,id):
    data = Address.objects.get(id=id) 
    data.delete()  
    return redirect('user:address')

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def searchuser(request):
    if "admin" in request.session:
        query = request.GET.get("q")

        if query:
            results = Customer.objects.filter(username__icontains=query)

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
        return render(request, "dashboard/customer.html", context)
    else:
        return redirect("admin")



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            customer = Customer.objects.get(email=email)
           
            if customer.email == email:
            
                message = generate_otp()
                sender_email = "nashirnoor2002@gmail.com"
                receiver_mail = email
                password = "qzyrtqxbcrdoqlpm"

                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_mail, message)

                except smtplib.SMTPAuthenticationError:
                    messages.error(request, 'Failed to send OTP email. Please check your email configuration.')
                    return redirect('signup')
                
                request.session['email'] =  email
                request.session['otp']   =  message
                messages.success (request, 'OTP is sent to your email')
                return redirect('reset_password')   
            
        except Customer.DoesNotExist:
            messages.info(request,"Email is not valid")
            return redirect('login')
    else:
        return redirect('login')

def generate_otp(length = 6):
    return ''.join(secrets.choice("0123456789") for i in range(length)) 

def reset_password(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            if new_password == confirm_password:
                email = request.session.get('email')
                try:
                    customer = Customer.objects.get(email=email)
                    customer.set_password(new_password)
                    customer.save()
                    del request.session['email'] 
                    del request.session['otp']
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('login')
                except Customer.DoesNotExist:
                    messages.error(request, 'Failed to reset password. Please try again later.')
                    return redirect('login')
            else:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please enter the correct OTP.')
            return redirect('reset_password')
    else:
        return render(request, 'main/passwordreset.html')
    

# views.py


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        # Check if the user is authenticated (not AnonymousUser)
        if not user.is_anonymous:
            # Check if the old password matches the user's current password
            if user.check_password(old_password):
                # Check if the new passwords match
                if new_password1 == new_password2:
                    # Set the new password for the user
                    user.set_password(new_password1)
                    user.save()

                    # Update the session to prevent the user from being logged out
                    update_session_auth_hash(request, user)

                    messages.success(request, 'Password reset successful.')
                    return redirect('user:profile')
                else:
                    messages.error(request, 'New password and confirm password do not match.')
            else:
                messages.error(request, 'Old password is incorrect.')
        else:
            messages.error(request, 'User is not authenticated.')

    return redirect('user:profile')






    
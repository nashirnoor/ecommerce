
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache
from .models import Category
from products.models import Product
from django.core.paginator import Paginator
from .forms import CategoryForm


def category_products(request, id):
    main_category = Category.objects.get(pk=id)
    products = Product.objects.filter(category=main_category, is_deleted=False)

    return render(request, "main/product_list.html", {'data': products})


def usercategory(request):
    data = Category.objects.filter(is_listed = True)
    context = {
        'data': data
    }
    return render(request,'main/main_categories.html', context )


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def category(request):
    if 'admin' in request.session:
        categories = Category.objects.all().order_by('id')
        
        
        paginator = Paginator(categories, per_page=5)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'categories': page_obj,
        }
        return render(request, 'dashboard/category.html', context)
    else:
        return redirect('admin')
    
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def add_category(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('category')
        else:
            form = CategoryForm()

        return render(request, 'dashboard/add_category.html', {'form': form})
    else:
        return redirect('admin')


#Fetch existing data 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def editcategory(request, category_id):
    if 'admin' in request.session:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'category_not_found.html')

        context = {'category': category}
        return render(request, 'dashboard/edit_category.html', context)
    else:
        return redirect ('admin')

from django.shortcuts import render,redirect
from .models import Category
from .forms import CategoryForm

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return render(request, 'category_not_found.html')

    if request.method == 'POST':
        category.category_name = request.POST.get('category_name', '')
        category.description = request.POST.get('description', '')
        category.category_offer_description = request.POST.get('offer_details', '')
        category.category_offer = request.POST.get('offer_price', '')

        # Convert the checkbox value to a boolean
        category.is_listed = request.POST.get('is_listed') == 'on'

        if 'image' in request.FILES:
            category.image = request.FILES['image']

        category.save()

        # Update products associated with the old category to the new one
        products_to_update = Product.objects.filter(category__id=id)
        for product in products_to_update:
            product.category = category
            product.save()

        return redirect('category')

    context = {'category': category}
    return render(request, 'dashboard/edit_category.html', context)


from django.contrib import messages

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def searchcategory(request):
    if "admin" in request.session:
        query = request.GET.get("q")

        if query:
            results = Category.objects.filter(category_name__icontains=query)
        else:
            results = []

        paginator = Paginator(results, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "categories": page_obj,
            "query": query,
        }
        if not results:
            messages.info(request, 'Category not found.')

        return render(request, "dashboard/category.html", context)

    else:
        return redirect("admin")


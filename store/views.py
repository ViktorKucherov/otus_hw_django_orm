from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Category, Product
from .forms import ProductForm


def index(request):
    """Главная страница - список всех товаров."""
    products = Product.objects.select_related('category').all()
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'store/index.html', context)


def category_detail(request, category_id):
    """Страница категории с товарами."""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).select_related('category')
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, product_id):
    """Страница товара."""
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'store/product_detail.html', context)


def product_create(request):
    """Создание нового товара."""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно добавлен!')
            return redirect('store:product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': categories,
        'title': 'Добавить товар',
    }
    return render(request, 'store/product_form.html', context)


def product_edit(request, product_id):
    """Редактирование товара."""
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно обновлен!')
            return redirect('store:product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'title': 'Редактировать товар',
    }
    return render(request, 'store/product_form.html', context)


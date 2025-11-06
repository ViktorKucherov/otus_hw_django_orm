from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from .tasks import log_new_product


class ProductListView(ListView):
    """ListView для отображения списка товаров."""
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Фильтрация и поиск товаров."""
        queryset = Product.objects.select_related('category').all()
        
        # Поиск
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category')
        context['selected_category'] = int(category_id) if category_id else None
        return context


class ProductDetailView(DetailView):
    """DetailView для отображения деталей товара."""
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    
    def get_queryset(self):
        """Оптимизация запросов."""
        return Product.objects.select_related('category')
    
    def get_context_data(self, **kwargs):
        """Добавление категорий в контекст."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(CreateView):
    """CreateView для добавления нового товара."""
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить товар'
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        """Обработка успешной валидации формы."""
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно добавлен!')
        # Запуск фоновой задачи Celery для логирования
        log_new_product.delay(self.object.id)
        return response
    
    def get_success_url(self):
        """URL для перенаправления после успешного создания."""
        return reverse_lazy('store:product_detail', kwargs={'product_id': self.object.id})


class ProductUpdateView(UpdateView):
    """UpdateView для редактирования товара."""
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    pk_url_kwarg = 'product_id'
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать товар'
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        """Обработка успешной валидации формы."""
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """URL для перенаправления после успешного обновления."""
        return reverse_lazy('store:product_detail', kwargs={'product_id': self.object.id})


class ProductDeleteView(DeleteView):
    """DeleteView для удаления товара."""
    model = Product
    template_name = 'store/product_confirm_delete.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('store:index')
    
    def delete(self, request, *args, **kwargs):
        """Обработка удаления с сообщением."""
        product = self.get_object()
        messages.success(request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


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


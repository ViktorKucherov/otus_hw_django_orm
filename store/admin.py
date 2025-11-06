from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from decimal import Decimal
from .models import Category, Product


class PriceRangeFilter(SimpleListFilter):
    """Кастомный фильтр по диапазонам цен."""
    title = 'Цена'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-1000', 'До 1 000 ₽'),
            ('1000-5000', '1 000 - 5 000 ₽'),
            ('5000-20000', '5 000 - 20 000 ₽'),
            ('20000+', 'Свыше 20 000 ₽'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return queryset.filter(price__lt=Decimal('1000.00'))
        if self.value() == '1000-5000':
            return queryset.filter(price__gte=Decimal('1000.00'), price__lt=Decimal('5000.00'))
        if self.value() == '5000-20000':
            return queryset.filter(price__gte=Decimal('5000.00'), price__lt=Decimal('20000.00'))
        if self.value() == '20000+':
            return queryset.filter(price__gte=Decimal('20000.00'))
        return queryset


class ProductInline(admin.TabularInline):
    """Инлайн для отображения товаров в категории."""
    model = Product
    extra = 1
    fields = ('name', 'price', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Продвинутая настройка админки для категорий."""
    list_display = ('name', 'description', 'products_count')
    search_fields = ('name', 'description')
    list_per_page = 20
    inlines = [ProductInline]
    
    def products_count(self, obj):
        """Количество товаров в категории."""
        count = obj.products.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Продвинутая настройка админки для товаров."""
    list_display = ('name', 'price', 'formatted_price', 'category', 'created_at', 'is_recent')
    list_filter = ('category', 'created_at', PriceRangeFilter)
    search_fields = ('name', 'description', 'category__name')
    date_hierarchy = 'created_at'
    list_editable = ('price', 'category')
    list_per_page = 25
    list_select_related = ('category',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Цена', {
            'fields': ('price',)
        }),
        ('Дополнительно', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_price(self, obj):
        """Форматированная цена с символом рубля."""
        return format_html(
            '<strong>{:,.0f} ₽</strong>',
            float(obj.price)
        )
    formatted_price.short_description = 'Цена'
    
    def is_recent(self, obj):
        """Проверка, является ли товар недавно созданным."""
        from django.utils import timezone
        from datetime import timedelta
        recent = timezone.now() - timedelta(days=7)
        if obj.created_at >= recent:
            return format_html('<span style="color: green;">Новый</span>')
        return format_html('<span style="color: gray;">-</span>')
    is_recent.short_description = 'Статус'
    is_recent.boolean = True
    
    @admin.action(description='Увеличить цену на 10%%')
    def make_expensive(self, request, queryset):
        """Действие: увеличить цену на 10%."""
        from django.db.models import F
        updated = queryset.update(price=F('price') * 1.1)
        self.message_user(request, f'Цена увеличена на 10% для {updated} товаров.')
    
    @admin.action(description='Уменьшить цену на 10%%')
    def make_cheap(self, request, queryset):
        """Действие: уменьшить цену на 10%."""
        from django.db.models import F
        updated = queryset.update(price=F('price') * 0.9)
        self.message_user(request, f'Цена уменьшена на 10% для {updated} товаров.')
    
    @admin.action(description='Увеличить цену на 20%%')
    def make_very_expensive(self, request, queryset):
        """Действие: увеличить цену на 20%."""
        from django.db.models import F
        updated = queryset.update(price=F('price') * 1.2)
        self.message_user(request, f'Цена увеличена на 20% для {updated} товаров.')
    
    @admin.action(description='Сбросить цену до 1000 ₽')
    def reset_price(self, request, queryset):
        """Действие: установить цену 1000 ₽."""
        from decimal import Decimal
        updated = queryset.update(price=Decimal('1000.00'))
        self.message_user(request, f'Цена установлена в 1000 ₽ для {updated} товаров.')
    
    actions = [make_expensive, make_cheap, make_very_expensive, reset_price]


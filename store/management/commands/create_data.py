"""
Кастомная команда для создания тестовых данных через ORM.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Создает тестовые данные для моделей Category и Product'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаем создание данных...'))

        # Создание категорий
        category1, created = Category.objects.get_or_create(
            name='Электроника',
            defaults={'description': 'Электронные устройства и гаджеты'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создана категория: {category1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'→ Категория уже существует: {category1.name}'))

        category2, created = Category.objects.get_or_create(
            name='Одежда',
            defaults={'description': 'Одежда и аксессуары'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создана категория: {category2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'→ Категория уже существует: {category2.name}'))

        category3, created = Category.objects.get_or_create(
            name='Книги',
            defaults={'description': 'Книги и литература'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создана категория: {category3.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'→ Категория уже существует: {category3.name}'))

        # Создание товаров
        products_data = [
            {
                'name': 'Смартфон',
                'description': 'Современный смартфон с хорошей камерой',
                'price': Decimal('29999.00'),
                'category': category1,
            },
            {
                'name': 'Ноутбук',
                'description': 'Мощный ноутбук для работы и игр',
                'price': Decimal('89999.00'),
                'category': category1,
            },
            {
                'name': 'Футболка',
                'description': 'Удобная хлопковая футболка',
                'price': Decimal('999.00'),
                'category': category2,
            },
            {
                'name': 'Джинсы',
                'description': 'Классические джинсы',
                'price': Decimal('2999.00'),
                'category': category2,
            },
            {
                'name': 'Python для начинающих',
                'description': 'Учебник по программированию на Python',
                'price': Decimal('1299.00'),
                'category': category3,
            },
            {
                'name': 'Django в примерах',
                'description': 'Практическое руководство по Django',
                'price': Decimal('1599.00'),
                'category': category3,
            },
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'created_at': timezone.now(),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Создан товар: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'→ Товар уже существует: {product.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Готово! Создано товаров: {created_count}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Всего категорий: {Category.objects.count()}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Всего товаров: {Product.objects.count()}'
        ))


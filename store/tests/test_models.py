"""
Тесты для моделей Category и Product.
Проверка CRUD операций.
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from store.models import Category, Product


@pytest.mark.django_db
class TestCategoryModel:
    """Тесты для модели Category."""
    
    def test_create_category(self):
        """Тест создания категории."""
        category = Category.objects.create(
            name='Тестовая категория',
            description='Описание тестовой категории'
        )
        assert category.id is not None
        assert category.name == 'Тестовая категория'
        assert category.description == 'Описание тестовой категории'
        assert str(category) == 'Тестовая категория'
    
    def test_read_category(self):
        """Тест чтения категории."""
        category = Category.objects.create(
            name='Категория для чтения',
            description='Описание'
        )
        retrieved = Category.objects.get(id=category.id)
        assert retrieved.name == 'Категория для чтения'
        assert retrieved.description == 'Описание'
    
    def test_update_category(self):
        """Тест обновления категории."""
        category = Category.objects.create(
            name='Исходная категория',
            description='Исходное описание'
        )
        category.name = 'Обновленная категория'
        category.description = 'Обновленное описание'
        category.save()
        
        updated = Category.objects.get(id=category.id)
        assert updated.name == 'Обновленная категория'
        assert updated.description == 'Обновленное описание'
    
    def test_delete_category(self):
        """Тест удаления категории."""
        category = Category.objects.create(
            name='Категория для удаления',
            description='Описание'
        )
        category_id = category.id
        category.delete()
        
        assert not Category.objects.filter(id=category_id).exists()


@pytest.mark.django_db
class TestProductModel:
    """Тесты для модели Product."""
    
    @pytest.fixture
    def category(self):
        """Фикстура для создания категории."""
        return Category.objects.create(
            name='Тестовая категория',
            description='Описание'
        )
    
    def test_create_product(self, category):
        """Тест создания товара."""
        product = Product.objects.create(
            name='Тестовый товар',
            description='Описание товара',
            price=Decimal('1000.00'),
            category=category
        )
        assert product.id is not None
        assert product.name == 'Тестовый товар'
        assert product.description == 'Описание товара'
        assert product.price == Decimal('1000.00')
        assert product.category == category
        assert product.created_at is not None
        assert str(product) == 'Тестовый товар'
    
    def test_read_product(self, category):
        """Тест чтения товара."""
        product = Product.objects.create(
            name='Товар для чтения',
            description='Описание',
            price=Decimal('2000.00'),
            category=category
        )
        retrieved = Product.objects.get(id=product.id)
        assert retrieved.name == 'Товар для чтения'
        assert retrieved.price == Decimal('2000.00')
        assert retrieved.category == category
    
    def test_update_product(self, category):
        """Тест обновления товара."""
        product = Product.objects.create(
            name='Исходный товар',
            description='Исходное описание',
            price=Decimal('1000.00'),
            category=category
        )
        product.name = 'Обновленный товар'
        product.price = Decimal('1500.00')
        product.save()
        
        updated = Product.objects.get(id=product.id)
        assert updated.name == 'Обновленный товар'
        assert updated.price == Decimal('1500.00')
    
    def test_delete_product(self, category):
        """Тест удаления товара."""
        product = Product.objects.create(
            name='Товар для удаления',
            description='Описание',
            price=Decimal('1000.00'),
            category=category
        )
        product_id = product.id
        product.delete()
        
        assert not Product.objects.filter(id=product_id).exists()
    
    def test_product_foreign_key_relationship(self, category):
        """Тест связи ForeignKey между Product и Category."""
        product = Product.objects.create(
            name='Товар с категорией',
            description='Описание',
            price=Decimal('1000.00'),
            category=category
        )
        
        # Проверка связи от Product к Category
        assert product.category == category
        
        # Проверка обратной связи через related_name
        assert product in category.products.all()
    
    def test_category_cascade_delete(self, category):
        """Тест каскадного удаления товаров при удалении категории."""
        product1 = Product.objects.create(
            name='Товар 1',
            description='Описание',
            price=Decimal('1000.00'),
            category=category
        )
        product2 = Product.objects.create(
            name='Товар 2',
            description='Описание',
            price=Decimal('2000.00'),
            category=category
        )
        
        product1_id = product1.id
        product2_id = product2.id
        
        category.delete()
        
        # Товары должны быть удалены вместе с категорией
        assert not Product.objects.filter(id=product1_id).exists()
        assert not Product.objects.filter(id=product2_id).exists()
    
    def test_product_ordering(self, category):
        """Тест сортировки товаров по дате создания (новые первыми)."""
        product1 = Product.objects.create(
            name='Товар 1',
            description='Описание',
            price=Decimal('1000.00'),
            category=category
        )
        product2 = Product.objects.create(
            name='Товар 2',
            description='Описание',
            price=Decimal('2000.00'),
            category=category
        )
        
        products = Product.objects.all()
        assert products.first() == product2  # Новый товар первым
        assert products.last() == product1
    
    def test_category_ordering(self):
        """Тест сортировки категорий по названию."""
        cat2 = Category.objects.create(name='Б', description='Описание')
        cat1 = Category.objects.create(name='А', description='Описание')
        cat3 = Category.objects.create(name='В', description='Описание')
        
        categories = Category.objects.all()
        assert categories[0] == cat1
        assert categories[1] == cat2
        assert categories[2] == cat3


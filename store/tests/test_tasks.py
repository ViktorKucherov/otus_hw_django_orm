"""
Тесты для фоновых задач Celery.
"""
import pytest
from decimal import Decimal
from store.models import Category, Product
from store.tasks import log_new_product


@pytest.mark.django_db
class TestCeleryTasks:
    """Тесты для фоновых задач Celery."""
    
    def test_log_new_product_task(self):
        """Тест задачи логирования нового товара."""
        # Создаем категорию и товар
        category = Category.objects.create(
            name='Тестовая категория',
            description='Описание'
        )
        product = Product.objects.create(
            name='Тестовый товар',
            description='Описание товара',
            price=Decimal('1000.00'),
            category=category
        )
        
        # Выполняем задачу синхронно (для тестирования)
        result = log_new_product(product.id)
        
        # Проверяем результат
        assert result['status'] == 'success'
        assert result['product_id'] == product.id
        assert result['product_name'] == 'Тестовый товар'
        assert result['category'] == 'Тестовая категория'
        
        # Проверяем, что товар существует
        assert Product.objects.filter(id=product.id).exists()
        assert Product.objects.get(id=product.id).name == 'Тестовый товар'
    
    def test_log_new_product_task_with_invalid_id(self):
        """Тест задачи с несуществующим ID товара."""
        # Пытаемся выполнить задачу с несуществующим ID
        result = log_new_product(99999)
        
        # Проверяем, что задача вернула ошибку
        assert result['status'] == 'error'
        assert 'не найден' in result['message']
        assert result['product_id'] == 99999
    
    def test_log_new_product_task_integration(self):
        """Интеграционный тест: создание товара и запуск задачи."""
        category = Category.objects.create(
            name='Категория для интеграции',
            description='Описание'
        )
        
        product = Product.objects.create(
            name='Интеграционный товар',
            description='Тестовое описание',
            price=Decimal('2500.00'),
            category=category
        )
        
        # Выполняем задачу
        result = log_new_product.apply(args=[product.id])
        
        # Проверяем, что задача выполнена успешно
        assert result.successful() or result.state == 'SUCCESS'


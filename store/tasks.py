"""
Фоновые задачи Celery для приложения store.
"""
import logging
from celery import shared_task
from store.models import Product

# Настройка логгера для задач
logger = logging.getLogger(__name__)


@shared_task
def log_new_product(product_id):
    """
    Фоновая задача для логирования информации о добавлении нового товара.
    
    Args:
        product_id: ID созданного товара
    """
    try:
        product = Product.objects.get(id=product_id)
        
        logger.info("=" * 70)
        logger.info("НОВЫЙ ТОВАР ДОБАВЛЕН В МАГАЗИН")
        logger.info("=" * 70)
        logger.info(f"ID товара: {product.id}")
        logger.info(f"Название: {product.name}")
        logger.info(f"Категория: {product.category.name}")
        logger.info(f"Цена: {product.price} руб.")
        if product.description:
            logger.info(f"Описание: {product.description}")
        logger.info(f"Дата создания: {product.created_at}")
        logger.info("=" * 70)
        logger.info(f"Задача выполнена успешно для товара '{product.name}'")
        logger.info("=" * 70)
        
        return {
            'status': 'success',
            'product_id': product.id,
            'product_name': product.name,
            'category': product.category.name,
            'price': str(product.price)
        }
    except Product.DoesNotExist:
        logger.error(f"ОШИБКА: Товар с ID {product_id} не найден!")
        return {
            'status': 'error',
            'message': f'Товар с ID {product_id} не найден',
            'product_id': product_id
        }
    except Exception as e:
        logger.exception(f"ОШИБКА при выполнении задачи: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'product_id': product_id
        }


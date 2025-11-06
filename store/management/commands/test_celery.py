"""
Кастомная команда для тестирования работы Celery.
"""
from django.core.management.base import BaseCommand
from store.tasks import log_new_product
from store.models import Product


class Command(BaseCommand):
    help = 'Тестирование работы Celery - запускает задачу для последнего товара'

    def handle(self, *args, **options):
        try:
            product = Product.objects.last()
            
            if not product:
                self.stdout.write(self.style.ERROR(
                    'Нет товаров в базе данных. Сначала создайте товары через команду create_data'
                ))
                return
            
            self.stdout.write(self.style.SUCCESS(
                f'Найден товар: {product.name} (ID: {product.id})'
            ))
            self.stdout.write('')
            self.stdout.write('Запускаю фоновую задачу Celery...')
            self.stdout.write('')
            
            result = log_new_product.delay(product.id)
            
            self.stdout.write(self.style.SUCCESS(
                f'Задача отправлена в очередь! Task ID: {result.id}'
            ))
            self.stdout.write('')
            
            try:
                task_result = result.get(timeout=10)
                self.stdout.write(self.style.SUCCESS('Результат выполнения задачи:'))
                self.stdout.write(str(task_result))
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f'Не удалось получить результат (возможно, worker не запущен): {e}'
                ))
                self.stdout.write('')
                self.stdout.write('Убедитесь, что Redis запущен и Celery worker работает')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))


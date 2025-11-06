"""
Конфигурация Celery для проекта.
"""
import os
import logging
from celery import Celery
from celery.signals import setup_logging

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра Celery
app = Celery('config')

# Загрузка настроек из Django settings с префиксом CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех приложений Django
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs):
    """Настройка логирования для Celery."""
    from django.conf import settings
    if hasattr(settings, 'LOGGING'):
        import logging.config
        logging.config.dictConfig(settings.LOGGING)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Отладочная задача для проверки работы Celery."""
    logger = logging.getLogger(__name__)
    logger.info(f'Request: {self.request!r}')


from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/edit/', views.product_edit, name='product_edit'),
]


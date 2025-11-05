from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:product_id>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]


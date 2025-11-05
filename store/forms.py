from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Форма для добавления и редактирования товара."""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена (₽)',
            'category': 'Категория',
        }
    
    def clean_price(self):
        """Валидация цены."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        if price is not None and price == 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
    
    def clean_name(self):
        """Валидация названия."""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return name.strip()



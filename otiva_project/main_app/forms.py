from django import forms
from main_app.models import Good, Device, Manufacturer, DeviceType
from user_app.models import OtivaUser


def get_all_brands():
    queryset = Manufacturer.objects.values_list('name', 'name').distinct()
    return tuple(queryset)


class AddGoodForm(forms.Form):
    brand = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        label='Название бренда',
        widget=forms.widgets.Select(attrs={'class': 'form-select'})
    )
    type = forms.ModelChoiceField(
        queryset=DeviceType.objects.all(),
        label='Тип устройства',
        widget=forms.widgets.Select(attrs={'class': 'form-select'})
    )
    
    condition = forms.ChoiceField(
        choices=Good.CONDITIONS,
        widget=forms.widgets.Select(attrs={'class': 'form-select'}))
    
    model = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label='Модель',
        widget=forms.widgets.Select(attrs={'class': 'form-select'}),
    )
    # p_n = forms.CharField(label='Номер детали', required=False)
    
    price = forms.DecimalField(
        label='Цена',
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:30%'
        }),
    )
    
    period = forms.IntegerField(
        label='Период',
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:30%'
        }),
    )
    
    images = forms.FileField(
        label='Добавить фото',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'multiple': True,
            
        })
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.widgets.Textarea(attrs={
            'class': 'form-control',
            'rows': '5',
        })
    )


class AddDeviceForm(forms.Form):
    """Форма добавления устройства"""
    
    dev_model = forms.CharField(max_length=100, label='Модель аппарата')
    dev_type = forms.CharField(max_length=100, label='Тип аппарата')
    manuf = forms.CharField(max_length=100, label='Производитель')
    
    params = forms.CharField(max_length=3000, label='Параметры')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dev_model'].widget.attrs.update({'class': 'form-control'})
        self.fields['dev_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['manuf'].widget.attrs.update({'class': 'form-control'})
        self.fields['params'].widget = forms.widgets.Textarea(attrs={'class': 'form-control'})
    
    def save(self, commit=True):
        dev_type_, _ = DeviceType.objects.get_or_create(type_name=self.cleaned_data['dev_type'])
        manuf_, _ = Manufacturer.objects.get_or_create(name=self.cleaned_data['manuf'])
        
        if self.errors:
            raise ValueError('Ошибка сохранения Устройства')
        
        new_device = Device.objects.create(
            dev_model=self.cleaned_data['dev_model'],
            dev_type=dev_type_,
            manuf=manuf_,
            params=self.cleaned_data['params']
        )
        return new_device


class UserPersonalDataForm(forms.Form):
    """Форма лияных данных пользователя"""
    
    # avatar = forms.FileField(label='Добавить фото', required=False,)
    user_type = forms.ChoiceField(choices=OtivaUser.USER_TYPES, label='*Тип учетной записи')
    first_name = forms.CharField(max_length=100, label='*Имя')
    surname = forms.CharField(max_length=100, label='Фамилия', required=False)
    phone = forms.CharField(max_length=20, validators=[], label='*Телефон')
    city = forms.CharField(max_length=50, label='*Город')
    area = forms.CharField(max_length=50, label='Регион', required=False)
    post_code = forms.CharField(max_length=6, label='Почтовый индекс', required=False)
    street = forms.CharField(max_length=50, label='Улица', required=False)
    building = forms.CharField(max_length=5, label='Дом', required=False)
    apartment = forms.CharField(max_length=50, label='Квартира', required=False)
    metro = forms.CharField(max_length=50, label='Метро', required=False)
    map_url = forms.CharField(max_length=50, label='Ссылка на Яндекс Карты', required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs.update({'class': 'form-select'})
        
        for field in self.fields:
            if field != 'user_type':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

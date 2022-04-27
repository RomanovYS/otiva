from django import forms

from advertisement_app.models import TechAdvertisement


class TechAdvertisementCreateForm(forms.ModelForm):
    """Форма создания объявления техники"""

    photos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TechAdvertisement
        fields = ('title', 'description', 'condition', 'placement_period', 'price', 'photos')


class TechAdvertisementEditForm(forms.ModelForm):
    """Редактирования объявления техники"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TechAdvertisement
        fields = ('title', 'description', 'condition', 'placement_period', 'price')

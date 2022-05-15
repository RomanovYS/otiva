from django import forms


class AddGoodForm(forms.Form):

    brand = forms.CharField()
    type = forms.CharField()
    condition = forms.CharField()
    model = forms.CharField()
    p_n = forms.CharField()
    price = forms.DecimalField()
    period = forms.IntegerField()
    add_photo = forms.FileField()
    description = forms.CharField(widget=forms.Textarea())
    
from django import forms
from .models import Tea

class TeaForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Enter your Tea",
                                   "class": "form-control",
                               }
                           ), label="")
    
    class Meta:
        model = Tea
        exclude = ("user",)
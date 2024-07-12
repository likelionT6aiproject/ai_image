from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    prompt = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter prompt',
        'style': 'margin-top: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%;'
    }))
    
    class Meta:
        model = UploadedImage
        fields = ['image', 'prompt']

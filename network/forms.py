from django import forms
from .settings import NEW_POST_LENGTH

class NewPostForm(forms.Form):
    post = forms.CharField(label='', max_length=NEW_POST_LENGTH, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Add new post',
        'style': 'height: 120px'}))
    user = forms.IntegerField(required=True, widget=forms.HiddenInput())
from django import forms
from .settings import NEW_POST_LENGTH

class NewPostForm(forms.Form):
    post = forms.CharField(label='', max_length=NEW_POST_LENGTH, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'newpost',
        'placeholder': 'Add new post',
        'style': 'height: 120px'}))
    max_length = forms.IntegerField(required=False, initial=NEW_POST_LENGTH, widget=forms.HiddenInput(attrs={
        'id': 'maxlength'})) # This is used to expose the value of the max length setting for the javascript
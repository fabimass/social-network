from django import forms

class NewPostForm(forms.Form):
    post = forms.CharField(label='', max_length=400, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Add new post',
        'style': 'height: 120px'}))
    user = forms.IntegerField(required=True, widget=forms.HiddenInput())
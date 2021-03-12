from django.forms import ModelForm
from django import forms
from .models import ListItem, Comment
from datetime import datetime

class ListItemForm(ModelForm):
    class Meta:
        model = ListItem
        fields = ["name", "description", "price", "category", "image_link"]


class CommentForm(forms.Form):
    text = forms.Textarea()
    item = forms.HiddenInput()
    user = forms.HiddenInput()
        
from django import forms
from django.utils.safestring import mark_safe
from ServerClient.models import Lab
from .utils import new_choices


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             'required': True,
                                                             'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password',
                                                                 'required': True}))


class QueryForm(forms.Form):

    select_seccion = forms.ChoiceField(label="Pick a section",
                                       choices=new_choices(),
                                       widget=forms.Select(attrs={
                                            'id': 'section_select'
                                        }
                                       ))
    query_name = forms.CharField(label= 'Query Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Name your query here',
                                                             'name': 'query[]',
                                                             'required': True}))
    query_body = forms.ChoiceField(label= mark_safe(''),
                                   widget=forms.Select(attrs={
                                            'id': '0-0',
                                            'onChange': 'loadQueryArguments()'}))


class ResultsForm(forms.Form):
    select_seccion = forms.ChoiceField(label="Pick a section",
                                       choices= new_choices(),
                                       widget=forms.Select(attrs={
                                            'id': 'section_select'
                                        }
                                       ))



from django import forms
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             'required': True,
                                                             'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password',
                                                                 'required': True}))


class QueryForm(forms.Form):
    query_name = forms.CharField(label= 'Nombre de la consulta',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Nombra tu query aqui',
                                                             'name': 'query[]',
                                                             'required': True,
                                                             'autofocus': True}))
    query_body = forms.ChoiceField(label= mark_safe(''),
                                   widget=forms.Select(attrs={
                                            'id': '0-0',
                                            'onChange': 'loadQueryArguments()'}))



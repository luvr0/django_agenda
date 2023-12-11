from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from contact.models import Contact
from django.urls import reverse 
from django import forms
from typing import Any

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Nome'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Sobrenome'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Ex.: +55(35)991234567'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'exemplo@gmail.com'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Sua descrição'
        })

    class Meta:
        model = Contact
        fields = 'first_name', 'last_name', 'phone', 'email', 'description', 'category',

    def clean(self):
        clean_data = self.cleaned_data
        first_name = clean_data.get('first_name')
        last_name = clean_data.get('last_name')

        if first_name == last_name:
            self.add_error(
                'first_name',
                ValidationError(
                    'Nome não pode ser igual ao sobrenome.',
                    code='invalid'
                )
            )

            self.add_error(
                'last_name',
                ValidationError(
                    'Sobrenome não pode ser igual ao nome.',
                    code='invalid'
                )
            )

        return super().clean()

@login_required(login_url='contact:login')
def create(request):
    var_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        text = {
            'form': form,
            'var_action': var_action
        }
        
        if form.is_valid():
            var_save = form.save(commit=False)
            var_save.owner = request.user
            var_save.save()
            return redirect('contact:update', id=var_save.pk    )

        return render(
            request,
            'contact/crud_create.html',
            text
        )

    text = {
        'form': ContactForm(),
        'var_action': var_action
    }

    return render(
        request,
        'contact/crud_create.html',
        text
    )
@login_required(login_url='contact:login')
def update(request, id):
    up_contact = get_object_or_404(Contact, pk=id, show=True, owner=request.user)
    var_action = reverse('contact:update', args=(id,))
    
    if request.method == 'POST':
        form = ContactForm(data=request.POST, instance=up_contact)
        text = {
            'form': form,
            'var_action': var_action
        }

        if form.is_valid():
            var_save = form.save()
            return redirect('contact:update', id=var_save.id)

        return render(
            request,
            'contact/crud_create.html',
            text
        )

    text = {
        'form': ContactForm(instance=up_contact),
        'var_action': var_action
    }

    return render(
        request,
        'contact/crud_create.html',
        text
    )
@login_required(login_url='contact:login')
def delete(request, id):
    del_contact = get_object_or_404(Contact, pk=id, show=True, owner=request.user)

    del_contact.delete()
    return redirect('contact:index')

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True
    )
    last_name = forms.CharField(
        required=True
    )
    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('E-mail já existente', code='invalid')
            )

        return email
    
class RegisterUpdate(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )
    password2 = forms.CharField(
        label='Repetir senha',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('E-mail já existente', code='invalid')
                )

        return email
    
    def save(self, commit=True):
        clean_data = self.cleaned_data
        user = super().save(commit=False)
        password = clean_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )



        return password1
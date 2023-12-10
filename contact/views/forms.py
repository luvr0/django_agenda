from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact
from django.urls import reverse 
from django import forms
from contact.models import Contact

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


def create(request):
    var_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        text = {
            'form': form,
            'var_action': var_action
        }
        
        if form.is_valid():
            var_save = form.save()
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

def update(request, id):
    up_contact = get_object_or_404(Contact, pk=id, show=True)
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
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact


def home(request):
    contacts = Contact.objects.filter(show=True) 

    text = {
        'contacts': contacts,
        'title_web': 'Contatos -',
    }

    return render(
        request,
        'contact/index.html',
        text
    )

def search(request):
    search_module = request.GET.get('q', '').strip()

    if search_module == '':
        return redirect('contact:index')

    contacts = Contact.objects.filter(show=True).filter(
        Q(first_name__icontains=search_module) |
        Q(last_name__icontains=search_module)  |
        Q(email__icontains=search_module) |
        Q(phone__icontains=search_module)
        )

    text = {
        'contacts': contacts,
        'title_web': 'Pesquisa -',
    }

    return render(
        request,
        'contact/index.html',
        text
    )

def contact(request, id):
    single_contact = get_object_or_404(Contact.objects.filter(pk=id), show=True)

    title_web = f'{single_contact.first_name} {single_contact.last_name} -'

    text = {
        'contact': single_contact,
        'title_web': title_web,
    }

    return render(
        request,
        'contact/single_contact.html',
        text
    )


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator


def home(request):
    contacts = Contact.objects.filter(show=True)

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    text = {
        'page_obj': page_obj,
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

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    text = {
        'page_obj': page_obj,
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


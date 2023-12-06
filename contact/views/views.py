from django.shortcuts import render, get_object_or_404
from contact.models import Contact


def home(request):
    contacts = Contact.objects.filter(show=True) 

    text = {
        'contacts': contacts,
    }

    return render(
        request,
        'contact/index.html',
        text
    )

def contact(request, id):
    single_contact = get_object_or_404(Contact.objects.filter(pk=id), show=True)

    text = {
        'contact': single_contact,
    }

    return render(
        request,
        'contact/single_contact.html',
        text
    )


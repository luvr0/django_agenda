from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator


def create(request):
    text = {

    }

    return render(
        request,
        'contact/crud_create.html',
        text
    )
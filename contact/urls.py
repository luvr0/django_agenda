from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.home, name='index'),
    path('contact/<int:id>/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'),
]

from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('<int:id>/', views.contact, name='contact'),
    path('', views.home, name='index'),
]

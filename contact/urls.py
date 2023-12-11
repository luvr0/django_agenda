from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.home, name='index'),

    path('contact/<int:id>/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'),
    path('contact/<int:id>/update/', views.update, name='update'),
    path('contact/<int:id>/delete/', views.delete, name='delete'),

    path('user/create/', views.register, name='register'),
    path('user/login/', views.user_login, name='login'),
    path('user/logout/', views.user_logout, name='logout'),
    path('user/update/', views.user_update, name='user_update'),

]

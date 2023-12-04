from django.contrib import admin

from contact.models import Contact, Category

@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'phone',
    ordering = 'id',
    search_fields = 'id', 'first_name',
    list_per_page = 5


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = 'name',
    ordering = 'id',
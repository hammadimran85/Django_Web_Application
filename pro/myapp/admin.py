from django.contrib import admin
from .models import customer, extended, book

# Register your models here.
admin.site.register(customer)
admin.site.register(extended)
admin.site.register(book)

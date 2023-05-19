from django.contrib import admin
from .models import customer
from .models import extended

# Register your models here.
admin.site.register(customer)
admin.site.register(extended)

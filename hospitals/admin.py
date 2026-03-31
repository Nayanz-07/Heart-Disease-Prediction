from django.contrib import admin
from .models import Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'rating']
    list_filter = ['state']
    search_fields = ['name', 'city']

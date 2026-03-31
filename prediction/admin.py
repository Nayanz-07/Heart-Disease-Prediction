from django.contrib import admin
from .models import PredictionRecord

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display  = ['user', 'age', 'chol', 'prediction', 'probability', 'created_at']
    list_filter   = ['prediction', 'sex']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

from django.contrib import admin
from .models import Politician
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(Politician)
class PoliticianAdmin(ImportExportModelAdmin):
    pass


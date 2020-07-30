from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(NormalFeed)
admin.site.register(SmallFeed)
admin.site.register(Comment)
admin.site.register(CommentToComment)

# Register your models here.
@admin.register(Politician)
class PoliticianAdmin(ImportExportModelAdmin):
    pass


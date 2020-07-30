from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Politician)
admin.site.register(NormalFeed)
admin.site.register(SmallFeed)
admin.site.register(Comment)
admin.site.register(CommentToComment)
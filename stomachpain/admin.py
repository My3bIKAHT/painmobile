from django.contrib import admin

# Register your models here.

from .models import Question, Drug

admin.site.register(Question)
admin.site.register(Drug)
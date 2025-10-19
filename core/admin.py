from django.contrib import admin
from .models import User, Case, Question, Subject, SchoolClass, Schedule

admin.site.register(User)
admin.site.register(Case)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(SchoolClass)
admin.site.register(Schedule)

from django.contrib import admin
from .models import User, Course, Application, Review

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Application)
admin.site.register(Review)

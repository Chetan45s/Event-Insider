from django.contrib import admin
from .models import post_event,club,Profile, BlogComment, RegistrationForEvent
from django.contrib.admin.options import ModelAdmin

# Register your models here.

# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','date_posted','author')



admin.site.register(post_event, PostAdmin)
admin.site.register(club)
admin.site.register(Profile)
admin.site.register(BlogComment)
admin.site.register(RegistrationForEvent)

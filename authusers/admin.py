from django.contrib import admin
from .models import User , Profile,ContactUs
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username' , 'email', 'date_joined']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_image','full_name','bio','phone']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','phone','subject','message']



admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ContactUs,ContactAdmin)

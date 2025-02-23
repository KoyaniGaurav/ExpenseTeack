from django.contrib import admin
from .models import Expence, UserReg
@admin.register(UserReg)
class UserAdmin(admin.ModelAdmin):
    list_display = ['userId', 'name', 'email']
# Register your models here.

@admin.register(Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ['expance_name','cost','created_at','category','userId']

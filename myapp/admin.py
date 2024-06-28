from django.contrib import admin
from .models import User, Department, ATM, OS, PermissionType, UserPermission, \
    Basis, Service, AT, DataBase, Frontend, Backend, Hardware, Host

admin.site.register(User)
admin.site.register(Department)
admin.site.register(ATM)
admin.site.register(OS)
admin.site.register(Basis)
admin.site.register(Service)
admin.site.register(UserPermission)
admin.site.register(AT)
admin.site.register(Frontend)
admin.site.register(Backend)
admin.site.register(DataBase)
admin.site.register(Hardware)
admin.site.register(Host)

@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
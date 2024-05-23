from django.contrib import admin
from .models import User, Department, Server, ATM, OS, PermissionType, UserPermission, \
    Basis, ComputerLaptop, Socket, AppService

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Server)
admin.site.register(ATM)
admin.site.register(OS)
admin.site.register(Basis)
admin.site.register(ComputerLaptop)
admin.site.register(Socket)
admin.site.register(AppService)
admin.site.register(UserPermission)

@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
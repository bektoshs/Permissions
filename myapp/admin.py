from django.contrib import admin
from .models import User, Department, ATM, OS, PermissionType, UserPermission, \
    Basis, Service, AT, DataBase, Frontend, Backend, Hardware, Host
from import_export.admin import ImportExportModelAdmin


@admin.register(User)
class UserData(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'role', 'is_admin')
    search_fields = ('first_name', 'last_name', 'department__name', 'role', 'is_admin')

@admin.register(Department)
class DepartmentData(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ATM)
class ATMData(ImportExportModelAdmin):
    list_display = ('location', 'model', 'os', 'status')
    search_fields = ('location', 'model', 'os__name', 'status')

@admin.register(OS)
class OSData(ImportExportModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ('name', 'comment')

@admin.register(Basis)
class BasisData(ImportExportModelAdmin):
    list_display = ('title', 'reg_number', 'basis_file')
    search_fields = ('title', 'reg_number', 'basis_file')

@admin.register(Service)
class ServiceData(ImportExportModelAdmin):
    list_display = ('name', 'version', 'service_type', 'status')
    search_fields = ('name', 'version', 'service_type', 'status')


@admin.register(UserPermission)
class UserPermissionData(ImportExportModelAdmin):
    list_display = ('subject_id', 'subject', 'object_id', 'object', 'permission', 'basis_given_by', 'given_date',
                    'basis', 'expire_date')
    search_fields = ('subject_id', 'subject', 'object_id', 'object', 'permission__name', 'basis_given_by__name',
                     'basis__name', 'given_date', 'expire_date')

@admin.register(AT)
class ATData(ImportExportModelAdmin):
    list_display = ('name', 'database', 'backend', 'frontend', 'comment')
    search_fields = ('name', 'database__name', 'backend__name', 'frontend__name', 'comment')

@admin.register(Frontend)
class FrontendData(ImportExportModelAdmin):
    list_display = ('name', 'ip_address', 'host', 'soft')
    search_fields = ('name', 'ip_address', 'host__name', 'soft__name')

@admin.register(Backend)
class BackendData(ImportExportModelAdmin):
    list_display = ('name', 'ip_address', 'host', 'soft')
    search_fields = ('name', 'ip_address', 'host__name', 'soft__name')

@admin.register(DataBase)
class DataBaseData(ImportExportModelAdmin):
    list_display = ('name', 'ip_address', 'host', 'soft')
    search_fields = ('name', 'ip_address', 'host__name', 'soft__name')

@admin.register(Hardware)
class HardwareData(ImportExportModelAdmin):
    list_display = ('inventor_number', 'serial_number', 'type', 'status', 'model', 'manager', 'manager_ip',
                    'responsible_employee', 'responsible_department')
    search_fields = ('inventor_number', 'serial_number', 'type', 'status', 'model', 'manager', 'manager_ip',
                     'responsible_employee__first_name', 'responsible_employee__last_name',
                     'responsible_department__name')

@admin.register(Host)
class HostData(ImportExportModelAdmin):
    list_display = ('name', 'hw', 'os')
    search_fields = ('name', 'hw__model', 'os__name')

@admin.register(PermissionType)
class PermissionTypeAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']
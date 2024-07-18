from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User, Department, ATM, OS, PermissionType, UserPermission, \
    Basis, Service, AT, DataBase, Frontend, Backend, Hardware, Host
from import_export.admin import ImportExportModelAdmin
from .forms import UserPermissionsForm


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
class UserPermissionAdmin(ImportExportModelAdmin):
    form = UserPermissionsForm
    list_display = ('id', 'get_object_display', 'get_subject_display', 'permission', 'basis_given_by', 'given_date',
                    'basis', 'expire_date')
    search_fields = ('object_id', 'subject_id')
    list_filter = ('permission', 'basis_given_by', 'given_date', 'expire_date')

    def get_object_display(self, obj):
        try:
            object_instance = obj.object_content_type.get_object_for_this_type(id=obj.object_id)
            if isinstance(object_instance, User):
                return f"{object_instance.first_name} {object_instance.last_name}"
            elif hasattr(object_instance, 'name'):
                return object_instance.name
            return str(object_instance)
        except Exception as e:
            return str(e)
    get_object_display.short_description = 'Object'

    def get_subject_display(self, obj):
        try:
            subject_instance = obj.subject_content_type.get_object_for_this_type(id=obj.subject_id)
            if isinstance(subject_instance, User):
                return f"{subject_instance.first_name} {subject_instance.last_name}"
            elif hasattr(subject_instance, 'name'):
                return subject_instance.name
            return str(subject_instance)
        except Exception as e:
            return str(e)
    get_subject_display.short_description = 'Subject'


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
from rest_framework import serializers
from .models import Department, User, OS, Hardware, Basis, UserPermission, \
    ATM, PermissionType, Service, Host, DataBase, Frontend, Backend, AT


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    """
    *** Agar bo'lim ya'ni Department'ni o'zgartirish kerak bo'lsa pastdagi ishlatiladi.
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'department', 'role', 'is_admin']


class OSSerializer(serializers.ModelSerializer):

    class Meta:
        model = OS
        fields = ['id', 'name', 'comment']


class HardwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = '__all__'

# class HardwareSerializer(serializers.ModelSerializer):
#     responsible_employee = UserSerializer(read_only=True)
#     responsible_department = DepartmentSerializer(read_only=True)
#     """In hardware I removed os, because it unnecessary"""
#     # os_id = serializers.PrimaryKeyRelatedField(
#     #     queryset=OS.objects.all(),
#     #     allow_null=True,
#     #     write_only=True,
#     #     source='os'
#     # )
#     # os = OSSerializer(read_only=True)
#
#     class Meta:
#         model = Hardware
#         fields = ['id', 'inventor_number', 'serial_number', 'type', 'status',
#                   'model', 'manager', 'manager_ip',
#                   'responsible_employee', 'responsible_department']


class HostSerializer(serializers.ModelSerializer):
    os = OSSerializer(read_only=True)
    hardware = HardwareSerializer(read_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'hardware', 'os']


class ATMSerializer(serializers.ModelSerializer):
    os_id = serializers.PrimaryKeyRelatedField(
        queryset=OS.objects.all(),
        allow_null=True,
        write_only=True,
        source='os'
    )
    os = OSSerializer(read_only=True)

    class Meta:
        model = ATM
        fields = ['id', 'location', 'model', 'os', 'os_id', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # os_representation = representation.pop('os_id', None)
        if instance.os:
            representation['os'] = OSSerializer(instance.os).data
        return representation


class PermissionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionType
        fields = ['id', 'name']


"""
Bu qism ishlamayapti sababi ComputerLaptop model o'chirildi
"""
# class ComputerLaptopSerializer(serializers.ModelSerializer):
#     os_id = serializers.PrimaryKeyRelatedField(
#         queryset=OS.objects.all(),
#         write_only=True,
#         allow_null=True,
#         source='os',
#     )
#     responsible_employee = UserSerializer(read_only=True)
#     os = OSSerializer(read_only=True)
#
#     class Meta:
#         model = ComputerLaptop
#         fields = ['id', 'device_name', 'netbios_name', 'mac_address', 'ip_address', 'os', 'os_id',
#                   'specifications', 'responsible_employee', 'responsible_employee_id']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if instance.os:
#             representation['os'] = OSSerializer(instance.os).data
#         return representation


class BasisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basis
        fields = ['id', 'title', 'reg_number', 'basis_file']


class UserPermissionSerializer(serializers.ModelSerializer):
    # subject = UserSerializer(read_only=True)
    # object = HardwareSerializer(read_only=True)
    permission = PermissionTypeSerializer(read_only=True)
    basis = BasisSerializer(read_only=True)
    # subject_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='subject'
    # )
    # object_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Hardware.objects.all(),
    #     write_only=True,
    #     source='object'
    # )
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=PermissionType.objects.all(),
        write_only=True,
        source='permission'
    )
    basis_id = serializers.PrimaryKeyRelatedField(
        queryset=Basis.objects.all(),
        write_only=True,
        source='basis'
    )

    class Meta:
        model = UserPermission
        fields = ['subject_id', 'subject', 'object_id', 'object', 'permission', 'permission_id',
                  'basis_given_by', 'basis', 'basis_id', 'given_date', 'expire_date']

    def create(self, validated_data):
        return UserPermission.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['subject'] = UserSerializer(instance.user).data
        response['object'] = HardwareSerializer(instance.device).data
        response['permission'] = PermissionTypeSerializer(instance.permission).data
        response['basis'] = BasisSerializer(instance.basis).data
        return response


class ServiceSerializer(serializers.ModelSerializer):
    responsible_employee = UserSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'version', 'service_type', 'status']


class FrontendSerializer(serializers.ModelSerializer):
    host = HostSerializer(many=True)
    soft = ServiceSerializer(many=True)

    class Meta:
        model = Frontend
        fields = ['id', 'name', 'ip_address', 'host', 'soft']


class BackendSerializer(serializers.ModelSerializer):
    host = HostSerializer(read_only=True)
    soft = ServiceSerializer(read_only=True)

    class Meta:
        model = Backend
        fields = ['id', 'name', 'ip_address', 'host', 'soft']


class DataBaseSerializer(serializers.ModelSerializer):
    host = HostSerializer(read_only=True)
    soft = ServiceSerializer(read_only=True)

    class Meta:
        model = DataBase
        fields = ['id', 'name', 'db_model', 'ip_address', 'host', 'soft']


class ATSerializer(serializers.ModelSerializer):
    database = DataBaseSerializer(many=True)
    backend = BackendSerializer(many=True)
    frontend = FrontendSerializer(many=True)
    responsible_employee = UserSerializer(many=True)

    class Meta:
        model = AT
        fields = ['id', 'name', 'database', 'backend', 'frontend', 'comment']

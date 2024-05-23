from rest_framework import serializers
from .models import Department, User, OS, ComputerLaptop, Basis, UserPermission, Server, \
    ATM, PermissionType, Socket, AppService


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    """
    *** Agar bo'lim ya'ni Departmentga ham o'zgartirish kerak bo'lsa pastdagi ishlatiladi. 👍
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'department', 'role']


class OSSerializer(serializers.ModelSerializer):

    class Meta:
        model = OS
        fields = ['id', 'name', 'version', 'comment']


class ServerSerializer(serializers.ModelSerializer):
    responsible_employee = UserSerializer(read_only=True)
    os_id = serializers.PrimaryKeyRelatedField(
        queryset=OS.objects.all(),
        allow_null=True,
        write_only=True,
        source='os'
    )
    os = OSSerializer(read_only=True)
    responsible_department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Server
        fields = ['id', 'server_name', 'ip_address', 'server_role',
                  'responsible_employee', 'os', 'os_id', 'responsible_department']


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


class ComputerLaptopSerializer(serializers.ModelSerializer):
    os_id = serializers.PrimaryKeyRelatedField(
        queryset=OS.objects.all(),
        write_only=True,
        allow_null=True,
        source='os',
    )
    responsible_employee = UserSerializer(read_only=True)
    os = OSSerializer(read_only=True)

    class Meta:
        model = ComputerLaptop
        fields = ['id', 'device_name', 'netbios_name', 'mac_address', 'ip_address', 'os', 'os_id',
                  'specifications', 'responsible_employee', 'responsible_employee_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.os:
            representation['os'] = OSSerializer(instance.os).data
        return representation


class BasisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basis
        fields = ['id', 'title', 'reg_number', 'basis_file', 'given_by']


class UserPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    device = ComputerLaptopSerializer(read_only=True)
    permission = PermissionTypeSerializer(read_only=True)
    basis = BasisSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=ComputerLaptop.objects.all(),
        write_only=True,
        source='device'
    )
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
        fields = ['user', 'user_id', 'device', 'device_id', 'permission', 'permission_id', 'basis', 'basis_id']

    def create(self, validated_data):
        return UserPermission.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['device'] = ComputerLaptopSerializer(instance.device).data
        response['permission'] = PermissionTypeSerializer(instance.permission).data
        response['basis'] = BasisSerializer(instance.basis).data
        return response


class SocketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Socket
        fields = ['port', 'protocol']


class AppServiceSerializer(serializers.ModelSerializer):
    network_sockets = SocketSerializer(many=True, read_only=True)
    responsible_employee = UserSerializer(read_only=True)

    class Meta:
        model = AppService
        fields = ['name', 'version', 'service_type', 'network_sockets', 'responsible_employee']

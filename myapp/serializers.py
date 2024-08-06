from abc import ABC

from rest_framework import serializers
from .models import Department, User, OS, Hardware, Basis, UserPermission, \
    ATM, PermissionType, Service, Host, DataBase, Frontend, Backend, AT, Subnet, IPAddress
from django.contrib.contenttypes.models import ContentType


class SubnetSerializer(serializers.ModelSerializer):
    total_ips = serializers.IntegerField(read_only=True)
    ip_list = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )

    class Meta:
        model = Subnet
        fields = ['id', 'address', 'subnet_mask', 'total_ips', 'ip_list']

    def get_total_ips(self, obj):
        return obj.total_ips()

    def get_ip_list(self, obj):
        return obj.ip_list()


class SubnetSerializerForCall(serializers.ModelSerializer):

    class Meta:
        model = Subnet
        fields = ['id', 'address', 'subnet_mask']


class IPAddressSerializer(serializers.ModelSerializer):
    # subnet = serializers.PrimaryKeyRelatedField(queryset=Subnet.objects.all())
    subnet = SubnetSerializer(read_only=True)

    class Meta:
        model = IPAddress
        fields = ['id', 'address', 'subnet']


class IPAddressSerializerForCall(serializers.ModelSerializer):
    subnet = SubnetSerializerForCall(read_only=True)

    class Meta:
        model = IPAddress
        fields = ['id', 'address', 'subnet']


class AddIPToSubnetSerializer(serializers.Serializer):
    ip_address = serializers.CharField()

    def create(self, validated_data):
        ip = validated_data.get('ip_address')
        new_ip = Host.add_ip_to_subnet(ip)
        if new_ip:
            return new_ip
        raise serializers.ValidationError("No matching subnet found for this IP")


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only=True)
    department = DepartmentSerializer()
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


class HostSerializer(serializers.ModelSerializer):
    os = OSSerializer(read_only=True)
    hardware = HardwareSerializer(read_only=True)
    ips = IPAddressSerializerForCall(many=True, read_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'hardware', 'os', 'ips']


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


class BasisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basis
        fields = ['id', 'title', 'reg_number', 'basis_file']


class UserPermissionSerializer(serializers.ModelSerializer):
    object_content_type = serializers.SlugRelatedField(queryset=ContentType.objects.all(), slug_field='model')
    subject_content_type = serializers.SlugRelatedField(queryset=ContentType.objects.all(), slug_field='model')

    object = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    permission = PermissionTypeSerializer(read_only=True)
    basis = BasisSerializer(read_only=True)
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
    # basis_given_by = serializers

    class Meta:
        model = UserPermission
        fields = '__all__'

    def get_object(self, instance):
        object_instance = instance.object_content_type.model_class().objects.get(id=instance.object_id)
        if isinstance(object_instance, User):
            return f"{object_instance.first_name} {object_instance.last_name}"
        return object_instance.name

    def get_subject(self, instance):
        subject_instance = instance.subject_content_type.model_class().objects.get(id=instance.subject_id)
        if isinstance(subject_instance, User):
            return f"{subject_instance.first_name} {subject_instance.last_name}"
        return subject_instance.name

    def create(self, validated_data):
        return UserPermission.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['object'] = self.get_object(instance)
        response['subject'] = self.get_subject(instance)

        response['permission'] = PermissionTypeSerializer(instance.permission).data
        response['basis'] = BasisSerializer(instance.basis).data
        del response['object_id']
        del response['subject_id']
        return response


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['id', 'name', 'version', 'service_type', 'status']


class FrontendSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    soft = ServiceSerializer()

    class Meta:
        model = Frontend
        fields = ['id', 'name', 'ip_address', 'host', 'soft']


class BackendSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    soft = ServiceSerializer()

    class Meta:
        model = Backend
        fields = ['id', 'name', 'ip_address', 'host', 'soft']


class DataBaseSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    soft = ServiceSerializer()

    class Meta:
        model = DataBase
        fields = ['id', 'name', 'db_model', 'ip_address', 'host', 'soft']


class ATSerializer(serializers.ModelSerializer):
    database = DataBaseSerializer()
    backend = BackendSerializer()
    frontend = FrontendSerializer()

    class Meta:
        model = AT
        fields = ['id', 'name', 'database', 'backend', 'frontend', 'comment']

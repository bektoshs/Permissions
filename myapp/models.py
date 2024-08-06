from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import uuid
import ipaddress


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_name + " " + self.last_name)
    
    
class OS(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)


class Hardware(models.Model):
    inventor_number = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    manager_ip = models.CharField(max_length=100)
    responsible_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    responsible_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.model)


class Subnet(models.Model):
    address = models.CharField(max_length=255)
    subnet_mask = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        network = ipaddress.ip_network(self.address, strict=False)
        self.subnet_mask = str(network.netmask)
        super().save(*args, **kwargs)

    def total_ips(self):
        network = ipaddress.ip_network(self.address, strict=False)
        return network.network_address

    def ip_list(self):
        network = ipaddress.ip_network(self.address, strict=False)
        return [str(ip) for ip in network.hosts()]

    @staticmethod
    def contains_ip(subnet, ip):
        network = ipaddress.ip_network(subnet.address, strict=False)
        return ipaddress.ip_address(ip) in network


class IPAddress(models.Model):
    address = models.CharField(max_length=255)
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE, related_name='ips')

    def __str__(self):
        return self.address


class Host(models.Model):
    name = models.CharField(max_length=255)
    hw = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="host_hardware")
    os = models.ForeignKey(OS, on_delete=models.CASCADE, related_name="host_os")
    ips = models.ManyToManyField(IPAddress)

    def __str__(self):
        return str(self.name)

    @classmethod
    def add_ip_to_subnet(cls, ip):
        subnets = Subnet.objects.all()
        for subnet in subnets:
            if subnet.contains_ip(subnet, ip):
                ip_address = IPAddress(address=ip, subnet=subnet)
                ip_address.save()
                return ip_address
        return None
    

class ATM(models.Model):
    location = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os = models.ForeignKey(OS, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return str(f'Manzil {self.location} Model: {self.model}')
    

class PermissionType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
    

class UserPermission(models.Model):
    permission = models.ForeignKey(PermissionType, on_delete=models.SET_NULL, null=True, blank=True)
    basis = models.ForeignKey('Basis', on_delete=models.CASCADE)
    basis_given_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="bases_given_by")
    given_date = models.DateTimeField(auto_now_add=True, blank=True)
    expire_date = models.DateTimeField()

    # Object (subject that is giving the permission)
    object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='object_permissions',
                                            default=1)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('object_content_type', 'object_id')

    # Subject (subject that is receiving the permission)
    subject_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='subject_permissions',
                                             default=1)
    subject_id = models.PositiveIntegerField()
    subject = GenericForeignKey('subject_content_type', 'subject_id')

    def __str__(self):
        return f"{self.subject_id}'s permission to {self.object_id}"
    

class Basis(models.Model):
    title = models.CharField(max_length=200)
    reg_number = models.CharField(max_length=100)
    basis_file = models.FileField(upload_to='basis_files/')

    # This give randomly name for title
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = str(uuid.uuid4())
        super(Basis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    service_type = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} {self.version}"


class Frontend(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="front_host")
    soft = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="front_soft_service")

    def __str__(self):
        return f"{self.name} - {self.ip_address}"


class Backend(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="back_host")
    soft = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="back_service_soft")

    def __str__(self):
        return f"{self.name} - {self.ip_address}"


class DataBase(models.Model):
    name = models.CharField(max_length=100)
    db_model = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="database_host")
    soft = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="database_soft_service")

    def __str__(self):
        return f"{self.name} model: {self.db_model}"


class AT(models.Model):
    name = models.CharField(max_length=255)
    database = models.ForeignKey(DataBase, on_delete=models.CASCADE, related_name="at_database")
    backend = models.ForeignKey(Backend, on_delete=models.CASCADE, related_name="at_back")
    frontend = models.ForeignKey(Frontend, on_delete=models.CASCADE, related_name="at_frontend")
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name
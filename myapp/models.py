from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


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
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)
    
    
class Server(models.Model):
    server_name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=100)
    server_role = models.CharField(max_length=255)
    os = models.ForeignKey(OS, on_delete=models.CASCADE)
    responsible_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    responsible_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.server_name)
    

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


class ComputerLaptop(models.Model):
    device_name = models.CharField(max_length=255)
    netbios_name = models.CharField(max_length=255, null=True, blank=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    os = models.ForeignKey(OS, on_delete=models.SET_NULL, null=True)
    specifications = models.TextField(null=True)
    responsible_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.device_name)
    

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(ComputerLaptop, on_delete=models.SET_NULL, null=True, blank=True)
    permission = models.ForeignKey(PermissionType, on_delete=models.SET_NULL, null=True, blank=True)
    basis = models.ForeignKey('Basis', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s permission"
    

class Basis(models.Model):
    title = models.CharField(max_length=255, blank=True)
    reg_number = models.CharField(max_length=100)
    basis_file = models.FileField(upload_to='basis_files/')
    given_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_bases")

    # This give randomly name for title
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = str(uuid.uuid4())
        super(Basis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
    

class Socket(models.Model):
    port = models.IntegerField()
    protocol = models.CharField(max_length=20)

    def __str__(self):
        return f"({self.protocol}:{self.port})"


class AppService(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    service_type = models.CharField(max_length=200)
    network_sockets = models.ManyToManyField(Socket, related_name='connected_services')
    responsible_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_employee')
    
    def __str__(self):
        return f"{self.name} {self.version} - {self.network_sockets}"
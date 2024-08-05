from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity
from django.http import Http404
from .models import Department, OS, User, Hardware, Basis, \
    ATM, PermissionType, UserPermission, Service, Backend, DataBase, Frontend, AT, Host, \
    Subnet, IPAddress
from .serializers import OSSerializer, HardwareSerializer, ATMSerializer, \
    BasisSerializer, DepartmentSerializer, UserSerializer, PermissionTypeSerializer, \
    UserPermissionSerializer, ServiceSerializer, BackendSerializer, DataBaseSerializer, \
    FrontendSerializer, ATSerializer, HostSerializer, SubnetSerializer, IPAddressSerializer, AddIpToSubnetSerializer
from .permissions import IsSuperPermission, IsReadOnlyPermission


class SubnetListCreateAPIView(APIView):
    def get(self, request):
        subnets = Subnet.objects.all()
        serializer = SubnetSerializer(subnets, many=True)
        return Response(serializer.data)


class IPAddressListCreateAPIView(APIView):
    def get(self, request):
        ip_addresses = IPAddress.objects.all()
        serializer = IPAddressSerializer(ip_addresses, many=True)
        return Response(serializer.data)


class HostListCreateAPIView(APIView):
    def get(self, request):
        host = Host.objects.all()
        serializer = HostSerializer(host, many=True)
        return Response(serializer.data)


class DepartmentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Department.objects.all()
        serializer = DepartmentSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response("Please add value for search")
        departments = Department.objects.annotate(
            search=SearchVector('name')
        ).filter(search=search)
        departments_data = DepartmentSerializer(departments, many=True).data
        return Response({"Result": departments_data})


class DepartmentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchByName(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        first_name = request.query_params.get('first_name', '')
        search_type = request.query_params.get('search_type', 'partial')
        print(f"Received first_name: {first_name}, search_type: {search_type}")

        if not first_name:
            return Response([])
        if search_type == 'exact':
            users = User.objects.filter(first_name__iexact=first_name)
        else:
            users = User.objects.annotate(
                similarity=TrigramSimilarity('first_name', first_name)
            ).filter(similarity__gt=0.1).order_by('-similarity')
        print(f"User found: {users.count()}")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = self.get_object(pk)
        if isinstance(user, Response):
            return user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    """
    Qachonki foydalanuvchini ma'lumotlarinni o'zgartirmoqchi bo'linsa quyidagilar majburiy 
    {
        "first_name":"Bektosh", 
        "last_name": "Salimov",
         "role": "Admin"
    }
    """

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HardwareList(APIView):

    def get(self, request):
        hardware = Hardware.objects.all()
        serializer = HardwareSerializer(hardware, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HardwareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class HardwareSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response("Iltimos search'ga qiymat bering")

        hardware = Hardware.objects.annotate(
            search=SearchVector('inventor_number', 'serial_number', 'type', 'status', 'model',
                                'manager', 'manager_ip',
                                'responsible_employee__first_name', 'responsible_employee__last_name',
                                'responsible_department__name')
        ).filter(search=search)
        hardware_data = HardwareSerializer(hardware, many=True).data
        return Response({'Result': hardware_data})


class HardwareDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Hardware.objects.get(pk=pk)
        except Hardware.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        hardware = self.get_object(pk)
        if isinstance(hardware, Response):
            return hardware
        serializer = HardwareSerializer(hardware)
        return Response(serializer.data)

    def put(self, request, pk):
        hardware = self.get_object(pk)
        if isinstance(hardware, Response):
            return hardware
        serializer = HardwareSerializer(hardware, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hardware = self.get_object(pk)
        if isinstance(hardware, Response):
            return hardware
        hardware.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OSList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        os = OS.objects.all()
        serializer = OSSerializer(os, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OSSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response("Please add value for search")
        oses = OS.objects.annotate(
            search=SearchVector('name', 'version', 'comment')
        ).filter(search=search)
        oses_data = OSSerializer(oses, many=True).data
        return Response({"Result": oses_data})


class OSDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OS.objects.get(pk=pk)
        except OS.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        os = self.get_object(pk)
        serializer = OSSerializer(os)
        return Response(serializer.data)

    def put(self, request, pk):
        os = self.get_object(pk)
        serializer = OSSerializer(os, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        os = self.get_object(pk)
        os.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ATMList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        atm = ATM.objects.all()
        serializer = ATMSerializer(atm, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ATMSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ATMSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response("Please give value to search like http://127.0.0.1:8000/atms/search/?search=Yunusubod")
        atms = ATM.objects.annotate(
            search=SearchVector('location', 'model', 'os__name', 'status')
        ).filter(search=search)
        atms_data = ATMSerializer(atms, many=True).data
        return Response({"Result": atms_data})


class ATMDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ATM.objects.get(pk=pk)
        except ATM.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        atm = self.get_object(pk)
        serializer = ATMSerializer(atm)
        return Response(serializer.data)

    def put(self, request, pk):
        atm = self.get_object(pk)
        serializer = ATMSerializer(atm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        atm = self.get_object(pk)
        if isinstance(atm, Response):
            return atm
        atm.delete()
        return Response({"Status": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


class PermissionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permission = PermissionType.objects.all()
        serializer = PermissionTypeSerializer(permission, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionByName(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '')
        search_type = request.query_params.get('search_type', 'partial')

        if not search:
            return Response("Please add value for search")

        if search_type == 'exact':
            permission = PermissionType.objects.filter(permission_name__iexact=search)
        else:
            permission = PermissionType.objects.annotate(
                similarity=TrigramSimilarity('permission_name', search),
            ).filter(similarity__gt=0.3).order_by('-similarity')

        serializer = PermissionTypeSerializer(permission, many=True)
        return Response(serializer.data)


class PermissionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return PermissionType.objects.get(pk=pk)
        except PermissionType.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        permission = self.get_object(pk)
        serializer = PermissionTypeSerializer(permission)
        return Response(serializer.data)

    def put(self, request, pk):
        permission = self.get_object(pk)
        serializer = PermissionTypeSerializer(permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission = self.get_object(pk)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPermissionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = UserPermission.objects.all()
        serializer = UserPermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     serializer = UserPermissionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasisList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        basis = Basis.objects.all()
        serializer = BasisSerializer(basis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BasisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasisSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')

        if not search:
            return Response('Please add value for search')

        basis = Basis.objects.annotate(
            search=SearchVector('title', 'reg_number', 'basis_file')
        ).filter(search=search)

        basis_data = BasisSerializer(basis, many=True).data
        return Response({"Result": basis_data})


class BasisDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Basis.objects.get(pk=pk)
        except Basis.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        basis = self.get_object(pk)
        serializer = BasisSerializer(basis)
        return Response(serializer.data)

    def put(self, request, pk):
        basis = self.get_object(pk)
        serializer = BasisSerializer(basis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        basis = self.get_object(pk)
        basis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
==(ComputerLaptop Model o'chirildi)==

class ComputersLaptopsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        computer_laptop = ComputerLaptop.objects.all()
        serializer = ComputerLaptopSerializer(computer_laptop, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ComputerLaptopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ComputerLaptopsSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response('Please enter value for search')
        
        computers = ComputerLaptop.objects.annotate(
            search=SearchVector('device_name', 'mac_address', 'ip_address', 'specifications', 'os__name')
        ).filter(search=search)
        computers_data = ComputerLaptopSerializer(computers, many=True).data
        return Response({'Result': computers_data})


class ComputerLaptopsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ComputerLaptop.objects.get(pk=pk)
        except ComputerLaptop.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        computer = self.get_object(pk)
        serializer = ComputerLaptopSerializer(computer)
        return Response(serializer.data)
    
    def put(self, request, pk):
        computer = self.get_object(pk)
        serializer = ComputerLaptopSerializer(computer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        computer = self.get_object(pk)
        computer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class ServiceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        if not search:
            return Response('Please add value for search')
        services = Service.objects.annotate(
            search=SearchVector('name', 'version', 'service_type', 'status')
        ).filter(search=search)
        services_data = ServiceSerializer(services, many=True).data
        return Response({"Result": services_data})


class ServiceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GlobalSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '')

        if not search:
            return Response({'message': 'No search term provided'}, status=400)

        users = User.objects.annotate(
            search=SearchVector('first_name', 'last_name', 'department__name'),
        ).filter(search=search)
        departments = Department.objects.annotate(
            search=SearchVector('name'),
        ).filter(search=search)
        permission = PermissionType.objects.annotate(
            search=SearchVector('name'),
        ).filter(search=search)

        """Server chasti ishlamayapti, sababi server model'i o'chirildi"""
        # servers = Server.objects.annotate(
        #     search=SearchVector('server_name', 'ip_address', 'os__name',
        #                         'responsible_employee__first_name',
        #                         'responsible_employee__last_name',
        #                         'responsible_department__name'),
        # ).filter(search=search)
        atms = ATM.objects.annotate(
            search=SearchVector('location', 'model',
                                'os__name', 'os__version', 'status'),
        ).filter(search=search)
        oses = OS.objects.annotate(
            search=SearchVector('name', 'version', 'comment')
        ).filter(search=search)
        """Computer chasti ishlamayapti, sababi computer model'i o'chirildi"""
        # computers = ComputerLaptop.objects.annotate(
        #     search=SearchVector('device_name', 'netbios_name',
        #                         'mac_address', 'ip_address', 'os__name', 'os__version',
        #                         'specifications', 'responsible_employee__first_name',
        #                         'responsible_employee__last_name', 'responsible_employee__department',
        #                         'responsible_employee__department__name')
        # ).filter(search=search)
        basis = Basis.objects.annotate(
            search=SearchVector('title', 'given_by', 'reg_number')
        ).filter(search=search)
        user_permission = UserPermission.objects.annotate(
            search=SearchVector('user__first_name', 'user__last_name',
                                'device', 'device__device_name',
                                'permission__name',
                                'basis__title', 'basis__reg_number')
        ).filter(search=search)
        service = Service.objects.annotate(
            search=SearchVector('name', 'service_type', 'version'
                                                        'responsible_employee__first_name',
                                'responsible_employee__last_name')
        ).filter(search=search)

        user_data = UserSerializer(users, many=True).data
        department_data = DepartmentSerializer(departments, many=True).data
        permission_data = PermissionTypeSerializer(permission, many=True).data
        atm_data = ATMSerializer(atms, many=True).data
        os_data = OSSerializer(oses, many=True).data
        basis_data = BasisSerializer(basis, many=True).data
        user_permission_data = UserPermissionSerializer(user_permission, many=True).data
        service_data = ServiceSerializer(service, many=True).data
        return Response(
            {
                'users': user_data,
                'departments': department_data,
                'permission': permission_data,
                'atms': atm_data,
                'oses': os_data,
                'bases': basis_data,
                'user_permission': user_permission_data,
                'service': service_data
            }
        )

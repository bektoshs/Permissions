from django.urls import path

from .views import DepartmentList, DepartmentDetail, DepartmentSearchView, \
                    UserList, UserDetail, UserSearchByName, \
                    ServerList, ServerDetail, ServerSearchView, \
                    OSList, OSDetail, OSSearchView, \
                    ATMList, ATMDetail, ATMSearchView, \
                    PermissionList, PermissionByName, PermissionDetail, UserPermissionList, BasisList,\
                    BasisDetail, BasisSearchView, \
                    ComputersLaptopsList, ComputerLaptopsDetail, ComputerLaptopsSearchView, \
                    GlobalSearch, \
                    SocketList, SocketDetail, SocketSearchView, \
                    AppServiceList, AppServiceDetail, AppServiceSearchView

urlpatterns = [
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/search/', DepartmentSearchView.as_view(), name='department-search'),
    path('department/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),

    path('users/', UserList.as_view(), name='users-list'),
    path('user/name/', UserSearchByName.as_view(), name='user-by-firstname'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('servers/', ServerList.as_view(), name='servers-list'),
    path('servers/search/', ServerSearchView.as_view(), name='servers-search'),
    path('server/<int:pk>/', ServerDetail.as_view(), name='server-detail'),

    path('oses/', OSList.as_view(), name='oses-list'),
    path('oses/search/', OSSearchView.as_view(), name='oses-search'),
    path('os/<int:pk>/', OSDetail.as_view(), name='os-detail'),

    path('atms/', ATMList.as_view(), name='atms-list'),
    path('atms/search/', ATMSearchView.as_view(), name='atms-search'),
    path('atm/<int:pk>/', ATMDetail.as_view(), name='atm-detail'),

    path('permissions/', PermissionList.as_view(), name='permissions-list'),
    path('permissions/search/', PermissionByName.as_view(), name='permission-search'),
    path('permission/<int:pk>/', PermissionDetail.as_view(), name='permission-detail'),

    path('userpermissions/', UserPermissionList.as_view(), name='userpermission-list'),

    path('bases/', BasisList.as_view(), name='bases-list'),
    path('basis/search/', BasisSearchView.as_view(), name='basis-search'),
    path('basis/<int:pk>/', BasisDetail.as_view(), name='basis-detail'),
    
    path('sockets/', SocketList.as_view(), name='sockets-list'),
    path('sockets/search/', SocketSearchView.as_view(), name='sockets-search'),
    path('socket/<int:pk>/', SocketDetail.as_view(), name='socket-detail'),

    path('apps/', AppServiceList.as_view(), name='app-service-list'),
    path('apps/search/', AppServiceSearchView.as_view(), name='app-service-search'),
    path('app/<int:pk>/', AppServiceDetail.as_view(), name='app-service-detail'),

    path('computers/', ComputersLaptopsList.as_view(), name='computers-laptops-list'),
    path('computers/search/', ComputerLaptopsSearchView.as_view(), name='computers-search'),
    path('computer/<int:pk>/', ComputerLaptopsDetail.as_view(), name='computer-laptop-detail'),

    path('search/', GlobalSearch.as_view(), name='global-search'),
]
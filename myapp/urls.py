from django.urls import path

from .views import DepartmentList, DepartmentDetail, DepartmentSearchView, \
                    UserList, UserDetail, UserSearchByName, \
                    OSList, OSDetail, OSSearchView, \
                    HardwareList, HardwareSearchView, HardwareDetail, \
                    ATMList, ATMDetail, ATMSearchView, \
                    PermissionList, PermissionByName, PermissionDetail, UserPermissionList, BasisList,\
                    BasisDetail, BasisSearchView, \
                    GlobalSearch, \
                    ServiceList, ServiceDetail, ServiceSearchView

urlpatterns = [
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/search/', DepartmentSearchView.as_view(), name='department-search'),
    path('department/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),

    path('users/', UserList.as_view(), name='users-list'),
    path('user/name/', UserSearchByName.as_view(), name='user-by-firstname'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('hardwares/', HardwareList.as_view(), name='hardwares-list'),
    path('hardwares/search/', HardwareSearchView.as_view(), name='hardwares-search'),
    path('hardware/<int:pk>/', HardwareDetail.as_view(), name='hardware-detail'),

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

    path('services/', ServiceList.as_view(), name='app-service-list'),
    path('services/search/', ServiceSearchView.as_view(), name='app-service-search'),
    path('service/<int:pk>/', ServiceDetail.as_view(), name='app-service-detail'),

    path('user-permissions/', UserPermissionList.as_view(), name='users-permissions'),

    path('search/', GlobalSearch.as_view(), name='global-search'),
]
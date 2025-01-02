from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (FrontPageView, register,
                    login_view, logout_view, set_user_as_admin,
                    remove_user_as_admin,delete_user,admin_main, user_profile,
                    user_home, ServiceList, ServiceDetail, admin_service, admin_pet,
                    AdminServiceDetail, CreateService, UpdateService, DeleteService,
                    AdminPetDetail,CreatePet,UpdatePet,DeletePet,admin_owner,AdminOwnerDetail,CreateOwner,UpdateOwner,DeleteOwner,
                    admin_groomer, CreateGroomer, UpdateGroomer, DeleteGroomer, AdminGroomerDetail, 
                    admin_Appointment, CreateAppointment, UpdateAppointment, DeleteAppointment, appointment_Status, reschedule_appointment)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('admin-main/', admin_main, name='admin_main'),
    path('', FrontPageView.as_view(), name='FrontPage'),

    # For admin interface
    path('set-admin/<int:user_id>/', set_user_as_admin, name='set_admin'),  # set new admin
    path('remove-admin/<int:user_id>/', remove_user_as_admin, name='remove_admin'),  # remove-admin URL
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),     # delete admin/user
    path('update_profile/<int:user_id>/', views.update_user_profile, name='update_user_profile'),

   # Admin Html
    path('admin_service/', admin_service, name='admin_service'),
    path('admin_service/<int:pk>/', AdminServiceDetail.as_view(), name='admin_detail'),
    path('admin_service/create/', CreateService.as_view(), name='admin_CreateService'),
    path('admin_service/<int:pk>/edit/', UpdateService.as_view(), name='admin_update'),
    path('admin_service/<int:pk>/delete/', DeleteService.as_view(), name='admin_delete'),

    # Pet Html
    path('admin_pet/', admin_pet, name='admin_pet'),
    path('admin_pet/<int:pk>/', AdminPetDetail.as_view(), name='admin_Petdetail'),
    path('admin_pet/create/', CreatePet.as_view(), name='admin_CreatePet'),
    path('admin_pet/<int:pk>/edit/', UpdatePet.as_view(), name='admin_updatePet'),
    path('admin_pet/<int:pk>/delete/', DeletePet.as_view(), name='admin_Petdelete'),

     # Owner Html
    path('admin_owner/', admin_owner, name='admin_owner'),
    path('admin_owner/<int:pk>/', AdminOwnerDetail.as_view(), name='admin_Ownerdetail'),
    path('admin_owner/create/', CreateOwner.as_view(), name='admin_CreateOwner'),
    path('admin_owner/<int:pk>/edit/', UpdateOwner.as_view(), name='admin_updateOwner'),
    path('admin_owner/<int:pk>/delete/', DeleteOwner.as_view(), name='admin_deleteOwner'),

    # Groomer Html
    path('admin_groomer/', admin_groomer, name='admin_groomer'),
    path('admin_groomer/<int:pk>/', AdminGroomerDetail.as_view(), name='admin_Groomerdetail'),
    path('admin_groomer/create/', CreateGroomer.as_view(), name='admin_CreateGroomer'),
    path('admin_groomer/<int:pk>/edit/', UpdateGroomer.as_view(), name='admin_updateGroomer'),
    path('admin_groomer/<int:pk>/delete/', DeleteGroomer.as_view(), name='admin_deleteGroomer'),

    # Appointment Html
    path('admin_appointment/', admin_Appointment, name='admin_Appointment'),
    path('admin_appointment/create/', CreateAppointment.as_view(), name='admin_CreateAppointment'),
    path('admin_appointment/<int:pk>/edit/', UpdateAppointment.as_view(), name='admin_updateAppointment'),
    path('admin_appointment/<int:pk>/delete/', DeleteAppointment.as_view(), name='admin_Appointmentdelete'),
    path('admin_appointment/<int:pk>/review/', appointment_Status, name='appointment'),
    path('admin_appointment/<int:pk>/reschedule/', reschedule_appointment, name='reschedule_appointment'),

    # User Html
    path('user_home/', user_home, name='user_home'),
    path('service/', ServiceList.as_view(), name='service'),
    path('user_home/<int:pk>', ServiceDetail.as_view(), name='detail'),

    
    path('profile/', user_profile, name='user_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
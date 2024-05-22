from django.urls import path
from . import views





urlpatterns = [
    path('',views.signin,name='signin'),
    path('home/',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('edit/',views.home,name='edit'),
    path('logout/',views.logout, name='logout'),
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('updateuser/<int:user_id>/', views.updateuser, name='updateuser'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('createuser/', views.createuser, name='createuser')
]

from django.urls import path, include
from sleep_tracker import views
urlpatterns = [
    path('', views.index, name='index'),
    path('check/password', views.check_password, name='check_password'),
    path('register/user', views.register, name='register'),
    path('log/out', views.logout_lg, name='logout'),
    path('diag/nose', views.diagnose, name='diagnose'),
    path('delete/user', views.delete_user, name='delete_user'),
    path('request/report', views.health_report, name='health_report'),
    path('checkusername', views.check_username, name='check_username'),

]

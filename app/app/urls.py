from django.contrib import admin
from django.urls import path
from user import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup', views.sign_up,name='signup'),
    path('login', views.login,name='login'),
    path('profile', views.profile,name='profile'),
    path('changepassword', views.changePassword,name='changepassword'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('forgotPassword', views.forgotPassword,name='forgotPassword'),
    path('resetPassword/<str:hashed_email>', views.resetPassword,name='resetPassword'),
    path('logout', views.logout_view,name='logout'),
    path('', lambda request: redirect('dashboard', permanent=True)),  # Default redirect
]

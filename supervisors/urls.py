from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('signin/', views.signin, name='signin'),    
     path('operations/', views.operations, name='operations'),
     path('sales-reps/', views.sales_reps, name='sales_reps'),
     path('add_branch/', views.add_branch, name='add_branch'),
     path('reports/', views.reports, name='reports'),
     path('logout/', views.logout_view, name='logout'),
   
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

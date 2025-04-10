from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('landing', views.landing, name='landing'),    
    path('logout_sales/', views.logout_sales, name='logout_sales'),
    path('auth/', views.auth, name='auth'),
    path('sales/', views.sales, name='sales'),
    path('sales_reports/', views.sales_reports, name='sales_reports'),
   
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

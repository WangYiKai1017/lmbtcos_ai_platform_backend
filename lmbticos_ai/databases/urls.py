from django.urls import path
from . import views

urlpatterns = [
    # 获取数据库实例列表
    path('', views.get_databases, name='get_databases'),
    
    # 获取数据库实例详情
    path('<str:database_id>/', views.get_database_detail, name='get_database_detail'),
]
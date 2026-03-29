from django.urls import path
from . import views

urlpatterns = [
    # 获取模型路由器列表
    path('routers/', views.get_model_routers, name='get_model_routers'),
    
    # 获取模型路由器详情
    path('routers/<str:router_id>/', views.get_model_router_detail, name='get_model_router_detail'),
    
    # 获取模型列表
    path('', views.get_models, name='get_models'),
    
    # 创建模型路由器
    path('routers/', views.create_model_router, name='create_model_router'),
]
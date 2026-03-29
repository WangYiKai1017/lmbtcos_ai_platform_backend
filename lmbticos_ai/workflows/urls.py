from django.urls import path
from . import views

urlpatterns = [
    # 获取工作流列表
    path('', views.get_workflows, name='get_workflows'),
    
    # 获取工作流详情
    path('<str:workflow_id>/', views.get_workflow_detail, name='get_workflow_detail'),
    
    # 创建工作流
    path('', views.create_workflow, name='create_workflow'),
    
    # 添加工作流节点
    path('<str:workflow_id>/nodes/', views.add_workflow_node, name='add_workflow_node'),
    
    # 添加工作流边
    path('<str:workflow_id>/edges/', views.add_workflow_edge, name='add_workflow_edge'),
]
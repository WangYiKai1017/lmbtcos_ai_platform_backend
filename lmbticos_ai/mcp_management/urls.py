from django.urls import path
from . import views

urlpatterns = [
    # 获取MCP工具列表
    path('tools/', views.get_mcp_tools, name='get_mcp_tools'),
    
    # 获取MCP工具详情
    path('tools/<str:tool_id>/', views.get_mcp_tool_detail, name='get_mcp_tool_detail'),
    
    # 创建MCP工具
    path('tools/', views.create_mcp_tool, name='create_mcp_tool'),
]
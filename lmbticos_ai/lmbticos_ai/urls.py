"""
URL configuration for lmbticos_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT认证路由
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 文档管理模块路由
    path('v1/documents/', include('documents.urls')),
    
    # 切片工具模块路由
    path('v1/slice-tool/', include('slice_tool.urls')),
    
    # 模型管理模块路由
    path('v1/models/', include('models_management.urls')),
    
    # 数据管理模块路由
    path('v1/databases/', include('databases.urls')),
    
    # MCP管理模块路由
    path('v1/mcp/', include('mcp_management.urls')),
    
    # 技能管理模块路由
    path('v1/skills/', include('skills_management.urls')),
    
    # 看板页面模块路由
    path('v1/kanban/', include('kanban.urls')),
    
    # 需求拆解页面模块路由
    path('v1/requirements/', include('requirements.urls')),
    
    # 工作流页面模块路由
    path('v1/workflows/', include('workflows.urls')),
    
    # Agent管理模块路由
    path('v1/agents/', include('agents_api.urls')),
]

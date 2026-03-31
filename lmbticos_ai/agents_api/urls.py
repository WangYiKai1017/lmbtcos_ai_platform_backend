"""
Agents API路由配置
"""

from django.urls import path
from .views import (
    AgentListCreateView,
    AgentDetailView,
    AgentStartView,
    AgentStopView,
    AgentStatusView,
    AllAgentsStatusView
)

urlpatterns = [
    # 获取Agent列表和创建Agent
    path('agents/', AgentListCreateView.as_view(), name='agent-list-create'),
    # 获取指定Agent的详情
    path('agents/<str:agent_id>/', AgentDetailView.as_view(), name='agent-detail'),
    # 启动指定Agent
    path('agents/<str:agent_id>/start/', AgentStartView.as_view(), name='agent-start'),
    # 停止指定Agent
    path('agents/<str:agent_id>/stop/', AgentStopView.as_view(), name='agent-stop'),
    # 获取指定Agent的状态
    path('agents/<str:agent_id>/status/', AgentStatusView.as_view(), name='agent-status'),
    # 获取所有Agent的状态
    path('agents/status/', AllAgentsStatusView.as_view(), name='all-agents-status'),
]

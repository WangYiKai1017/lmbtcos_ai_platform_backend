"""
Agents API视图
处理Agent相关的API请求
"""

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from lmbticos_ai.utils import wrap_response
from agents import scheduler, DummyAgent
import json


class AgentListCreateView(APIView):
    """
    获取Agent列表和创建Agent
    """
    
    def get(self, request):
        """
        获取所有Agent的列表
        """
        agents = scheduler.get_all_agents_status()
        return wrap_response(agents, "获取Agent列表成功")
    
    def post(self, request):
        """
        创建一个新的Agent
        """
        try:
            data = request.data
            agent_name = data.get('name', '')
            agent_config = data.get('config', {})
            
            # 创建Agent实例（这里暂时使用DummyAgent，实际应用中可以根据类型创建不同的Agent）
            agent = DummyAgent(name=agent_name, config=agent_config)
            
            # 启动Agent
            if scheduler.start_agent(agent):
                return wrap_response(agent.get_status(), "创建并启动Agent成功", status=status.HTTP_201_CREATED)
            else:
                return wrap_response(None, "创建Agent失败", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return wrap_response(None, f"创建Agent时发生错误: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AgentDetailView(APIView):
    """
    获取指定Agent的详情
    """
    
    def get(self, request, agent_id):
        """
        获取指定Agent的详情
        """
        agent = scheduler.get_agent(agent_id)
        if agent:
            return wrap_response(agent.get_status(), "获取Agent详情成功")
        else:
            return wrap_response(None, "Agent不存在", status=status.HTTP_404_NOT_FOUND)


class AgentStartView(APIView):
    """
    启动指定的Agent
    """
    
    def post(self, request, agent_id):
        """
        启动指定的Agent
        """
        agent = scheduler.get_agent(agent_id)
        if agent:
            if scheduler.start_agent(agent):
                return wrap_response(agent.get_status(), "启动Agent成功")
            else:
                return wrap_response(None, "Agent已经在运行中", status=status.HTTP_400_BAD_REQUEST)
        else:
            return wrap_response(None, "Agent不存在", status=status.HTTP_404_NOT_FOUND)


class AgentStopView(APIView):
    """
    停止指定的Agent
    """
    
    def post(self, request, agent_id):
        """
        停止指定的Agent
        """
        if scheduler.stop_agent(agent_id):
            return wrap_response(None, "停止Agent成功")
        else:
            return wrap_response(None, "Agent不存在或停止失败", status=status.HTTP_404_NOT_FOUND)


class AgentStatusView(APIView):
    """
    获取指定Agent的状态
    """
    
    def get(self, request, agent_id):
        """
        获取指定Agent的状态
        """
        status_info = scheduler.get_agent_status(agent_id)
        if status_info:
            return wrap_response(status_info, "获取Agent状态成功")
        else:
            return wrap_response(None, "Agent不存在", status=status.HTTP_404_NOT_FOUND)


class AllAgentsStatusView(APIView):
    """
    获取所有Agent的状态
    """
    
    def get(self, request):
        """
        获取所有Agent的状态
        """
        all_status = scheduler.get_all_agents_status()
        return wrap_response(all_status, "获取所有Agent状态成功")

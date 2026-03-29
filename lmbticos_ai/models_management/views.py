from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ModelRouter, Model
from .serializers import ModelRouterSerializer, ModelSerializer
from lmbticos_ai.utils.response_wrapper import wrap_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_routers(request):
    """
    获取模型路由器列表
    """
    # TODO: 实现获取模型路由器列表的逻辑
    return wrap_response([], message="获取模型路由器列表成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_router_detail(request, router_id):
    """
    获取模型路由器详情
    """
    # TODO: 实现获取模型路由器详情的逻辑
    return wrap_response({}, message="获取模型路由器详情成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_models(request):
    """
    获取模型列表
    """
    # TODO: 实现获取模型列表的逻辑
    router_id = request.query_params.get('router_id', None)
    type = request.query_params.get('type', None)
    return wrap_response([], message="获取模型列表成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_model_router(request):
    """
    创建模型路由器
    """
    # TODO: 实现创建模型路由器的逻辑
    return wrap_response({}, message="创建模型路由器成功")

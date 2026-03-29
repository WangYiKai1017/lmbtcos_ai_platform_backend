from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from lmbticos_ai.utils.response_wrapper import wrap_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_system_tree(request):
    """
    获取文件系统树
    """
    # TODO: 实现获取文件系统树的逻辑
    parent_id = request.query_params.get('parent_id', None)
    return wrap_response([], message="获取文件系统树成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_folder(request):
    """
    创建文件夹
    """
    # TODO: 实现创建文件夹的逻辑
    return wrap_response({}, message="创建文件夹成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    上传文件
    """
    # TODO: 实现上传文件的逻辑
    return wrap_response({}, message="上传文件成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_detail(request, file_id):
    """
    获取文件详情
    """
    # TODO: 实现获取文件详情的逻辑
    return wrap_response({}, message="获取文件详情成功")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file_or_folder(request, id):
    """
    删除文件/文件夹
    """
    # TODO: 实现删除文件/文件夹的逻辑
    return wrap_response({}, message="删除成功")

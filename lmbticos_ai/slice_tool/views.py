from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SliceFile, SlicePage, SliceResult
from .serializers import SliceFileSerializer, SlicePageSerializer, SliceResultSerializer
from lmbticos_ai.utils.response_wrapper import wrap_response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_slice_file(request):
    """
    上传切片文件
    """
    # TODO: 实现上传切片文件的逻辑
    return wrap_response({}, message="文件上传成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upload_files(request):
    """
    获取上传文件列表
    """
    # TODO: 实现获取上传文件列表的逻辑
    return wrap_response([], message="获取文件列表成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_pages(request, file_id):
    """
    获取文档页面
    """
    # TODO: 实现获取文档页面的逻辑
    return wrap_response([], message="获取文档页面成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_slice_process(request, file_id):
    """
    开始切片处理
    """
    # TODO: 实现开始切片处理的逻辑
    return wrap_response({}, message="切片处理已开始")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_slice_result(request, result_id):
    """
    获取切片结果
    """
    # TODO: 实现获取切片结果的逻辑
    return wrap_response({}, message="获取切片结果成功")

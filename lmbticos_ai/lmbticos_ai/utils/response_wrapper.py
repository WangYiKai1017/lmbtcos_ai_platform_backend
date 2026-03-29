from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


def wrap_response(data, message="操作成功", status=200):
    """
    统一API响应格式
    :param data: 响应数据
    :param message: 响应消息
    :param status: HTTP状态码
    :return: Response对象
    """
    # 处理分页响应
    if isinstance(data, dict) and 'results' in data and 'count' in data:
        return Response({
            "success": True,
            "data": {
                "items": data['results'],
                "total": data['count'],
                "page": (data.get('offset', 0) // data.get('limit', 10)) + 1,
                "limit": data.get('limit', 10)
            },
            "message": message
        }, status=status)

    # 处理普通成功响应
    return Response({
        "success": True,
        "data": data,
        "message": message
    }, status=status)


class CustomPagination(LimitOffsetPagination):
    """
    自定义分页类
    """
    default_limit = 10
    max_limit = 100

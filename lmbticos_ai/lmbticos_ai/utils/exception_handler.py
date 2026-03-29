from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    自定义异常处理程序，统一错误响应格式
    :param exc: 异常对象
    :param context: 上下文
    :return: Response对象
    """
    # 调用DRF默认的异常处理程序获取响应
    response = exception_handler(exc, context)

    if response is not None:
        # 处理标准DRF异常响应
        error_code = response.status_code
        error_message = response.data.get('detail', '请求失败')
        error_details = {k: v for k, v in response.data.items() if k != 'detail'}

        response.data = {
            "success": False,
            "error": {
                "code": error_code,
                "message": error_message,
                "details": error_details
            }
        }
    else:
        # 处理未捕获的异常
        response = Response(
            {
                "success": False,
                "error": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "服务器内部错误",
                    "details": str(exc)
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response

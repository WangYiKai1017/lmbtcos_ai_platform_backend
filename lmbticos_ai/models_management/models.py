from django.db import models


class ModelRouter(models.Model):
    """
    模型路由器模型
    """
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='名称')
    type = models.CharField(max_length=50, verbose_name='类型')
    icon = models.CharField(max_length=10, verbose_name='图标')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    baseUrl = models.URLField(verbose_name='基础URL')
    status = models.CharField(max_length=20, default='active', verbose_name='状态')
    rateLimit = models.CharField(max_length=50, blank=True, null=True, verbose_name='速率限制')
    created = models.DateField(verbose_name='创建日期')
    lastUpdated = models.DateField(verbose_name='最后更新日期')
    
    class Meta:
        verbose_name = '模型路由器'
        verbose_name_plural = '模型路由器'
        ordering = ['-created']
    
    def __str__(self):
        return self.name


class Model(models.Model):
    """
    模型模型
    """
    id = models.CharField(max_length=50, primary_key=True)
    router_id = models.ForeignKey(ModelRouter, on_delete=models.CASCADE, related_name='models', verbose_name='所属路由器')
    name = models.CharField(max_length=100, verbose_name='名称')
    type = models.CharField(max_length=50, verbose_name='类型')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    provider = models.CharField(max_length=50, verbose_name='提供商')
    context = models.CharField(max_length=20, blank=True, null=True, verbose_name='上下文窗口')
    price = models.CharField(max_length=20, verbose_name='价格')
    
    class Meta:
        verbose_name = '模型'
        verbose_name_plural = '模型'
        ordering = ['name']
    
    def __str__(self):
        return self.name

# LMBTCOS-AI 平台后端服务

基于 Python Django + Djongo 构建的后端服务，提供了文档管理、切片工具、模型管理、数据管理、MCP管理、技能管理、看板页面、需求拆解页面和工作流页面等模块的API接口。

## 技术栈

- **框架**: Django 6.0
- **数据库**: MongoDB (使用 Djongo ORM)
- **API**: Django REST Framework
- **认证**: JWT Token

## 项目结构

```
lmbtcos_ai/
├── lmbticos_ai/             # 项目配置目录
│   ├── __init__.py
│   ├── settings.py          # 项目配置文件
│   ├── urls.py              # 项目主路由
│   ├── wsgi.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       ├── response_wrapper.py  # 统一响应格式
│       └── exception_handler.py # 统一异常处理
├── documents/              # 文档管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── slice_tool/             # 切片工具模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── models_management/      # 模型管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── databases/              # 数据管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── mcp_management/         # MCP管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── skills_management/      # 技能管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── kanban/                 # 看板页面模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── requirements/           # 需求拆解页面模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── workflows/              # 工作流页面模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── manage.py
```

## 安装和运行

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install django djongo djangorestframework pyjwt djangorestframework-simplejwt
```

### 2. 配置数据库

确保 MongoDB 服务已启动，并在 `lmbticos_ai/settings.py` 中配置数据库连接信息：

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'lmbticos_ai',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
            'username': '',
            'password': '',
            'authSource': '',
            'authMechanism': '',
        }
    }
}
```

### 3. 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

### 4. 创建超级用户

```bash
python manage.py createsuperuser
```

### 5. 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 `http://localhost:8000` 上运行。

## API 接口

所有 API 接口都遵循 RESTful 设计原则，使用 JSON 格式进行数据交换。接口以 `/v1/` 前缀开头，例如：

- `GET /v1/documents/` - 获取文件系统树
- `POST /v1/slice-tool/files/` - 上传切片文件
- `GET /v1/models/routers/` - 获取模型路由器列表

### 认证

所有 API 接口都需要 JWT Token 认证，在请求头中添加：

```
Authorization: Bearer {token}
```

可以通过以下接口获取 Token：

- `POST /v1/auth/token/` - 获取访问 Token
- `POST /v1/auth/token/refresh/` - 刷新 Token
- `POST /v1/auth/token/verify/` - 验证 Token

### 响应格式

#### 成功响应

```json
{
  "success": true,
  "data": {...}, // 响应数据
  "message": "操作成功"
}
```

#### 分页响应

```json
{
  "success": true,
  "data": {
    "items": [...], // 数据列表
    "total": 100, // 总记录数
    "page": 1, // 当前页码
    "limit": 10 // 每页记录数
  },
  "message": "操作成功"
}
```

#### 错误响应

```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "错误信息",
    "details": {...} // 详细错误信息
  }
}
```

## 开发说明

1. 每个模块都有独立的 `models.py`、`serializers.py`、`views.py` 和 `urls.py` 文件
2. 使用 Djongo 作为 MongoDB 的 ORM 框架
3. 使用 Django REST Framework 构建 RESTful API
4. 使用 JWT Token 进行认证
5. 统一的响应格式和异常处理
6. 支持分页、过滤、排序等功能

## 注意事项

1. 确保 MongoDB 服务已启动
2. 所有 API 接口都需要认证
3. 上传文件接口支持 `multipart/form-data` 格式
4. 详细的 API 文档请参考 `API_DEVELOPMENT_GUIDE.md`

## 后续开发

目前，所有 API 接口的具体实现都已标记为 TODO，需要根据业务需求进行实现。主要包括：

1. 完善各模块的模型和序列化器
2. 实现各 API 接口的具体业务逻辑
3. 添加数据验证和权限控制
4. 实现文件上传和存储功能
5. 添加缓存和性能优化
6. 编写测试用例

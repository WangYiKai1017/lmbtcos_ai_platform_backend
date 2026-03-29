# 后端API开发文档

## 1. 概述

本文档基于`MOCK_DATA_SCHEMA.md`生成，为LMBTCOS-AI平台后端开发提供API接口设计指导。所有API遵循RESTful设计原则，使用JSON格式进行数据交换。

## 2. 通用规范

### 2.1 基础URL

```
https://api.lmbticos.ai/v1
```

### 2.2 认证与授权

所有API接口均需进行认证，使用JWT令牌进行身份验证：

```http
Authorization: Bearer {token}
```

### 2.3 请求格式

所有请求使用JSON格式，设置以下请求头：

```http
Content-Type: application/json
Accept: application/json
```

### 2.4 响应格式

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

### 2.5 错误码

| 错误码 | 描述 |
|--------|------|
| 400 | 无效请求参数 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 2.6 分页与过滤

支持以下查询参数：

- `page`: 当前页码，默认为1
- `limit`: 每页记录数，默认为10，最大为100
- `sort`: 排序字段，支持`+`（升序）和`-`（降序）前缀，如`+created_at`
- `filter`: 过滤条件，JSON格式，如`{"status":"active"}`

## 3. 模块API设计

### 3.1 文档管理 (Document Management)

#### 3.1.1 获取文件系统树

```http
GET /documents
```

**请求参数**：
- `parent_id`: 父文件夹ID，为空则获取根目录

**响应示例**：

```json
{
  "success": true,
  "data": [
    {
      "id": "folder-001",
      "name": "项目文档",
      "type": "folder",
      "icon": "📁",
      "size": "",
      "modified": "2026-03-25",
      "children": [...]
    },
    {
      "id": "file-001",
      "name": "产品需求文档.pdf",
      "type": "file",
      "icon": "📄",
      "size": "2.5 MB",
      "modified": "2026-03-25"
    }
  ],
  "message": "获取文件系统树成功"
}
```

#### 3.1.2 创建文件夹

```http
POST /documents/folders
```

**请求体**：

```json
{
  "name": "新文件夹",
  "parent_id": "folder-001"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "folder-002",
    "name": "新文件夹",
    "type": "folder",
    "icon": "📁",
    "size": "",
    "modified": "2026-03-27",
    "parent_id": "folder-001"
  },
  "message": "创建文件夹成功"
}
```

#### 3.1.3 上传文件

```http
POST /documents/files
Content-Type: multipart/form-data
```

**请求参数**：
- `file`: 文件内容
- `parent_id`: 父文件夹ID

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "file-002",
    "name": "上传的文件.pdf",
    "type": "file",
    "icon": "📄",
    "size": "1.2 MB",
    "modified": "2026-03-27",
    "parent_id": "folder-001",
    "file_type": "pdf",
    "content_type": "application/pdf"
  },
  "message": "上传文件成功"
}
```

#### 3.1.4 获取文件详情

```http
GET /documents/files/{fileId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "file-001",
    "name": "产品需求文档.pdf",
    "type": "file",
    "icon": "📄",
    "size": "2.5 MB",
    "modified": "2026-03-25",
    "parent_id": "folder-002",
    "file_type": "pdf",
    "content_type": "application/pdf",
    "file_path": "/documents/产品需求文档.pdf",
    "uploaded_by": "user-001",
    "access_level": "public"
  },
  "message": "获取文件详情成功"
}
```

#### 3.1.5 删除文件/文件夹

```http
DELETE /documents/{id}
```

**响应示例**：

```json
{
  "success": true,
  "message": "删除成功"
}
```

### 3.2 切片工具 (Slice Tool)

#### 3.2.1 上传切片文件

```http
POST /slice-tool/files
Content-Type: multipart/form-data
```

**请求参数**：
- `file`: PDF/PPT文件
- `name`: 文件名（可选，默认使用原始文件名）

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "slice-file-001",
    "name": "文档.pdf",
    "type": "application/pdf",
    "size": 2560000,
    "uploaded": "2026-03-27T10:30:00.000Z",
    "status": "uploaded"
  },
  "message": "文件上传成功"
}
```

#### 3.2.2 获取上传文件列表

```http
GET /slice-tool/files
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "slice-file-001",
        "name": "文档.pdf",
        "type": "application/pdf",
        "size": 2560000,
        "uploaded": "2026-03-27T10:30:00.000Z",
        "status": "processed"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取文件列表成功"
}
```

#### 3.2.3 获取文档页面

```http
GET /slice-tool/files/{fileId}/pages
```

**响应示例**：

```json
{
  "success": true,
  "data": [
    {
      "id": "page-001",
      "file_id": "slice-file-001",
      "page_number": 1,
      "content": "这是文档的第 1 页内容预览...",
      "selected": false
    },
    {
      "id": "page-002",
      "file_id": "slice-file-001",
      "page_number": 2,
      "content": "这是文档的第 2 页内容预览...",
      "selected": false
    }
  ],
  "message": "获取文档页面成功"
}
```

#### 3.2.4 开始切片处理

```http
POST /slice-tool/files/{fileId}/process
```

**请求体**：

```json
{
  "page_ids": ["page-001", "page-002", "page-003"]
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "slice-result-001",
    "file_id": "slice-file-001",
    "page_ids": "page-001,page-002,page-003",
    "status": "pending"
  },
  "message": "切片处理已开始"
}
```

#### 3.2.5 获取切片结果

```http
GET /slice-tool/results/{resultId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "slice-result-001",
    "file_id": "slice-file-001",
    "page_ids": "page-001,page-002,page-003",
    "processed_content": "{\"pages\": [...]}",
    "status": "completed",
    "created_at": "2026-03-27T10:35:00.000Z",
    "completed_at": "2026-03-27T10:36:30.000Z"
  },
  "message": "获取切片结果成功"
}
```

### 3.3 模型管理 (Model Management)

#### 3.3.1 获取模型路由器列表

```http
GET /models/routers
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "router-001",
        "name": "OpenRouter",
        "type": "国际聚合路由器",
        "icon": "🌐",
        "description": "全球模型覆盖最全面的聚合平台",
        "baseUrl": "https://openrouter.ai/api/v1",
        "status": "active",
        "rateLimit": "50次/天 (免费)",
        "created": "2026-01-10",
        "lastUpdated": "2026-03-25"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取模型路由器列表成功"
}
```

#### 3.3.2 获取模型路由器详情

```http
GET /models/routers/{routerId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "router-001",
    "name": "OpenRouter",
    "type": "国际聚合路由器",
    "icon": "🌐",
    "description": "全球模型覆盖最全面的聚合平台",
    "baseUrl": "https://openrouter.ai/api/v1",
    "status": "active",
    "models": [
      {
        "id": "model-001",
        "name": "openrouter/free",
        "type": "智能路由",
        "description": "自动从可用免费模型中选择",
        "provider": "OpenRouter",
        "context": "1M",
        "price": "免费"
      }
    ],
    "rateLimit": "50次/天 (免费)",
    "created": "2026-01-10",
    "lastUpdated": "2026-03-25"
  },
  "message": "获取模型路由器详情成功"
}
```

#### 3.3.3 获取模型列表

```http
GET /models
```

**查询参数**：
- `router_id`: 可选，按路由器过滤
- `type`: 可选，按模型类型过滤

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "model-001",
        "router_id": "router-001",
        "name": "openrouter/free",
        "type": "智能路由",
        "description": "自动从可用免费模型中选择",
        "provider": "OpenRouter",
        "context": "1M",
        "price": "免费"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取模型列表成功"
}
```

#### 3.3.4 创建模型路由器

```http
POST /models/routers
```

**请求体**：

```json
{
  "name": "新路由器",
  "type": "国内路由器",
  "icon": "🏠",
  "description": "新的国内模型路由器",
  "baseUrl": "https://api.new-router.com/v1",
  "status": "active",
  "rateLimit": "无限制",
  "created": "2026-03-27",
  "lastUpdated": "2026-03-27"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "router-002",
    "name": "新路由器",
    "type": "国内路由器",
    "icon": "🏠",
    "description": "新的国内模型路由器",
    "baseUrl": "https://api.new-router.com/v1",
    "status": "active",
    "rateLimit": "无限制",
    "created": "2026-03-27",
    "lastUpdated": "2026-03-27"
  },
  "message": "创建模型路由器成功"
}
```

### 3.4 数据管理 (Data Management)

#### 3.4.1 获取数据库实例列表

```http
GET /databases
```

**查询参数**：
- `type`: 可选，按数据库类型过滤
- `status`: 可选，按状态过滤

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "db-001",
        "name": "PostgreSQL",
        "type": "pgsql",
        "icon": "🗄️",
        "description": "中台和后端连接的中间数据库",
        "host": "pgsql.middleware.internal",
        "port": 5432,
        "status": "active",
        "version": "15.4",
        "size": "128 GB",
        "tables": 45,
        "connections": 234,
        "uptime": "32 days, 14 hours",
        "lastBackup": "2026-03-25 02:00:00",
        "purpose": "核心业务数据存储"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取数据库实例列表成功"
}
```

#### 3.4.2 获取数据库实例详情

```http
GET /databases/{databaseId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "db-001",
    "name": "PostgreSQL",
    "type": "pgsql",
    "icon": "🗄️",
    "description": "中台和后端连接的中间数据库",
    "host": "pgsql.middleware.internal",
    "port": 5432,
    "status": "active",
    "version": "15.4",
    "size": "128 GB",
    "tables": 45,
    "connections": 234,
    "uptime": "32 days, 14 hours",
    "lastBackup": "2026-03-25 02:00:00",
    "purpose": "核心业务数据存储",
    "features": ["事务支持", "SQL兼容", "JSONB支持", "全文搜索"]
  },
  "message": "获取数据库实例详情成功"
}
```

### 3.5 MCP管理 (MCP Management)

#### 3.5.1 获取MCP工具列表

```http
GET /mcp/tools
```

**查询参数**：
- `type`: 可选，按工具类型过滤
- `status`: 可选，按状态过滤

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "mcp-001",
        "name": "Playwright MCP",
        "type": "浏览器自动化",
        "icon": "🌐",
        "provider": "微软",
        "address": "https://playwright-mcp.example.com",
        "status": "online",
        "version": "1.8.0",
        "description": "由微软官方出品的浏览器自动化工具",
        "usageCount": 12845,
        "lastUsed": "2026-03-25 14:30:45",
        "responseTime": "120ms",
        "availability": "99.9%"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取MCP工具列表成功"
}
```

#### 3.5.2 获取MCP工具详情

```http
GET /mcp/tools/{toolId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "mcp-001",
    "name": "Playwright MCP",
    "type": "浏览器自动化",
    "icon": "🌐",
    "provider": "微软",
    "address": "https://playwright-mcp.example.com",
    "apiKey": "pk_playwright_1234567890abcdef",
    "status": "online",
    "version": "1.8.0",
    "description": "由微软官方出品的浏览器自动化工具",
    "usageCount": 12845,
    "lastUsed": "2026-03-25 14:30:45",
    "responseTime": "120ms",
    "availability": "99.9%",
    "useCases": ["自动化网页操作", "表单填写", "数据提取", "自动化测试"],
    "tags": ["浏览器", "自动化", "测试", "网页代理"]
  },
  "message": "获取MCP工具详情成功"
}
```

#### 3.5.3 创建MCP工具

```http
POST /mcp/tools
```

**请求体**：

```json
{
  "name": "新MCP工具",
  "type": "API工具",
  "icon": "🔧",
  "provider": "供应商",
  "address": "https://new-mcp.example.com",
  "apiKey": "pk_new_1234567890abcdef",
  "status": "online",
  "version": "1.0.0",
  "description": "新的MCP工具",
  "useCases": ["API调用", "数据处理"],
  "tags": ["API", "工具"]
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "mcp-002",
    "name": "新MCP工具",
    "type": "API工具",
    "icon": "🔧",
    "provider": "供应商",
    "address": "https://new-mcp.example.com",
    "apiKey": "pk_new_1234567890abcdef",
    "status": "online",
    "version": "1.0.0",
    "description": "新的MCP工具",
    "usageCount": 0,
    "responseTime": "",
    "availability": "",
    "useCases": ["API调用", "数据处理"],
    "tags": ["API", "工具"]
  },
  "message": "创建MCP工具成功"
}
```

### 3.6 技能管理 (Skill Management)

#### 3.6.1 获取技能分类列表

```http
GET /skills/categories
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "frontend",
        "name": "前端开发 Skills",
        "icon": "🎨",
        "description": "前端开发相关的技能和工具"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取技能分类列表成功"
}
```

#### 3.6.2 获取技能列表

```http
GET /skills
```

**查询参数**：
- `category_id`: 可选，按分类过滤
- `complexity`: 可选，按复杂度过滤
- `language`: 可选，按语言过滤

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "code-reviewer",
        "category_id": "frontend",
        "name": "code-reviewer",
        "description": "代码审查助手，自动检测前端代码问题",
        "language": "JavaScript, TypeScript",
        "complexity": "中级",
        "popularity": 92,
        "usageCount": 15678,
        "lastUpdated": "2026-03-20"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取技能列表成功"
}
```

#### 3.6.3 获取技能详情

```http
GET /skills/{skillId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "code-reviewer",
    "category_id": "frontend",
    "name": "code-reviewer",
    "description": "代码审查助手，自动检测前端代码问题",
    "language": "JavaScript, TypeScript",
    "complexity": "中级",
    "popularity": 92,
    "usageCount": 15678,
    "lastUpdated": "2026-03-20",
    "tags": ["代码审查", "前端", "质量"]
  },
  "message": "获取技能详情成功"
}
```

### 3.7 看板页面 (KanbanLayer)

#### 3.7.1 获取泳道列表

```http
GET /kanban/swimlanes
```

**响应示例**：

```json
{
  "success": true,
  "data": [
    {
      "id": "ready-for-dev",
      "title": "Ready for Dev",
      "order_index": 1
    },
    {
      "id": "in-progress",
      "title": "In Progress",
      "order_index": 2
    }
  ],
  "message": "获取泳道列表成功"
}
```

#### 3.7.2 获取故事卡列表

```http
GET /kanban/cards
```

**查询参数**：
- `swimlane_id`: 可选，按泳道过滤
- `status`: 可选，按状态过滤
- `assignee_id`: 可选，按执行者过滤

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "REQ-001",
        "title": "用户认证系统",
        "summary": "实现用户注册、登录、忘记密码等功能",
        "status": "待处理",
        "assignee": {
          "id": "agent-1",
          "name": "开发agent - 后端",
          "avatar": "🛡️"
        },
        "reporter": {
          "id": "user-1",
          "name": "产品经理",
          "avatar": "👨‍💼"
        },
        "tags": ["认证", "用户", "安全"],
        "reportDate": "2026-03-20",
        "dueDate": "2026-04-10",
        "estimatedTime": "15d",
        "actualTime": "",
        "tokenUsage": "2000",
        "priority": "高"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取故事卡列表成功"
}
```

#### 3.7.3 创建故事卡

```http
POST /kanban/cards
```

**请求体**：

```json
{
  "title": "新功能开发",
  "summary": "实现新功能",
  "description": "详细描述新功能的需求",
  "status": "待处理",
  "assignee_id": "agent-1",
  "assignee_name": "开发agent - 后端",
  "assignee_avatar": "⚙️",
  "reporter_id": "user-1",
  "reporter_name": "产品经理",
  "reporter_avatar": "👨‍💼",
  "tags": ["新功能", "开发"],
  "reportDate": "2026-03-27",
  "dueDate": "2026-04-15",
  "estimatedTime": "10d",
  "priority": "中",
  "checklist": [
    { "text": "设计方案", "completed": false },
    { "text": "开发实现", "completed": false },
    { "text": "测试验证", "completed": false }
  ]
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "REQ-002",
    "title": "新功能开发",
    "summary": "实现新功能",
    "description": "详细描述新功能的需求",
    "status": "待处理",
    "assignee": {
      "id": "agent-1",
      "name": "开发agent - 后端",
      "avatar": "⚙️"
    },
    "reporter": {
      "id": "user-1",
      "name": "产品经理",
      "avatar": "👨‍💼"
    },
    "tags": ["新功能", "开发"],
    "reportDate": "2026-03-27",
    "dueDate": "2026-04-15",
    "estimatedTime": "10d",
    "actualTime": "",
    "tokenUsage": "0",
    "priority": "中",
    "checklist": [
      { "id": 1, "text": "设计方案", "completed": false },
      { "id": 2, "text": "开发实现", "completed": false },
      { "id": 3, "text": "测试验证", "completed": false }
    ]
  },
  "message": "创建故事卡成功"
}
```

#### 3.7.4 更新故事卡状态

```http
PUT /kanban/cards/{cardId}/status
```

**请求体**：

```json
{
  "status": "进行中"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "REQ-001",
    "status": "进行中"
  },
  "message": "更新故事卡状态成功"
}
```

### 3.8 需求拆解页面 (RequirementsLayer)

#### 3.8.1 创建对话会话

```http
POST /requirements/conversations
```

**请求体**：

```json
{
  "title": "新需求拆解",
  "user_id": "user-1"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "conv-001",
    "title": "新需求拆解",
    "user_id": "user-1",
    "created_at": "2026-03-27T10:45:00.000Z",
    "updated_at": "2026-03-27T10:45:00.000Z"
  },
  "message": "创建对话会话成功"
}
```

#### 3.8.2 获取对话消息列表

```http
GET /requirements/conversations/{sessionId}/messages
```

**响应示例**：

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_id": "conv-001",
      "text": "你好！我是需求拆解助手，请问你有什么需求需要拆解？",
      "is_user": false,
      "created_at": "2026-03-27T10:45:00.000Z"
    },
    {
      "id": 2,
      "session_id": "conv-001",
      "text": "我需要开发一个电商订单管理系统",
      "is_user": true,
      "created_at": "2026-03-27T10:46:00.000Z"
    }
  ],
  "message": "获取对话消息列表成功"
}
```

#### 3.8.3 发送对话消息

```http
POST /requirements/conversations/{sessionId}/messages
```

**请求体**：

```json
{
  "text": "我需要开发一个电商订单管理系统",
  "is_user": true
}
```

**响应示例**：

```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "session_id": "conv-001",
      "text": "我需要开发一个电商订单管理系统",
      "is_user": true,
      "created_at": "2026-03-27T10:46:00.000Z"
    },
    {
      "id": 3,
      "session_id": "conv-001",
      "text": "感谢您提供的需求！我将为您进行详细的需求拆解...",
      "is_user": false,
      "created_at": "2026-03-27T10:46:15.000Z"
    }
  ],
  "message": "发送消息成功"
}
```

#### 3.8.4 生成故事卡

```http
POST /requirements/conversations/{sessionId}/generate-cards
```

**请求体**：

```json
{
  "message_id": 3 // 基于哪个消息生成故事卡
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": "ORD-001",
        "title": "用户下单功能",
        "summary": "实现用户浏览商品、添加购物车、提交订单的完整流程",
        "description": "开发用户下单模块...",
        "status": "待处理",
        "assignee_id": "agent-1",
        "assignee_name": "开发agent - 后端",
        "assignee_avatar": "🛒",
        "reporter_id": "user-1",
        "reporter_name": "产品经理",
        "reporter_avatar": "👨‍💼",
        "tags": ["订单", "用户", "购物车"],
        "reportDate": "2026-03-27",
        "dueDate": "2026-04-10",
        "estimatedTime": "20d",
        "tokenUsage": "3000",
        "priority": "高"
      }
    ]
  },
  "message": "生成故事卡成功"
}
```

### 3.9 工作流页面 (WorkflowLayer)

#### 3.9.1 获取工作流列表

```http
GET /workflows
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "wf-001",
        "name": "项目开发流程",
        "description": "项目的完整开发流程",
        "created_by": "user-1",
        "created_at": "2026-03-27T10:50:00.000Z",
        "updated_at": "2026-03-27T10:50:00.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  },
  "message": "获取工作流列表成功"
}
```

#### 3.9.2 获取工作流详情

```http
GET /workflows/{workflowId}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "wf-001",
    "name": "项目开发流程",
    "description": "项目的完整开发流程",
    "created_by": "user-1",
    "created_at": "2026-03-27T10:50:00.000Z",
    "updated_at": "2026-03-27T10:50:00.000Z",
    "nodes": [
      {
        "id": "node-001",
        "workflow_id": "wf-001",
        "card_id": "REQ-001",
        "title": "用户认证系统",
        "summary": "实现用户注册、登录、忘记密码等功能",
        "status": "待处理",
        "x": 100,
        "y": 100
      }
    ],
    "edges": [
      {
        "id": "edge-001",
        "workflow_id": "wf-001",
        "source_node_id": "node-001",
        "target_node_id": "node-002"
      }
    ]
  },
  "message": "获取工作流详情成功"
}
```

#### 3.9.3 创建工作流

```http
POST /workflows
```

**请求体**：

```json
{
  "name": "新工作流",
  "description": "新的工作流描述",
  "created_by": "user-1"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "wf-002",
    "name": "新工作流",
    "description": "新的工作流描述",
    "created_by": "user-1",
    "created_at": "2026-03-27T10:55:00.000Z",
    "updated_at": "2026-03-27T10:55:00.000Z"
  },
  "message": "创建工作流成功"
}
```

#### 3.9.4 添加工作流节点

```http
POST /workflows/{workflowId}/nodes
```

**请求体**：

```json
{
  "card_id": "REQ-002",
  "title": "新功能开发",
  "summary": "实现新功能",
  "status": "待处理",
  "x": 200,
  "y": 200
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "node-003",
    "workflow_id": "wf-001",
    "card_id": "REQ-002",
    "title": "新功能开发",
    "summary": "实现新功能",
    "status": "待处理",
    "x": 200,
    "y": 200
  },
  "message": "添加工作流节点成功"
}
```

#### 3.9.5 添加工作流边

```http
POST /workflows/{workflowId}/edges
```

**请求体**：

```json
{
  "source_node_id": "node-001",
  "target_node_id": "node-003"
}
```

**响应示例**：

```json
{
  "success": true,
  "data": {
    "id": "edge-002",
    "workflow_id": "wf-001",
    "source_node_id": "node-001",
    "target_node_id": "node-003"
  },
  "message": "添加工作流边成功"
}
```

## 4. 数据验证

所有API接口都应进行严格的数据验证，确保数据的完整性和一致性。建议使用以下验证方式：

- **请求参数验证**：验证所有必填参数是否存在，参数类型是否正确
- **数据格式验证**：验证日期、时间、邮箱、URL等格式是否正确
- **业务规则验证**：验证数据是否符合业务逻辑规则
- **权限验证**：验证用户是否有操作该资源的权限

## 5. 性能优化

为了提高API性能，建议：

- **使用分页**：对返回大量数据的接口使用分页
- **添加缓存**：对频繁访问的数据使用缓存
- **优化数据库查询**：使用索引，避免全表扫描
- **压缩响应数据**：使用gzip等压缩算法减小响应大小
- **异步处理**：对耗时操作使用异步处理

## 6. 安全考虑

- **认证与授权**：确保所有API都有适当的认证和授权机制
- **输入验证**：对所有用户输入进行验证，防止注入攻击
- **输出过滤**：对输出数据进行过滤，防止敏感信息泄露
- **HTTPS**：使用HTTPS加密传输数据
- **限流**：对API进行限流，防止滥用
- **日志记录**：记录所有API访问和操作日志，便于审计和排查问题

## 7. 版本控制

API版本控制使用URL路径前缀的方式，如：

```
https://api.lmbticos.ai/v1
```

当API需要重大变更时，应增加版本号，如：

```
https://api.lmbticos.ai/v2
```

## 8. 文档维护

API文档应与代码同步更新，建议使用以下工具：

- **Swagger/OpenAPI**：自动生成API文档
- **Postman**：创建API测试集合和文档
- **Markdown**：手动维护API文档（如本文档）

## 9. 测试

所有API接口都应进行充分的测试，包括：

- **单元测试**：测试单个函数或方法
- **集成测试**：测试多个组件之间的交互
- **API测试**：测试API接口的功能和性能
- **负载测试**：测试API在高负载下的性能

## 10. 部署

- **容器化**：使用Docker容器化部署API服务
- **编排**：使用Kubernetes等工具进行容器编排
- **监控**：使用Prometheus、Grafana等工具监控API性能
- **日志**：使用ELK、Loki等工具收集和分析日志
- **CI/CD**：使用GitHub Actions、Jenkins等工具实现持续集成和持续部署

## 11. 总结

本API开发文档基于`MOCK_DATA_SCHEMA.md`生成，提供了LMBTCOS-AI平台所有模块的API设计指导。后端开发人员应严格按照本文档的规范进行开发，确保API的一致性、安全性和性能。
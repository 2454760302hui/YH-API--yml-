# 🚀 YH API测试框架

<div align="center">

![YH API Testing Framework](https://img.shields.io/badge/YH-API%20Testing-blue?style=for-the-badge&logo=python)
![Python Version](https://img.shields.io/badge/Python-3.7%2B-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**专业级API自动化测试框架 | 智能 • 高效 • 专业**

[快速开始](#-快速开始) • [功能特性](#-核心特性) • [文档](#-使用文档) • [示例](#-使用示例) • [支持](#-技术支持)

</div>

---

## 📖 项目简介

**YH API测试框架** 是一个功能强大、易于使用的API自动化测试工具，专为现代API测试需求而设计。框架集成了AI智能测试、并发执行、专业报告生成等先进功能，帮助开发团队快速构建高质量的API测试体系。

## ✨ 核心特性

### 🎯 智能测试
- **🤖 AI驱动测试**: 集成AI功能，智能生成测试用例和验证规则
- **📊 数据驱动**: 支持YAML配置文件，轻松管理测试数据
- **🔄 参数化测试**: 支持多种数据源的参数化测试
- **🎲 随机测试**: 智能生成随机测试数据

### 🚀 高性能执行
- **⚡ 并发执行**: 支持多线程并发测试，大幅提升测试效率
- **🔗 连接池**: 智能HTTP连接池管理，优化网络性能
- **🌐 协议支持**: HTTP/HTTPS、WebSocket、Socket全协议支持
- **⏱️ 性能监控**: 实时监控请求响应时间和系统资源

### 📊 专业报告
- **📈 Allure报告**: 生成专业级的Allure测试报告，自动打开浏览器
- **📋 实时监控**: 实时查看测试执行状态和进度
- **📄 多格式输出**: 支持JSON、HTML、XML等多种报告格式
- **📊 统计分析**: 详细的测试统计和趋势分析

### 🔧 灵活配置
- **🌍 环境管理**: 支持多环境配置切换（测试/生产/本地）
- **🔌 插件系统**: 可扩展的插件架构
- **✅ 自定义断言**: 支持自定义验证规则和复杂断言
- **📝 变量管理**: 全局变量和会话变量管理

### 📱 通知集成
- **💬 企业微信**: 支持企业微信消息通知
- **📧 邮件通知**: 测试结果邮件推送
- **🔗 Webhook**: 自定义Webhook通知
- **📱 多渠道**: 支持多种通知渠道集成

### 🎨 用户体验
- **🖥️ 交互式Shell**: 美观的命令行界面，支持智能提示
- **📚 在线文档**: 内置Swagger风格的API文档服务
- **🎯 一键生成**: 快速生成测试项目模板
- **🎪 Shell增强**: 分类命令显示，动态状态提示

## 🛠️ 安装指南

### 📋 环境要求
- **Python**: 3.7+ (推荐 3.9+)
- **操作系统**: Windows / macOS / Linux
- **内存**: 建议 2GB+ 可用内存
- **网络**: 稳定的网络连接（用于API测试）

### ⚡ 快速安装

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/yh-api-test.git
cd yh-api-test

# 2. 安装依赖
pip install -r requirements.txt

# 3. 验证安装
python yh_shell.py

# 4. 查看帮助
python yh_shell.py
🚀 YH-API-Test > help
```

### 📦 使用pip安装（推荐）

```bash
# 安装最新版本
pip install api-test-yh-pro

# 升级到最新版本
pip install --upgrade api-test-yh-pro

# 验证安装
yh-api-test --version
```

## 🚀 快速开始

### 1️⃣ 启动YH Shell

```bash
# 启动交互式Shell
python yh_shell.py
```

启动后会看到精美的欢迎界面：

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    🚀 API Testing                                            ║
    ║    ⚡ 智能 • 高效 • 专业                                      ║
    ║                                                               ║
    ║    🔧 HTTP/Socket   📊 Reports  🤖 AI Testing               ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝

    🏆 框架特性:
    • 🎯 精准的API测试 - 智能高效，追求完美
    • 🔥 并发测试支持 - 高性能，永不放弃
    • 📊 详细的测试报告 - 数据驱动，追求完美
    • 🚀 Socket/WebSocket测试 - 全方位覆盖
    • 💬 企业微信通知 - 团队协作无缝对接
    • 🎨 Allure报告 - 专业级测试展示

    输入 'help' 查看所有命令
    输入 'inspire' 获取激励语录
    输入 'fadeaway' 开始你的API测试之旅
    📞 技术支持 QQ: 2677989813

🚀 YH-API-Test >
```

### 2️⃣ 核心命令一览

#### 🎯 测试执行命令
| 命令 | 描述 | 示例 |
|------|------|------|
| `fadeaway [file]` | 开始精准测试 | `fadeaway test.yaml` |
| `load <file>` | 加载测试配置 | `load api_test.yaml` |
| `run` | 运行已加载的测试 | `run` |
| `concurrent <n>` | 并发测试 | `concurrent 5` |

#### 🤖 智能功能命令
| 命令 | 描述 | 示例 |
|------|------|------|
| `ai <url>` | AI智能测试 | `ai https://api.example.com` |
| `socket <host>` | Socket连接测试 | `socket localhost:8080` |
| `wechat [msg]` | 企业微信通知 | `wechat "测试完成"` |

#### 📊 报告和状态命令
| 命令 | 描述 | 示例 |
|------|------|------|
| `report` | 生成Allure报告 | `report` |
| `status` | 查看当前状态 | `status` |
| `docs` | 启动文档服务器 | `docs` |

#### 🔧 工具和管理命令
| 命令 | 描述 | 示例 |
|------|------|------|
| `vars <op>` | 变量管理 | `vars set token abc123` |
| `generate [name]` | 生成测试项目 | `generate my_project` |
| `inspire` | 获取激励语录 | `inspire` |
| `help` | 显示帮助信息 | `help` |

#### 🐚 Shell模式命令
所有命令都支持Shell模式，格式为 `shell <command> [args]`：

```bash
🚀 YH-API-Test > shell run test.yaml
🚀 YH-API-Test > shell ai https://httpbin.org
🚀 YH-API-Test > shell generate demo_project
```

### 3️⃣ 创建测试配置

创建 `api_test.yaml` 文件：

```yaml
# 全局配置
config:
  name: "YH API测试示例"
  base_url: "https://httpbin.org"
  timeout: 30
  headers:
    User-Agent: "YH-API-Test/1.0"

# 全局变量
variables:
  username: "testuser"
  password: "testpass123"

# 测试用例
tests:
  - name: "POST请求测试"
    description: "测试POST请求和JSON响应"
    request:
      method: POST
      url: "/post"
      headers:
        Content-Type: "application/json"
      json:
        username: "${username}"
        password: "${password}"
        timestamp: "${current_time()}"
    validate:
      - check: status_code
        expected: 200
      - check: json.json.username
        expected: "${username}"
      - check: response_time
        expected: less_than
        value: 2000
    extract:
      - user_id: json.json.username

  - name: "GET请求测试"
    description: "测试GET请求和参数传递"
    request:
      method: GET
      url: "/get"
      params:
        user_id: "${user_id}"
        format: "json"
    validate:
      - check: status_code
        expected: 200
      - check: json.args.user_id
        expected: "${user_id}"
      - check: json.headers.Host
        expected: "httpbin.org"

  - name: "文件上传测试"
    description: "测试文件上传功能"
    request:
      method: POST
      url: "/post"
      files:
        file: "test_data.txt"
    validate:
      - check: status_code
        expected: 200
      - check: json.files
        expected: not_empty
```

### 4️⃣ 运行测试

```bash
# 方式1: 直接运行测试文件
🚀 YH-API-Test > fadeaway api_test.yaml

# 方式2: 先加载后运行
🚀 YH-API-Test > load api_test.yaml
✅ 测试文件加载成功: api_test.yaml
🚀 YH-API-Test > run

# 方式3: 并发测试
🚀 YH-API-Test > concurrent 3

# 方式4: Shell模式
🚀 YH-API-Test > shell run api_test.yaml
```

### 5️⃣ 查看测试结果

```bash
# 查看测试状态
🚀 YH-API-Test > status

# 生成Allure报告
🚀 YH-API-Test > report

# 启动文档服务
🚀 YH-API-Test > docs
```

## 🎯 高级功能

### 🤖 AI智能测试

YH框架集成了AI功能，可以智能分析API并生成测试用例：

```bash
# AI分析API并生成测试
🚀 YH-API-Test > ai https://jsonplaceholder.typicode.com/posts

# AI会自动：
# 1. 分析API结构
# 2. 生成测试用例
# 3. 创建验证规则
# 4. 执行智能测试
```

### 🔄 并发测试

支持高性能并发测试，大幅提升测试效率：

```bash
# 设置并发用户数
🚀 YH-API-Test > concurrent 10

# 查看并发测试状态
🚀 YH-API-Test > status
```

### 🌐 Socket/WebSocket测试

支持Socket和WebSocket协议测试：

```bash
# Socket连接测试
🚀 YH-API-Test > socket localhost:8080

# WebSocket测试（在YAML中配置）
- name: "WebSocket连接测试"
  request:
    type: websocket
    url: "ws://localhost:8080/ws"
    message: "Hello WebSocket"
  validate:
    - check: connection_status
      expected: "connected"
```

### 📊 变量管理

强大的变量管理系统，支持全局变量和会话变量：

```bash
# 设置变量
🚀 YH-API-Test > vars set api_token "abc123xyz"
🚀 YH-API-Test > vars set base_url "https://api.example.com"

# 查看所有变量
🚀 YH-API-Test > vars get

# 删除变量
🚀 YH-API-Test > vars del api_token
```

### 📱 企业微信通知

集成企业微信通知，实时推送测试结果：

```bash
# 发送测试完成通知
🚀 YH-API-Test > wechat "API测试已完成，成功率95%"

# 在YAML中配置自动通知
config:
  notifications:
    wechat:
      webhook_url: "your_webhook_url"
      auto_notify: true
```

### 🎨 项目生成器

一键生成完整的测试项目模板：

```bash
# 生成测试项目
🚀 YH-API-Test > generate my_api_project

# 生成的项目结构：
my_api_project/
├── config/
│   ├── test_config.yaml
│   └── prod_config.yaml
├── tests/
│   ├── basic_tests.yaml
│   └── advanced_tests.yaml
├── data/
│   └── test_data.json
├── reports/
└── run.py
```

## ⚙️ 配置详解

### 🌍 环境配置

支持多环境配置管理：

```yaml
# config/environments.yaml
environments:
  test:
    base_url: "https://test-api.example.com"
    timeout: 30
    retry_count: 3

  prod:
    base_url: "https://api.example.com"
    timeout: 60
    retry_count: 5

  local:
    base_url: "http://localhost:8000"
    timeout: 10
    retry_count: 1
```

### 🔧 全局配置项

```yaml
config:
  # 基础配置
  name: "API测试项目"
  version: "1.0.0"
  base_url: "https://api.example.com"
  timeout: 30

  # 请求配置
  headers:
    User-Agent: "YH-API-Test/1.0"
    Accept: "application/json"

  # 认证配置
  auth:
    type: "bearer"
    token: "${api_token}"

  # 重试配置
  retry:
    count: 3
    delay: 1
    backoff: 2

  # 报告配置
  reports:
    allure:
      enabled: true
      auto_open: true

  # 通知配置
  notifications:
    wechat:
      enabled: true
      webhook_url: "${wechat_webhook}"
```

### 📋 断言配置

支持丰富的断言类型：

```yaml
validate:
  # 状态码断言
  - check: status_code
    expected: 200

  # JSON路径断言
  - check: json.data.id
    expected: greater_than
    value: 0

  # 响应时间断言
  - check: response_time
    expected: less_than
    value: 1000

  # 正则表达式断言
  - check: json.email
    expected: regex
    pattern: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  # 自定义断言
  - check: custom
    script: |
      assert response.json()['status'] == 'success'
      assert len(response.json()['data']) > 0
```

## 📚 使用文档

### 🔍 内置文档服务

框架提供内置的文档服务，支持Swagger风格的API文档：

```bash
# 启动文档服务器
🚀 YH-API-Test > docs

# 访问 http://localhost:8080 查看文档
# 文档包含：
# - API接口文档
# - 测试用例示例
# - 配置说明
# - 最佳实践
```

### 📖 示例项目

查看 `examples/` 目录获取更多示例：

- `enhanced_test_example.py` - Python API调用示例
- `enhanced_yaml_test.yaml` - 完整的YAML配置示例
- `api_test_project/` - 完整项目模板

## 🚀 最佳实践

### 1. 项目结构建议

```
your_project/
├── config/
│   ├── test.yaml      # 测试环境配置
│   ├── prod.yaml      # 生产环境配置
│   └── common.yaml    # 通用配置
├── tests/
│   ├── auth/          # 认证相关测试
│   ├── user/          # 用户相关测试
│   └── order/         # 订单相关测试
├── data/
│   ├── users.json     # 测试数据
│   └── products.json  # 产品数据
├── utils/
│   └── helpers.py     # 辅助函数
└── reports/           # 测试报告
```

### 2. 命名规范

- 测试文件：`test_<module>_<feature>.yaml`
- 测试用例：使用描述性名称，如 "用户登录成功测试"
- 变量名：使用下划线命名，如 `api_token`, `user_id`

### 3. 错误处理

```yaml
tests:
  - name: "带错误处理的测试"
    request:
      method: GET
      url: "/api/users/999"
    validate:
      - check: status_code
        expected: 404
    on_failure:
      - log: "用户不存在，符合预期"
      - continue: true
```

## 📞 技术支持

### 💬 联系方式
- **QQ技术支持**: 2677989813
- **GitHub Issues**: 欢迎提交Bug报告和功能建议
- **Pull Requests**: 欢迎贡献代码

### 🤝 贡献指南
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

<div align="center">

**💪 YH精神永存！持续改进，追求卓越！** 🚀

*让API测试变得简单而强大*

</div>

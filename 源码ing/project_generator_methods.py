#!/usr/bin/env python3
"""
项目生成器的辅助方法
包含各种文件创建方法的实现
"""

def create_run_script_content():
    """创建运行脚本内容"""
    return '''#!/usr/bin/env python3
"""
API测试项目运行脚本
使用YH API测试框架执行测试
"""

import os
import sys
import yaml
import json
import time
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def load_config():
    """加载配置文件"""
    config_path = Path("config/test_config.yaml")
    if not config_path.exists():
        print(f"{Fore.RED}❌ 配置文件不存在: {config_path}{Style.RESET_ALL}")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_test_cases():
    """加载测试用例"""
    test_path = Path("tests/api_tests.yaml")
    if not test_path.exists():
        print(f"{Fore.RED}❌ 测试用例文件不存在: {test_path}{Style.RESET_ALL}")
        return None
    
    with open(test_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_tests():
    """运行测试"""
    print(f"{Fore.YELLOW + Style.BRIGHT}🚀 YH API测试框架 - 项目测试{Style.RESET_ALL}")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    if not config:
        return False
    
    # 加载测试用例
    test_cases = load_test_cases()
    if not test_cases:
        return False
    
    print(f"{Fore.CYAN}📋 项目信息:{Style.RESET_ALL}")
    print(f"  名称: {test_cases.get('project', {}).get('name', 'Unknown')}")
    print(f"  版本: {test_cases.get('project', {}).get('version', '1.0.0')}")
    print(f"  描述: {test_cases.get('project', {}).get('description', 'No description')}")
    
    print(f"\\n{Fore.CYAN}🔧 配置信息:{Style.RESET_ALL}")
    print(f"  基础URL: {config.get('server', {}).get('base_url', 'Not configured')}")
    print(f"  超时时间: {config.get('server', {}).get('timeout', 30)}秒")
    print(f"  重试次数: {config.get('server', {}).get('retry_count', 3)}")
    
    # 检查是否安装了api-test-yh-pro
    try:
        # 尝试导入yh_shell模块
        sys.path.append('..')  # 添加上级目录到路径
        from yh_shell import YHShell

        print(f"\\n{Fore.GREEN}✅ 检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 启动测试执行...{Style.RESET_ALL}")

        # 创建shell实例并运行测试
        shell = YHShell()
        shell.do_load("tests/api_tests.yaml")
        shell.do_run("")

        return True
        
    except ImportError:
        print(f"\\n{Fore.YELLOW}⚠️  未检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📦 请先安装框架: pip install api-test-yh-pro{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 或者将此项目复制到框架目录中运行{Style.RESET_ALL}")

        # 提供手动运行指导
        print(f"\\n{Fore.MAGENTA}📋 手动运行步骤:{Style.RESET_ALL}")
        print("1. 安装框架: pip install api-test-yh-pro")
        print("2. 启动框架: python -c \\"from yh_shell import YHShell; YHShell().cmdloop()\\"")
        print("3. 在框架中运行: load tests/api_tests.yaml")
        print("4. 执行测试: run")
        
        return False

def main():
    """主函数"""
    print(f"{Fore.MAGENTA + Style.BRIGHT}YH精神永存！{Style.RESET_ALL}")
    
    success = run_tests()
    
    if success:
        print(f"\\n{Fore.GREEN + Style.BRIGHT}🎉 测试执行完成！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 查看报告: reports/目录{Style.RESET_ALL}")
    else:
        print(f"\\n{Fore.RED}❌ 测试执行失败{Style.RESET_ALL}")
    
    print(f"\\n{Fore.YELLOW}\\"持续改进，追求完美！\\" - YH精神{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
'''

def create_readme_content():
    """创建README内容"""
    return '''# API测试项目

基于YH API测试框架的完整API测试项目模板。

## 🚀 项目简介

这是一个使用YH API测试框架生成的完整测试项目，包含了完整的配置文件、测试用例、数据文件和工具类，可以直接用于API接口测试。

## 📁 项目结构

```
api_test_project/
├── config/                 # 配置文件目录
│   ├── test_config.yaml   # 主配置文件
│   └── environments.yaml  # 环境配置文件
├── tests/                  # 测试用例目录
│   └── api_tests.yaml     # API测试用例
├── data/                   # 测试数据目录
│   ├── test_data.yaml     # 测试数据文件
│   └── test_file.txt      # 测试文件
├── utils/                  # 工具类目录
│   └── helpers.py         # 辅助工具类
├── reports/               # 测试报告目录
├── run_tests.py          # 测试运行脚本
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install api-test-kb-pro
```

### 2. 配置项目

编辑 `config/test_config.yaml` 文件，更新以下配置：

- `server.base_url`: 替换为实际的API服务器地址
- `auth`: 配置认证信息（token、用户名密码等）
- 其他相关配置

### 3. 更新测试用例

编辑 `tests/api_tests.yaml` 文件：

- 将示例URL替换为实际的API接口地址
- 更新请求参数、请求体数据
- 修改断言条件以匹配实际API响应

### 4. 运行测试

```bash
# 方式1: 使用项目运行脚本
python run_tests.py

# 方式2: 使用YH框架命令行
python -c "from yh_shell import YHShell; YHShell().cmdloop()"
# 然后在框架中执行:
# > load tests/api_tests.yaml
# > run
```

## 📋 配置说明

### 主配置文件 (config/test_config.yaml)

- **base**: 项目基本信息
- **server**: API服务器配置
- **auth**: 认证配置（支持Bearer Token、Basic Auth、API Key）
- **database**: 数据库配置（可选）
- **reporting**: 报告生成配置
- **notifications**: 通知配置（企业微信、邮件）
- **concurrency**: 并发测试配置

### 测试用例文件 (tests/api_tests.yaml)

- **project**: 测试项目信息
- **globals**: 全局变量定义
- **tests**: 测试用例列表
- **suites**: 测试套件配置

## 🧪 测试用例类型

项目包含以下类型的测试用例示例：

1. **GET请求测试** - 获取数据接口测试
2. **POST请求测试** - 创建数据接口测试
3. **PUT请求测试** - 更新数据接口测试
4. **DELETE请求测试** - 删除数据接口测试
5. **文件上传测试** - 文件上传接口测试
6. **参数化测试** - 批量数据测试
7. **依赖测试** - 测试用例间的依赖关系

## 🔧 自定义配置

### 添加新的测试用例

在 `tests/api_tests.yaml` 的 `tests` 部分添加新的测试用例：

```yaml
- name: "新测试用例"
  description: "测试描述"
  method: "GET"
  url: "${base_url}/your-endpoint"
  headers:
    Content-Type: "application/json"
  assertions:
    - type: "status_code"
      expected: 200
```

### 配置认证

在 `config/test_config.yaml` 中配置认证信息：

```yaml
auth:
  type: "bearer"  # bearer, basic, api_key
  token: "your_actual_token_here"
```

### 设置环境变量

在 `config/environments.yaml` 中配置不同环境：

```yaml
dev:
  base_url: "https://dev-api.example.com"
test:
  base_url: "https://test-api.example.com"
prod:
  base_url: "https://api.example.com"
```

## 📊 测试报告

测试完成后，报告将生成在 `reports/` 目录中：

- `test_report.html` - HTML格式报告
- `test_results.json` - JSON格式结果
- `allure-report/` - Allure报告（如果启用）

## 🤖 AI智能测试

框架支持AI智能测试功能：

```bash
# 在YH框架中使用
> ai https://your-api-server.com
```

## 💡 使用技巧

1. **变量替换**: 在测试用例中使用 `${variable_name}` 进行变量替换
2. **数据提取**: 使用 `extract` 从响应中提取数据供后续测试使用
3. **测试套件**: 使用 `suites` 组织不同类型的测试
4. **并发测试**: 配置 `concurrency` 进行并发测试
5. **通知集成**: 配置企业微信或邮件通知测试结果

## 🚀 YH精神

> "持续改进，追求完美！" - YH精神

持续改进，追求完美的API测试！

## 📞 支持

如有问题，请联系：
- QQ: 2677989813
- 项目地址: [api-test-kb-pro](https://github.com/your-repo)

---

**💪 YH精神永存！继续追求完美的API测试！**
'''

def create_env_config_content():
    """创建环境配置内容"""
    return '''# 环境配置文件
# 支持多环境配置，便于在不同环境间切换

# 开发环境
dev:
  name: "开发环境"
  base_url: "https://dev-api.example.com"  # 替换为实际开发环境地址
  database:
    host: "dev-db.example.com"
    port: 5432
    name: "dev_database"
  auth:
    token: "dev_token_here"
  features:
    debug_mode: true
    mock_external_apis: true

# 测试环境
test:
  name: "测试环境"
  base_url: "https://test-api.example.com"  # 替换为实际测试环境地址
  database:
    host: "test-db.example.com"
    port: 5432
    name: "test_database"
  auth:
    token: "test_token_here"
  features:
    debug_mode: true
    mock_external_apis: false

# 预发布环境
staging:
  name: "预发布环境"
  base_url: "https://staging-api.example.com"  # 替换为实际预发布环境地址
  database:
    host: "staging-db.example.com"
    port: 5432
    name: "staging_database"
  auth:
    token: "staging_token_here"
  features:
    debug_mode: false
    mock_external_apis: false

# 生产环境
prod:
  name: "生产环境"
  base_url: "https://api.example.com"  # 替换为实际生产环境地址
  database:
    host: "prod-db.example.com"
    port: 5432
    name: "prod_database"
  auth:
    token: "prod_token_here"
  features:
    debug_mode: false
    mock_external_apis: false
    read_only_mode: true  # 生产环境只读模式

# 本地环境
local:
  name: "本地环境"
  base_url: "http://localhost:8080"
  database:
    host: "localhost"
    port: 5432
    name: "local_database"
  auth:
    token: "local_token_here"
  features:
    debug_mode: true
    mock_external_apis: true
'''

def create_test_data_content():
    """创建测试数据内容"""
    return '''# 测试数据文件
# 包含各种测试场景的数据

# 用户测试数据
users:
  valid_user:
    name: "张三"
    email: "zhangsan@example.com"
    age: 25
    department: "技术部"
    phone: "13800138000"
    address: "北京市朝阳区"
  
  invalid_user:
    name: ""  # 空名称
    email: "invalid-email"  # 无效邮箱
    age: -1  # 无效年龄
  
  admin_user:
    name: "管理员"
    email: "admin@example.com"
    role: "admin"
    permissions: ["read", "write", "delete"]

# 产品测试数据
products:
  valid_product:
    name: "测试产品"
    description: "这是一个测试产品"
    price: 99.99
    category: "电子产品"
    stock: 100
    tags: ["测试", "产品", "电子"]
  
  expensive_product:
    name: "高端产品"
    price: 9999.99
    category: "奢侈品"
  
  out_of_stock_product:
    name: "缺货产品"
    stock: 0

# 订单测试数据
orders:
  simple_order:
    user_id: 12345
    products:
      - product_id: 1
        quantity: 2
        price: 99.99
      - product_id: 2
        quantity: 1
        price: 199.99
    total_amount: 399.97
    shipping_address: "北京市朝阳区测试地址"
  
  bulk_order:
    user_id: 12345
    products:
      - product_id: 1
        quantity: 100
        price: 99.99

# 认证测试数据
auth:
  valid_credentials:
    username: "testuser"
    password: "testpass123"
    email: "testuser@example.com"
  
  invalid_credentials:
    username: "wronguser"
    password: "wrongpass"
  
  expired_token: "expired.jwt.token.here"
  valid_token: "valid.jwt.token.here"

# 文件测试数据
files:
  valid_image:
    filename: "test_image.jpg"
    content_type: "image/jpeg"
    size: 1024000  # 1MB
  
  large_file:
    filename: "large_file.zip"
    content_type: "application/zip"
    size: 10485760  # 10MB
  
  invalid_file:
    filename: "test.exe"
    content_type: "application/x-executable"

# 搜索测试数据
search:
  valid_queries:
    - "测试"
    - "产品"
    - "用户"
  
  invalid_queries:
    - ""  # 空查询
    - "a"  # 太短
    - "x" * 1000  # 太长
  
  special_queries:
    - "测试 AND 产品"
    - "用户 OR 客户"
    - '"精确匹配"'

# 分页测试数据
pagination:
  valid_params:
    - page: 1
      size: 10
    - page: 2
      size: 20
    - page: 1
      size: 50
  
  invalid_params:
    - page: 0
      size: 10
    - page: 1
      size: 0
    - page: -1
      size: -1

# 边界值测试数据
boundary_values:
  strings:
    empty: ""
    single_char: "a"
    max_length: "a" * 255
    unicode: "测试🏀🐍"
  
  numbers:
    zero: 0
    negative: -1
    max_int: 2147483647
    min_int: -2147483648
    decimal: 123.456
  
  arrays:
    empty: []
    single_item: [1]
    large_array: [1, 2, 3, 4, 5] * 100

# 错误场景数据
error_scenarios:
  network_errors:
    - timeout: 30000  # 超时场景
    - connection_refused: true  # 连接拒绝
  
  server_errors:
    - status_code: 500
      message: "内部服务器错误"
    - status_code: 503
      message: "服务不可用"
  
  client_errors:
    - status_code: 400
      message: "请求参数错误"
    - status_code: 401
      message: "未授权访问"
    - status_code: 404
      message: "资源不存在"
'''

def create_utils_content():
    """创建工具类内容"""
    return '''#!/usr/bin/env python3
"""
测试辅助工具类
提供常用的测试工具函数
"""

import json
import yaml
import time
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class TestHelpers:
    """测试辅助工具类"""
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱地址"""
        username = TestHelpers.generate_random_string(8)
        domains = ['example.com', 'test.com', 'demo.org']
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_phone() -> str:
        """生成随机手机号"""
        prefixes = ['138', '139', '150', '151', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"
    
    @staticmethod
    def generate_timestamp(days_offset: int = 0) -> str:
        """生成时间戳"""
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.isoformat()
    
    @staticmethod
    def load_test_data(file_path: str) -> Dict[str, Any]:
        """加载测试数据文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif file_path.endswith('.json'):
                    return json.load(f)
                else:
                    raise ValueError(f"不支持的文件格式: {file_path}")
        except Exception as e:
            print(f"加载测试数据失败: {e}")
            return {}
    
    @staticmethod
    def validate_response_structure(response: Dict[str, Any], expected_keys: List[str]) -> bool:
        """验证响应结构"""
        for key in expected_keys:
            if key not in response:
                return False
        return True
    
    @staticmethod
    def extract_json_value(data: Dict[str, Any], path: str) -> Any:
        """从JSON中提取值（支持点号路径）"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: int = 1) -> bool:
        """等待条件满足"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def create_test_file(file_path: str, content: str = "测试文件内容") -> bool:
        """创建测试文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建测试文件失败: {e}")
            return False
    
    @staticmethod
    def cleanup_test_files(file_paths: List[str]) -> None:
        """清理测试文件"""
        import os
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"删除文件失败 {file_path}: {e}")

class DataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_user_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成用户测试数据"""
        users = []
        for i in range(count):
            user = {
                'id': i + 1,
                'name': f"测试用户{i+1:03d}",
                'email': TestHelpers.generate_random_email(),
                'phone': TestHelpers.generate_random_phone(),
                'age': random.randint(18, 65),
                'department': random.choice(['技术部', '产品部', '运营部', '市场部']),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 365))
            }
            users.append(user)
        return users
    
    @staticmethod
    def generate_product_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成产品测试数据"""
        products = []
        categories = ['电子产品', '服装', '食品', '图书', '家居']
        
        for i in range(count):
            product = {
                'id': i + 1,
                'name': f"测试产品{i+1:03d}",
                'description': f"这是第{i+1}个测试产品的描述",
                'price': round(random.uniform(10.0, 1000.0), 2),
                'category': random.choice(categories),
                'stock': random.randint(0, 100),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 30))
            }
            products.append(product)
        return products

class AssertionHelpers:
    """断言辅助工具"""
    
    @staticmethod
    def assert_status_code(actual: int, expected: int) -> bool:
        """断言状态码"""
        return actual == expected
    
    @staticmethod
    def assert_response_time(actual: float, max_time: float) -> bool:
        """断言响应时间"""
        return actual <= max_time
    
    @staticmethod
    def assert_json_contains(response: Dict[str, Any], expected_data: Dict[str, Any]) -> bool:
        """断言JSON包含指定数据"""
        for key, value in expected_data.items():
            if key not in response or response[key] != value:
                return False
        return True
    
    @staticmethod
    def assert_array_length(array: List[Any], expected_length: int) -> bool:
        """断言数组长度"""
        return len(array) == expected_length
    
    @staticmethod
    def assert_string_contains(text: str, substring: str) -> bool:
        """断言字符串包含子串"""
        return substring in text

# 使用示例
if __name__ == "__main__":
    # 生成测试数据示例
    print("生成用户数据:")
    users = DataGenerator.generate_user_data(3)
    for user in users:
        print(f"  {user}")
    
    print("\\n生成产品数据:")
    products = DataGenerator.generate_product_data(2)
    for product in products:
        print(f"  {product}")
    
    # 工具函数示例
    print(f"\\n随机字符串: {TestHelpers.generate_random_string()}")
    print(f"随机邮箱: {TestHelpers.generate_random_email()}")
    print(f"随机手机: {TestHelpers.generate_random_phone()}")
    print(f"当前时间戳: {TestHelpers.generate_timestamp()}")
'''

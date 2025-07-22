#!/usr/bin/env python3
"""
简单项目生成器
创建可靠的项目文件，避免ZIP解压问题
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path

def create_project_files():
    """创建项目文件内容"""
    files_content = {
        "README.md": """# YH API测试框架项目

基于YH API测试框架的完整API测试项目模板。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install api-test-yh-pro
```

### 2. 配置项目
编辑 `config/config.yaml` 文件，更新测试配置。

### 3. 运行测试
```bash
python run.py
```

## 📁 项目结构
```
yh-api-test-project/
├── config/                 # 配置文件目录
│   ├── config.yaml        # 主配置文件
│   ├── environments.yaml  # 环境配置
│   └── global_vars.yaml   # 全局变量
├── test_cases/            # 测试用例目录
│   ├── api_tests/         # API测试用例
│   └── performance_tests/ # 性能测试用例
├── data/                  # 测试数据目录
├── reports/               # 测试报告目录
├── logs/                  # 日志目录
├── scripts/               # 脚本目录
├── run.py                 # 主运行脚本
└── requirements.txt       # 依赖文件
```

## 📞 技术支持
QQ: 2677989813

---
**💪 YH精神永存！持续改进，追求完美！**
""",
        
        "requirements.txt": """api-test-yh-pro>=1.0.0
requests>=2.28.0
pyyaml>=6.0
colorama>=0.4.4
allure-pytest>=2.12.0
""",
        
        "run.py": """#!/usr/bin/env python3
\"\"\"
YH API测试框架项目运行脚本
\"\"\"

import os
import sys
import yaml
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def main():
    \"\"\"主函数\"\"\"
    print(f"{Fore.MAGENTA + Style.BRIGHT}🚀 YH API测试框架{Style.RESET_ALL}")
    print(f"{Fore.CYAN}持续改进，追求完美！{Style.RESET_ALL}")
    
    # 检查配置文件
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        print(f"{Fore.RED}❌ 配置文件不存在: {config_path}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 请先配置 config/config.yaml 文件{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✅ 配置文件检查通过{Style.RESET_ALL}")
    
    # 这里可以添加实际的测试执行逻辑
    print(f"{Fore.BLUE}🧪 开始执行测试...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 请安装 api-test-yh-pro 包后运行完整测试{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📞 技术支持 QQ: 2677989813{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
""",
        
        "config/config.yaml": """# YH API测试框架配置文件

# 基本配置
project:
  name: "YH API测试项目"
  version: "1.0.0"
  description: "基于YH API测试框架的项目"

# 环境配置
environment:
  default: "test"
  base_url: "https://api.example.com"
  timeout: 30

# 测试配置
test:
  concurrent: false
  threads: 1
  retry: 3
  delay: 1

# 报告配置
report:
  type: "allure"
  auto_open: true
  output_dir: "reports"

# 通知配置
notification:
  enabled: false
  webhook_url: ""
  
# 日志配置
logging:
  level: "INFO"
  file: "logs/test.log"
""",
        
        "config/environments.yaml": """# 环境配置文件

environments:
  test:
    base_url: "https://test-api.example.com"
    database_url: "test-db-connection"
    
  staging:
    base_url: "https://staging-api.example.com"
    database_url: "staging-db-connection"
    
  production:
    base_url: "https://api.example.com"
    database_url: "prod-db-connection"
""",
        
        "config/global_vars.yaml": """# 全局变量配置

global_vars:
  # 用户信息
  test_user:
    username: "test_user"
    password: "test_password"
    email: "test@example.com"
  
  # API密钥
  api_keys:
    service_a: "your_api_key_here"
    service_b: "your_api_key_here"
  
  # 测试数据
  test_data:
    product_id: 12345
    category_id: 67890
""",
        
        "test_cases/api_tests/login_test.yaml": """# 登录接口测试用例

test_suite:
  name: "登录接口测试"
  description: "测试用户登录相关接口"

test_cases:
  - name: "用户登录成功"
    description: "测试正确用户名密码登录"
    request:
      method: "POST"
      url: "/api/login"
      headers:
        Content-Type: "application/json"
      body:
        username: "${global_vars.test_user.username}"
        password: "${global_vars.test_user.password}"
    
    assertions:
      - type: "status_code"
        expected: 200
      - type: "json_path"
        path: "$.success"
        expected: true
      - type: "json_path"
        path: "$.data.token"
        exists: true
    
    extract:
      - name: "auth_token"
        path: "$.data.token"
        
  - name: "用户登录失败"
    description: "测试错误密码登录"
    request:
      method: "POST"
      url: "/api/login"
      headers:
        Content-Type: "application/json"
      body:
        username: "${global_vars.test_user.username}"
        password: "wrong_password"
    
    assertions:
      - type: "status_code"
        expected: 401
      - type: "json_path"
        path: "$.success"
        expected: false
""",
        
        "data/test_data.json": """{
  "users": [
    {
      "id": 1,
      "username": "test_user1",
      "email": "user1@example.com",
      "role": "user"
    },
    {
      "id": 2,
      "username": "test_user2", 
      "email": "user2@example.com",
      "role": "admin"
    }
  ],
  "products": [
    {
      "id": 1,
      "name": "测试产品1",
      "price": 99.99,
      "category": "electronics"
    },
    {
      "id": 2,
      "name": "测试产品2",
      "price": 199.99,
      "category": "books"
    }
  ]
}"""
    }
    
    return files_content

def create_simple_zip(output_path="yh-api-test-project-simple.zip"):
    """创建简单的ZIP文件，确保兼容性"""
    print("📦 创建简单项目ZIP文件...")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    project_dir = os.path.join(temp_dir, "yh-api-test-project")
    
    try:
        # 创建项目目录结构
        directories = [
            "config",
            "test_cases/api_tests",
            "test_cases/performance_tests",
            "data",
            "reports/allure-results",
            "logs",
            "scripts"
        ]
        
        for directory in directories:
            dir_path = os.path.join(project_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
        
        # 创建文件
        files_content = create_project_files()
        for file_path, content in files_content.items():
            full_path = os.path.join(project_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 创建ZIP文件 - 使用最简单的方法
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as zipf:  # 不压缩，提高兼容性
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, temp_dir)
                    # 使用正斜杠
                    arc_path = arc_path.replace('\\', '/')
                    zipf.write(file_path, arc_path)
        
        print(f"✅ ZIP文件创建成功: {output_path}")
        print(f"📊 文件大小: {os.path.getsize(output_path)} bytes")
        
        # 测试ZIP文件
        with zipfile.ZipFile(output_path, 'r') as test_zipf:
            file_list = test_zipf.namelist()
            print(f"📋 包含 {len(file_list)} 个文件")
            
            # 测试解压
            test_extract_dir = tempfile.mkdtemp()
            test_zipf.extractall(test_extract_dir)
            print("✅ ZIP文件解压测试成功")
            shutil.rmtree(test_extract_dir)
        
        return output_path
        
    except Exception as e:
        print(f"❌ 创建ZIP文件失败: {e}")
        return None
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

def main():
    """主函数"""
    print("🚀 YH API测试框架 - 简单项目生成器")
    print("=" * 50)
    
    # 创建下载目录
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    
    # 生成ZIP文件
    output_path = os.path.join(download_dir, "yh-api-test-project-simple.zip")
    result = create_simple_zip(output_path)
    
    if result:
        print(f"\n🎉 项目生成成功！")
        print(f"📁 文件位置: {os.path.abspath(result)}")
        print(f"💡 这个ZIP文件应该可以在Windows上正常解压")
        print(f"📞 技术支持 QQ: 2677989813")
    else:
        print(f"\n❌ 项目生成失败")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复ZIP文件解压问题的专用脚本
"""

import os
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_robust_zip(source_dir, zip_path):
    """创建更强健的ZIP文件"""
    print(f"🔧 创建强健的ZIP文件: {zip_path}")
    
    try:
        # 使用最兼容的ZIP设置
        with zipfile.ZipFile(zip_path, 'w', 
                           compression=zipfile.ZIP_DEFLATED,
                           compresslevel=6,
                           allowZip64=True) as zipf:
            
            # 收集所有文件和目录
            all_items = []
            
            for root, dirs, files in os.walk(source_dir):
                # 添加目录
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    rel_path = os.path.relpath(dir_path, source_dir)
                    # 确保使用正斜杠
                    rel_path = rel_path.replace(os.sep, '/')
                    if not rel_path.endswith('/'):
                        rel_path += '/'
                    all_items.append(('dir', dir_path, rel_path))
                
                # 添加文件
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, source_dir)
                    # 确保使用正斜杠
                    rel_path = rel_path.replace(os.sep, '/')
                    all_items.append(('file', file_path, rel_path))
            
            # 按路径排序，确保目录在文件之前
            all_items.sort(key=lambda x: (x[2], x[0] == 'file'))
            
            # 添加到ZIP文件
            for item_type, full_path, rel_path in all_items:
                try:
                    if item_type == 'dir':
                        # 添加空目录
                        zipf.writestr(rel_path, '')
                        print(f"✅ 目录: {rel_path}")
                    else:
                        # 添加文件
                        if os.path.exists(full_path):
                            zipf.write(full_path, rel_path)
                            size = os.path.getsize(full_path)
                            print(f"✅ 文件: {rel_path} ({size} bytes)")
                        else:
                            print(f"⚠️ 文件不存在: {full_path}")
                            
                except Exception as e:
                    print(f"❌ 添加失败 {rel_path}: {e}")
                    
                    # 对于文件，尝试用字符串方式添加
                    if item_type == 'file' and os.path.exists(full_path):
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            zipf.writestr(rel_path, content.encode('utf-8'))
                            print(f"✅ 重试成功: {rel_path}")
                        except Exception as e2:
                            print(f"❌ 重试也失败 {rel_path}: {e2}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建ZIP文件失败: {e}")
        return False

def test_zip_extraction(zip_path):
    """测试ZIP文件解压"""
    print(f"\n🧪 测试ZIP文件解压: {zip_path}")
    
    if not os.path.exists(zip_path):
        print(f"❌ ZIP文件不存在: {zip_path}")
        return False
    
    print(f"📊 文件大小: {os.path.getsize(zip_path)} bytes")
    
    try:
        # 测试ZIP文件是否可读
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            print(f"📋 包含 {len(file_list)} 个项目")
            
            # 显示前几个项目
            for i, item in enumerate(file_list[:5]):
                print(f"   {i+1}. {item}")
            if len(file_list) > 5:
                print(f"   ... 还有 {len(file_list) - 5} 个项目")
            
            # 测试解压到临时目录
            temp_dir = tempfile.mkdtemp(prefix="zip_test_")
            print(f"📁 解压到: {temp_dir}")
            
            try:
                zipf.extractall(temp_dir)
                print("✅ 解压成功")
                
                # 验证解压后的文件
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        size = os.path.getsize(file_path)
                        extracted_files.append((rel_path, size))
                
                print(f"📄 解压出 {len(extracted_files)} 个文件:")
                for rel_path, size in extracted_files[:5]:
                    print(f"   ✅ {rel_path} ({size} bytes)")
                if len(extracted_files) > 5:
                    print(f"   ... 还有 {len(extracted_files) - 5} 个文件")
                
                return True
                
            except Exception as e:
                print(f"❌ 解压失败: {e}")
                return False
            finally:
                # 清理临时目录
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    except zipfile.BadZipFile as e:
        print(f"❌ ZIP文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取ZIP文件失败: {e}")
        return False

def create_test_project():
    """创建测试项目结构"""
    print("📦 创建测试项目结构...")
    
    # 创建临时项目目录
    temp_dir = tempfile.mkdtemp(prefix="test_project_")
    project_dir = os.path.join(temp_dir, "yh-api-test-project")
    os.makedirs(project_dir)
    
    # 创建目录结构
    directories = [
        "config",
        "test_cases/api_tests",
        "test_cases/performance_tests", 
        "reports/allure-results",
        "logs",
        "data",
        "scripts"
    ]
    
    for directory in directories:
        dir_path = os.path.join(project_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    # 创建测试文件
    files_content = {
        "README.md": """# YH API测试框架项目

## 项目简介
这是一个基于YH API测试框架的完整测试项目。

## 快速开始
1. 安装依赖: pip install -r requirements.txt
2. 配置环境: 修改 config/config.yaml
3. 运行测试: python run.py

## 技术支持
QQ: 2677989813
""",
        "requirements.txt": """requests>=2.28.0
pyyaml>=6.0
pytest>=7.0.0
allure-pytest>=2.12.0
""",
        "run.py": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
YH API测试框架主运行脚本
\"\"\"

def main():
    print("🚀 YH API测试框架启动...")
    print("✅ 测试完成!")

if __name__ == "__main__":
    main()
""",
        "config/config.yaml": """# YH API测试框架配置
project:
  name: "YH API测试项目"
  version: "1.0.0"

api:
  base_url: "https://api.example.com"
  timeout: 30
""",
        "test_cases/api_tests/login_test.yaml": """# 登录接口测试
test_info:
  name: "登录接口测试"
  
test_cases:
  - name: "正常登录"
    request:
      method: "POST"
      url: "/api/login"
      json:
        username: "test"
        password: "123456"
    validate:
      - check: "status_code"
        expect: 200
""",
        "data/test_data.json": """{
  "users": [
    {
      "username": "test",
      "password": "123456"
    }
  ]
}"""
    }
    
    # 写入文件
    for file_path, content in files_content.items():
        full_path = os.path.join(project_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建文件: {file_path}")
    
    return temp_dir, project_dir

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 ZIP文件解压问题修复工具")
    print("=" * 60)
    
    # 创建测试项目
    temp_dir, project_dir = create_test_project()
    
    try:
        # 创建ZIP文件
        zip_filename = "yh-api-test-project-fixed.zip"
        zip_path = os.path.join(os.getcwd(), zip_filename)
        
        print(f"\n🔧 生成修复后的ZIP文件...")
        if create_robust_zip(project_dir, zip_path):
            print(f"✅ ZIP文件创建成功: {zip_path}")
            
            # 测试解压
            if test_zip_extraction(zip_path):
                print(f"\n🎉 ZIP文件修复成功!")
                print(f"📁 修复后的文件: {zip_path}")
                print("💡 现在可以正常解压使用了")
            else:
                print(f"\n❌ ZIP文件仍然有问题")
        else:
            print(f"❌ ZIP文件创建失败")
    
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

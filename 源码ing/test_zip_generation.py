#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试ZIP文件生成和解压功能
"""

import os
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import SwaggerDocsServer
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保swagger_docs.py文件存在")
    sys.exit(1)

def test_zip_generation():
    """测试ZIP文件生成功能"""
    print("🧪 开始测试ZIP文件生成功能...")
    
    try:
        # 创建SwaggerDocsServer实例
        docs_server = SwaggerDocsServer()
        
        print("📦 生成项目ZIP文件...")
        zip_filename = docs_server.generate_project_structure()
        
        print(f"✅ ZIP文件生成成功: {zip_filename}")
        
        # 检查ZIP文件是否存在
        download_dir = os.path.join(os.getcwd(), "downloads")
        zip_path = os.path.join(download_dir, zip_filename)
        
        if not os.path.exists(zip_path):
            print(f"❌ ZIP文件不存在: {zip_path}")
            return False
        
        print(f"✅ ZIP文件存在: {zip_path}")
        print(f"📊 文件大小: {os.path.getsize(zip_path)} bytes")
        
        return zip_path
        
    except Exception as e:
        print(f"❌ ZIP文件生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_zip_extraction(zip_path):
    """测试ZIP文件解压功能"""
    print("\n🔍 开始测试ZIP文件解压功能...")
    
    try:
        # 创建临时解压目录
        extract_dir = tempfile.mkdtemp(prefix="test_extract_")
        print(f"📁 解压目录: {extract_dir}")
        
        # 解压ZIP文件
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # 显示ZIP文件内容
            file_list = zipf.namelist()
            print(f"📋 ZIP文件包含 {len(file_list)} 个文件/目录:")
            
            for i, file_name in enumerate(file_list[:10]):  # 只显示前10个
                print(f"   {i+1}. {file_name}")
            
            if len(file_list) > 10:
                print(f"   ... 还有 {len(file_list) - 10} 个文件")
            
            # 解压所有文件
            zipf.extractall(extract_dir)
            print("✅ ZIP文件解压成功")
        
        # 验证解压后的文件结构
        print("\n🔍 验证解压后的文件结构...")
        
        project_dir = os.path.join(extract_dir, "yh-api-test-project")
        if not os.path.exists(project_dir):
            print("❌ 项目目录不存在")
            return False
        
        print(f"✅ 项目目录存在: {project_dir}")
        
        # 检查必要的文件
        required_files = [
            "README.md",
            "requirements.txt", 
            "run.py",
            "config/config.yaml",
            "test_cases/api_tests/login_test.yaml"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = os.path.join(project_dir, file_path)
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                print(f"✅ {file_path} ({file_size} bytes)")
            else:
                missing_files.append(file_path)
                print(f"❌ {file_path} (缺失)")
        
        if missing_files:
            print(f"\n⚠️ 缺失文件: {missing_files}")
            return False
        
        # 检查目录结构
        print("\n📁 检查目录结构...")
        required_dirs = [
            "config",
            "test_cases/api_tests",
            "test_cases/performance_tests",
            "reports/allure-results",
            "logs",
            "data",
            "scripts"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = os.path.join(project_dir, dir_path)
            if os.path.exists(full_path) and os.path.isdir(full_path):
                print(f"✅ {dir_path}/")
            else:
                missing_dirs.append(dir_path)
                print(f"❌ {dir_path}/ (缺失)")
        
        if missing_dirs:
            print(f"\n⚠️ 缺失目录: {missing_dirs}")
        
        # 测试文件内容
        print("\n📄 检查文件内容...")
        
        # 检查README.md
        readme_path = os.path.join(project_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                if "YH API测试框架" in readme_content:
                    print("✅ README.md 内容正确")
                else:
                    print("❌ README.md 内容不正确")
        
        # 检查run.py
        run_py_path = os.path.join(project_dir, "run.py")
        if os.path.exists(run_py_path):
            with open(run_py_path, 'r', encoding='utf-8') as f:
                run_content = f.read()
                if "if __name__ == '__main__':" in run_content:
                    print("✅ run.py 内容正确")
                else:
                    print("❌ run.py 内容不正确")
        
        print(f"\n🎉 ZIP文件解压测试完成!")
        print(f"📁 解压目录: {extract_dir}")
        print("💡 您可以手动检查解压后的文件")
        
        return True
        
    except Exception as e:
        print(f"❌ ZIP文件解压失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 YH API测试框架 - ZIP文件生成和解压测试")
    print("=" * 60)
    
    # 测试ZIP文件生成
    zip_path = test_zip_generation()
    if not zip_path:
        print("❌ ZIP文件生成测试失败")
        return
    
    # 测试ZIP文件解压
    if test_zip_extraction(zip_path):
        print("\n🎉 所有测试通过!")
        print("✅ ZIP文件可以正常生成和解压")
    else:
        print("\n❌ ZIP文件解压测试失败")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

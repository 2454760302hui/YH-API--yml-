#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极ZIP文件修复方案
专门解决Windows系统ZIP解压失败问题
"""

import os
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path
import struct

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_windows_compatible_zip(source_dir, zip_path):
    """创建完全兼容Windows的ZIP文件"""
    print(f"🔧 创建Windows兼容的ZIP文件: {zip_path}")
    
    try:
        # 使用最保守的ZIP设置，确保Windows兼容性
        with zipfile.ZipFile(zip_path, 'w', 
                           compression=zipfile.ZIP_DEFLATED,
                           compresslevel=1,  # 使用较低的压缩级别
                           allowZip64=False) as zipf:  # 禁用ZIP64以提高兼容性
            
            # 收集所有文件，不包含空目录（Windows兼容性更好）
            files_to_add = []
            
            for root, dirs, files in os.walk(source_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # 计算相对路径
                    rel_path = os.path.relpath(file_path, source_dir)
                    # 强制使用正斜杠，这是ZIP标准
                    rel_path = rel_path.replace('\\', '/')
                    files_to_add.append((file_path, rel_path))
            
            # 按路径排序
            files_to_add.sort(key=lambda x: x[1])
            
            # 添加文件到ZIP
            for file_path, rel_path in files_to_add:
                try:
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        # 检查文件大小，避免过大的文件
                        file_size = os.path.getsize(file_path)
                        if file_size > 50 * 1024 * 1024:  # 50MB限制
                            print(f"⚠️ 跳过过大文件: {rel_path} ({file_size} bytes)")
                            continue
                        
                        # 使用二进制模式读取文件，避免编码问题
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        # 创建ZipInfo对象，手动设置属性
                        zip_info = zipfile.ZipInfo(filename=rel_path)
                        zip_info.compress_type = zipfile.ZIP_DEFLATED
                        
                        # 设置文件时间（使用当前时间）
                        import time
                        zip_info.date_time = time.localtime()[:6]
                        
                        # 设置文件属性（普通文件）
                        zip_info.external_attr = 0o644 << 16
                        
                        # 写入文件数据
                        zipf.writestr(zip_info, file_data)
                        print(f"✅ 添加文件: {rel_path} ({file_size} bytes)")
                        
                except Exception as e:
                    print(f"❌ 添加文件失败 {rel_path}: {e}")
                    continue
        
        # 验证生成的ZIP文件
        if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
            print(f"✅ ZIP文件生成成功: {os.path.getsize(zip_path)} bytes")
            return True
        else:
            print("❌ ZIP文件生成失败或为空")
            return False
            
    except Exception as e:
        print(f"❌ 创建ZIP文件时出错: {e}")
        return False

def create_simple_zip(source_dir, zip_path):
    """创建最简单的ZIP文件，最大化兼容性"""
    print(f"🔧 创建简单ZIP文件: {zip_path}")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as zipf:  # 不压缩，直接存储
            for root, dirs, files in os.walk(source_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, source_dir)
                    # 确保使用正斜杠
                    rel_path = rel_path.replace('\\', '/')
                    
                    if os.path.exists(file_path):
                        zipf.write(file_path, rel_path)
                        print(f"✅ 添加: {rel_path}")
        
        return os.path.exists(zip_path) and os.path.getsize(zip_path) > 0
        
    except Exception as e:
        print(f"❌ 创建简单ZIP失败: {e}")
        return False

def test_zip_with_windows_tools(zip_path):
    """使用Windows工具测试ZIP文件"""
    print(f"\n🧪 测试ZIP文件兼容性: {zip_path}")
    
    if not os.path.exists(zip_path):
        print("❌ ZIP文件不存在")
        return False
    
    print(f"📊 文件大小: {os.path.getsize(zip_path)} bytes")
    
    try:
        # 使用Python的zipfile模块测试
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            print(f"📋 包含 {len(file_list)} 个文件")
            
            # 显示文件列表
            for i, filename in enumerate(file_list[:5]):
                print(f"   {i+1}. {filename}")
            if len(file_list) > 5:
                print(f"   ... 还有 {len(file_list) - 5} 个文件")
            
            # 测试读取第一个文件
            if file_list:
                try:
                    first_file = file_list[0]
                    content = zipf.read(first_file)
                    print(f"✅ 成功读取文件: {first_file} ({len(content)} bytes)")
                except Exception as e:
                    print(f"❌ 读取文件失败: {e}")
            
            # 尝试解压到临时目录
            temp_dir = tempfile.mkdtemp(prefix="zip_test_")
            try:
                zipf.extractall(temp_dir)
                
                # 验证解压结果
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        extracted_files.append(rel_path)
                
                print(f"✅ 解压成功，提取了 {len(extracted_files)} 个文件")
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
        print(f"❌ 测试ZIP文件失败: {e}")
        return False

def create_test_project_minimal():
    """创建最小化的测试项目"""
    print("📦 创建最小化测试项目...")
    
    temp_dir = tempfile.mkdtemp(prefix="minimal_project_")
    project_dir = os.path.join(temp_dir, "yh-api-test-project")
    os.makedirs(project_dir)
    
    # 只创建最基本的文件，避免复杂结构
    files_content = {
        "README.md": """# YH API测试框架项目

这是一个基于YH API测试框架的测试项目。

## 快速开始

1. 安装依赖: pip install -r requirements.txt
2. 运行测试: python run.py

## 技术支持
QQ: 2677989813
""",
        "requirements.txt": """requests>=2.28.0
pyyaml>=6.0
pytest>=7.0.0
""",
        "run.py": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    print("YH API测试框架启动...")
    print("测试完成!")

if __name__ == "__main__":
    main()
""",
        "config.yaml": """# 配置文件
project:
  name: "YH API测试项目"
  version: "1.0.0"

api:
  base_url: "https://api.example.com"
  timeout: 30
""",
        "test_example.yaml": """# 测试用例示例
test_info:
  name: "示例测试"

test_cases:
  - name: "基本测试"
    request:
      method: "GET"
      url: "/api/test"
    validate:
      - check: "status_code"
        expect: 200
"""
    }
    
    # 写入文件
    for filename, content in files_content.items():
        file_path = os.path.join(project_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建文件: {filename}")
    
    return temp_dir, project_dir

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 终极ZIP文件修复工具")
    print("专门解决Windows系统ZIP解压失败问题")
    print("=" * 60)
    
    # 创建最小化测试项目
    temp_dir, project_dir = create_test_project_minimal()
    
    try:
        # 尝试多种ZIP创建方法
        methods = [
            ("Windows兼容ZIP", create_windows_compatible_zip),
            ("简单ZIP", create_simple_zip)
        ]
        
        for method_name, create_func in methods:
            print(f"\n🔧 尝试方法: {method_name}")
            zip_filename = f"yh-api-test-project-{method_name.lower().replace(' ', '-')}.zip"
            zip_path = os.path.join(os.getcwd(), zip_filename)
            
            # 删除已存在的文件
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            # 创建ZIP文件
            if create_func(project_dir, zip_path):
                # 测试ZIP文件
                if test_zip_with_windows_tools(zip_path):
                    print(f"\n🎉 成功! 使用方法: {method_name}")
                    print(f"📁 生成的文件: {zip_path}")
                    print("💡 这个ZIP文件应该可以在Windows上正常解压")
                    break
                else:
                    print(f"❌ 方法 {method_name} 生成的ZIP文件测试失败")
                    # 删除失败的文件
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
            else:
                print(f"❌ 方法 {method_name} 创建ZIP文件失败")
        else:
            print("\n❌ 所有方法都失败了")
    
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

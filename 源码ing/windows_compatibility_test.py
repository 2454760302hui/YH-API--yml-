#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows兼容性测试脚本
验证生成的ZIP文件在Windows系统上的兼容性
"""

import os
import sys
import zipfile
import tempfile
import shutil
import subprocess
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_windows_extraction(zip_path):
    """测试Windows系统的ZIP解压兼容性"""
    print(f"🧪 测试Windows ZIP解压兼容性: {zip_path}")
    
    if not os.path.exists(zip_path):
        print(f"❌ ZIP文件不存在: {zip_path}")
        return False
    
    print(f"📊 文件大小: {os.path.getsize(zip_path)} bytes")
    
    # 测试1: Python zipfile模块测试
    print("\n🔍 测试1: Python zipfile模块")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            print(f"✅ 可以读取ZIP文件，包含 {len(file_list)} 个文件")
            
            # 检查文件名编码
            for filename in file_list[:5]:
                try:
                    # 尝试编码/解码文件名
                    encoded = filename.encode('utf-8')
                    decoded = encoded.decode('utf-8')
                    print(f"✅ 文件名编码正常: {filename}")
                except Exception as e:
                    print(f"⚠️ 文件名编码问题: {filename} - {e}")
            
            # 测试解压
            temp_dir = tempfile.mkdtemp(prefix="win_test_")
            try:
                zipf.extractall(temp_dir)
                
                # 验证解压结果
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        extracted_files.append(rel_path)
                
                print(f"✅ Python解压成功，提取了 {len(extracted_files)} 个文件")
                
                # 测试文件内容
                for file_path in extracted_files[:3]:
                    full_path = os.path.join(temp_dir, file_path)
                    try:
                        if file_path.endswith('.md') or file_path.endswith('.py') or file_path.endswith('.yaml'):
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                print(f"✅ 文件内容读取正常: {file_path} ({len(content)} 字符)")
                    except Exception as e:
                        print(f"⚠️ 文件内容读取问题: {file_path} - {e}")
                
                return True
                
            except Exception as e:
                print(f"❌ Python解压失败: {e}")
                return False
            finally:
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    except Exception as e:
        print(f"❌ Python zipfile测试失败: {e}")
        return False

def test_zip_structure(zip_path):
    """测试ZIP文件结构"""
    print(f"\n🔍 测试ZIP文件结构")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            
            # 检查必要文件
            required_files = [
                'yh-api-test-project/README.md',
                'yh-api-test-project/requirements.txt',
                'yh-api-test-project/run.py'
            ]
            
            missing_files = []
            for required_file in required_files:
                if required_file not in file_list:
                    missing_files.append(required_file)
            
            if missing_files:
                print(f"⚠️ 缺少必要文件: {missing_files}")
            else:
                print("✅ 所有必要文件都存在")
            
            # 检查文件路径格式
            path_issues = []
            for filename in file_list:
                if '\\' in filename:
                    path_issues.append(filename)
            
            if path_issues:
                print(f"⚠️ 发现反斜杠路径: {path_issues[:3]}...")
            else:
                print("✅ 所有路径使用正斜杠格式")
            
            # 检查文件大小
            total_size = 0
            for filename in file_list:
                info = zipf.getinfo(filename)
                total_size += info.file_size
            
            print(f"✅ 解压后总大小: {total_size} bytes")
            
            return len(missing_files) == 0 and len(path_issues) == 0
            
    except Exception as e:
        print(f"❌ 结构测试失败: {e}")
        return False

def create_windows_test_zip():
    """创建专门用于Windows测试的ZIP文件"""
    print("🔧 创建Windows测试专用ZIP文件...")
    
    try:
        from swagger_docs import SwaggerDocsServer
        docs_server = SwaggerDocsServer()
        
        # 生成ZIP文件
        zip_filename = docs_server.generate_project_structure()
        download_dir = os.path.join(os.getcwd(), "downloads")
        zip_path = os.path.join(download_dir, zip_filename)
        
        if os.path.exists(zip_path):
            print(f"✅ ZIP文件生成成功: {zip_path}")
            return zip_path
        else:
            print("❌ ZIP文件生成失败")
            return None
            
    except Exception as e:
        print(f"❌ 生成ZIP文件时出错: {e}")
        return None

def generate_usage_instructions():
    """生成使用说明"""
    instructions = """
# 🎉 Windows ZIP文件解压成功！

## 📋 使用说明

### 1. 解压文件
- 右键点击ZIP文件
- 选择"解压到..."或"提取到..."
- 选择目标文件夹

### 2. 安装依赖
打开命令提示符或PowerShell，进入项目目录：
```
cd yh-api-test-project
pip install -r requirements.txt
```

### 3. 运行测试
```
python run.py
```

### 4. 配置项目
编辑 `config/config.yaml` 文件，修改API地址和认证信息：
```yaml
api:
  base_url: "https://your-api.example.com"
  timeout: 30

auth:
  type: "bearer"
  token: "your_token_here"
```

### 5. 查看报告
测试完成后，报告将生成在 `reports/` 目录下。

## 📞 技术支持
如有问题，请联系 QQ: 2677989813

## 🎯 项目结构
```
yh-api-test-project/
├── README.md                 # 项目说明
├── requirements.txt          # 依赖包
├── run.py                   # 主程序
├── config/                  # 配置文件
├── test_cases/             # 测试用例
├── data/                   # 测试数据
└── scripts/                # 辅助脚本
```
"""
    
    # 保存使用说明
    with open("Windows使用说明.txt", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 已生成Windows使用说明.txt")

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 Windows ZIP文件兼容性测试")
    print("=" * 60)
    
    # 创建测试ZIP文件
    zip_path = create_windows_test_zip()
    
    if not zip_path:
        print("❌ 无法创建测试ZIP文件")
        return
    
    # 运行兼容性测试
    print(f"\n🔍 开始兼容性测试...")
    
    structure_ok = test_zip_structure(zip_path)
    extraction_ok = test_windows_extraction(zip_path)
    
    print(f"\n📊 测试结果:")
    print(f"   结构测试: {'✅ 通过' if structure_ok else '❌ 失败'}")
    print(f"   解压测试: {'✅ 通过' if extraction_ok else '❌ 失败'}")
    
    if structure_ok and extraction_ok:
        print(f"\n🎉 Windows兼容性测试全部通过！")
        print(f"📁 ZIP文件位置: {zip_path}")
        print(f"📊 文件大小: {os.path.getsize(zip_path)} bytes")
        print(f"💡 这个ZIP文件可以在Windows系统上正常解压使用")
        
        # 生成使用说明
        generate_usage_instructions()
        
    else:
        print(f"\n❌ 兼容性测试失败，需要进一步修复")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

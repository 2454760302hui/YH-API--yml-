#!/usr/bin/env python3
"""
测试生成的项目是否可以正确执行
"""

import os
import sys
import zipfile
import tempfile
import subprocess
import shutil

def test_project_execution():
    """测试项目执行"""
    print("=" * 60)
    print("测试生成的项目是否可以正确执行")
    print("=" * 60)
    
    try:
        # 导入SwaggerDocsServer
        sys.path.append('.')
        from swagger_docs import SwaggerDocsServer
        
        # 生成项目
        print("1. 生成项目...")
        docs_server = SwaggerDocsServer()
        zip_filename = docs_server.generate_project_structure()
        print(f"   项目生成成功: {zip_filename}")
        
        # 检查ZIP文件
        download_dir = os.path.join(os.getcwd(), 'downloads')
        zip_path = os.path.join(download_dir, zip_filename)
        
        if not os.path.exists(zip_path):
            print(f"   错误: ZIP文件不存在 {zip_path}")
            return False
        
        print(f"   ZIP文件大小: {os.path.getsize(zip_path)} bytes")
        
        # 解压项目
        print("2. 解压项目...")
        temp_extract_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_extract_dir)
            file_list = zf.namelist()
            print(f"   解压成功，包含 {len(file_list)} 个文件")
        
        # 检查项目结构
        print("3. 检查项目结构...")
        project_dir = os.path.join(temp_extract_dir, 'yh-api-test-project')
        
        required_files = [
            'run.py',
            'README.md',
            'requirements.txt',
            'config/config.yaml',
            'config/environments.yaml',
            'config/global_vars.yaml',
            'data/test_data.json',
            'test_cases/api_tests/login_test.yaml'
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = os.path.join(project_dir, file_path)
            if os.path.exists(full_path):
                print(f"   [OK] {file_path}")
            else:
                missing_files.append(file_path)
                print(f"   [MISSING] {file_path}")
        
        if missing_files:
            print(f"   错误: 缺少文件 {missing_files}")
            return False
        
        # 测试运行项目
        print("4. 测试运行项目...")
        run_py_path = os.path.join(project_dir, 'run.py')
        
        if os.path.exists(run_py_path):
            try:
                result = subprocess.run(
                    [sys.executable, 'run.py'], 
                    cwd=project_dir, 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
                
                if result.returncode == 0:
                    print("   [SUCCESS] 项目运行成功！")
                    print("   运行输出:")
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip():
                            print(f"     {line}")
                    
                    # 检查输出是否包含预期内容
                    output = result.stdout
                    expected_keywords = [
                        "YH API测试框架",
                        "检查依赖包",
                        "加载配置文件",
                        "检查项目结构",
                        "运行演示测试",
                        "项目运行完成"
                    ]
                    
                    missing_keywords = []
                    for keyword in expected_keywords:
                        if keyword not in output:
                            missing_keywords.append(keyword)
                    
                    if missing_keywords:
                        print(f"   [WARNING] 输出中缺少预期内容: {missing_keywords}")
                    else:
                        print("   [OK] 输出内容完整")
                    
                else:
                    print(f"   [ERROR] 项目运行失败 (返回码: {result.returncode})")
                    print("   错误输出:")
                    print(result.stderr)
                    return False
                    
            except subprocess.TimeoutExpired:
                print("   [ERROR] 项目运行超时")
                return False
            except Exception as e:
                print(f"   [ERROR] 运行项目时出错: {e}")
                return False
        else:
            print("   [ERROR] run.py 文件不存在")
            return False
        
        # 清理临时文件
        print("5. 清理临时文件...")
        shutil.rmtree(temp_extract_dir)
        print("   清理完成")
        
        print("\n" + "=" * 60)
        print("测试结果: 全部通过！")
        print("生成的项目可以正确解压和执行")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = test_project_execution()
    
    if success:
        print("\n✅ 项目生成和执行测试通过！")
        print("用户现在可以:")
        print("1. 访问 http://localhost:8080/generate-project")
        print("2. 点击'生成并下载项目'")
        print("3. 下载并解压ZIP文件")
        print("4. 运行 python run.py")
        print("5. 按照README.md说明配置和使用")
    else:
        print("\n❌ 测试失败，需要进一步修复")
    
    print("\n技术支持 QQ: 2677989813")

if __name__ == "__main__":
    main()

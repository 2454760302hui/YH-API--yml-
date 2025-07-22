#!/usr/bin/env python3
"""
测试用户完整工作流程
"""

import os
import sys
import zipfile
import tempfile
import subprocess
import shutil

def test_user_workflow():
    """测试用户完整工作流程"""
    print("=" * 60)
    print("测试用户完整工作流程")
    print("=" * 60)
    
    # 1. 生成项目
    print("1. 生成项目...")
    sys.path.append('.')
    from swagger_docs import SwaggerDocsServer
    
    docs_server = SwaggerDocsServer()
    zip_filename = docs_server.generate_project_structure()
    print(f"   ✅ 项目生成成功: {zip_filename}")
    
    # 2. 模拟用户下载和解压
    print("2. 模拟用户下载和解压...")
    download_dir = os.path.join(os.getcwd(), 'downloads')
    zip_path = os.path.join(download_dir, zip_filename)
    
    # 创建用户工作目录
    user_work_dir = tempfile.mkdtemp(prefix='user_test_')
    print(f"   用户工作目录: {user_work_dir}")
    
    # 复制ZIP文件到用户目录
    import shutil
    user_zip_path = os.path.join(user_work_dir, zip_filename)
    shutil.copy2(zip_path, user_zip_path)
    
    # 解压
    with zipfile.ZipFile(user_zip_path, 'r') as zf:
        zf.extractall(user_work_dir)
    print("   ✅ 解压成功")
    
    # 3. 模拟用户安装依赖
    print("3. 模拟用户安装依赖...")
    project_dir = os.path.join(user_work_dir, 'yh-api-test-project')
    req_path = os.path.join(project_dir, 'requirements.txt')
    
    # 显示requirements.txt内容
    print("   requirements.txt内容:")
    with open(req_path, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n')[:10]:  # 显示前10行
            if line.strip() and not line.startswith('#'):
                print(f"     {line}")
    
    # 安装依赖
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
        cwd=project_dir,
        capture_output=True, 
        text=True, 
        timeout=60
    )
    
    if result.returncode == 0:
        print("   ✅ 依赖安装成功")
    else:
        print("   ❌ 依赖安装失败")
        print(f"   错误: {result.stderr[:200]}...")
        return False
    
    # 4. 模拟用户运行项目
    print("4. 模拟用户运行项目...")
    result = subprocess.run(
        [sys.executable, 'run.py'], 
        cwd=project_dir,
        capture_output=True, 
        text=True, 
        timeout=30
    )
    
    if result.returncode == 0:
        print("   ✅ 项目运行成功")
        print("   运行输出:")
        
        # 显示关键输出行
        lines = result.stdout.split('\n')
        key_lines = []
        for line in lines:
            if any(keyword in line for keyword in ['YH API', 'Checking dependencies', '[OK]', '[MISSING]', 'Test Results', 'completed']):
                key_lines.append(line)
        
        for line in key_lines[:15]:  # 显示前15个关键行
            if line.strip():
                print(f"     {line}")
                
        # 检查是否有依赖问题
        if '[MISSING]' in result.stdout:
            print("   ⚠️ 检测到缺少依赖包")
            return False
        else:
            print("   ✅ 所有依赖检查通过")
            
    else:
        print("   ❌ 项目运行失败")
        print(f"   错误: {result.stderr[:200]}...")
        return False
    
    # 5. 清理
    print("5. 清理测试环境...")
    shutil.rmtree(user_work_dir)
    print("   ✅ 清理完成")
    
    return True

def main():
    """主函数"""
    success = test_user_workflow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 用户工作流程测试完全通过！")
        print("\n用户现在可以:")
        print("1. 访问 http://localhost:8080/generate-project")
        print("2. 点击'生成并下载项目'")
        print("3. 下载并解压ZIP文件")
        print("4. 运行: pip install -r requirements.txt")
        print("5. 运行: python run.py")
        print("\n✅ 所有步骤都能正常工作，无编码错误！")
    else:
        print("❌ 用户工作流程测试失败")
        print("需要进一步检查和修复")
    
    print("\n📞 技术支持 QQ: 2677989813")
    print("=" * 60)

if __name__ == "__main__":
    main()

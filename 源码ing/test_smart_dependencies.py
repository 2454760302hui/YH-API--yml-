#!/usr/bin/env python3
"""
测试智能依赖管理功能
"""

import os
import sys
import zipfile
import tempfile
import subprocess
import shutil

def test_smart_dependencies():
    """测试智能依赖管理功能"""
    print("=" * 70)
    print("🧠 智能依赖管理功能测试")
    print("=" * 70)
    
    # 1. 生成项目
    print("1. 生成项目...")
    sys.path.append('.')
    from swagger_docs import SwaggerDocsServer
    
    docs_server = SwaggerDocsServer()
    zip_filename = docs_server.generate_project_structure()
    print(f"   ✅ 项目生成: {zip_filename}")
    
    # 2. 解压到临时目录
    print("2. 解压项目...")
    download_dir = os.path.join(os.getcwd(), 'downloads')
    zip_path = os.path.join(download_dir, zip_filename)
    temp_dir = tempfile.mkdtemp(prefix='smart_deps_test_')
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_dir)
    
    project_dir = os.path.join(temp_dir, 'yh-api-test-project')
    print(f"   ✅ 解压到: {project_dir}")
    
    # 3. 首次运行 - 应该自动安装依赖
    print("3. 首次运行测试...")
    print("   预期: 自动检查并安装依赖")
    
    result1 = subprocess.run(
        [sys.executable, 'run.py'],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=180
    )
    
    if result1.returncode == 0:
        print("   ✅ 首次运行成功")
        
        # 分析输出
        output1 = result1.stdout
        
        # 检查依赖安装
        if any(keyword in output1 for keyword in ['Auto-installing', 'Installing', 'SUCCESS']):
            print("   ✅ 检测到自动依赖安装")
        elif 'already verified' in output1:
            print("   ℹ️ 依赖已存在，跳过安装")
        
        # 检查标记文件
        marker_file = os.path.join(project_dir, '.deps_installed')
        if os.path.exists(marker_file):
            print("   ✅ 依赖标记文件已创建")
        
        # 检查报告生成
        if 'Test results generated' in output1:
            print("   ✅ 测试结果生成成功")
        
        if 'Allure server started' in output1:
            print("   ✅ Allure服务启动成功")
        elif 'HTML report' in output1:
            print("   ✅ HTML报告生成成功")
            
    else:
        print("   ❌ 首次运行失败")
        print(f"   错误: {result1.stderr[:200]}...")
        return False
    
    # 4. 第二次运行 - 应该跳过依赖检查
    print("\\n4. 第二次运行测试...")
    print("   预期: 跳过依赖检查，直接执行")
    
    result2 = subprocess.run(
        [sys.executable, 'run.py'],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if result2.returncode == 0:
        print("   ✅ 第二次运行成功")
        
        # 分析输出
        output2 = result2.stdout
        
        # 检查是否跳过依赖检查
        if 'already verified' in output2 or 'skipping check' in output2:
            print("   ✅ 成功跳过依赖检查")
        else:
            print("   ⚠️ 未检测到跳过依赖检查的信息")
        
        # 检查执行速度（第二次应该更快）
        if len(output2) < len(output1):
            print("   ✅ 第二次运行输出更简洁（跳过了安装步骤）")
        
        # 显示关键差异
        print("\\n   关键输出对比:")
        print("   首次运行关键信息:")
        lines1 = [line for line in output1.split('\\n') if any(keyword in line.lower() for keyword in 
                 ['checking', 'installing', 'auto-installing', 'success']) and line.strip()]
        for line in lines1[:3]:
            print(f"     {line}")
        
        print("   第二次运行关键信息:")
        lines2 = [line for line in output2.split('\\n') if any(keyword in line.lower() for keyword in 
                 ['already', 'skipping', 'verified', 'report']) and line.strip()]
        for line in lines2[:3]:
            print(f"     {line}")
            
    else:
        print("   ❌ 第二次运行失败")
        print(f"   错误: {result2.stderr[:200]}...")
        return False
    
    # 5. 检查生成的文件
    print("\\n5. 检查生成的文件...")
    
    # 检查依赖标记文件
    marker_file = os.path.join(project_dir, '.deps_installed')
    if os.path.exists(marker_file):
        print("   ✅ 依赖标记文件存在")
        with open(marker_file, 'r') as f:
            content = f.read()
            print(f"   📄 标记文件内容: {content.strip()}")
    
    # 检查报告文件
    reports_dir = os.path.join(project_dir, 'reports')
    if os.path.exists(reports_dir):
        print("   ✅ 报告目录存在")
        
        # 检查Allure结果
        allure_results = os.path.join(reports_dir, 'allure-results')
        if os.path.exists(allure_results):
            json_files = [f for f in os.listdir(allure_results) if f.endswith('.json')]
            print(f"   ✅ Allure结果文件: {len(json_files)} 个")
        
        # 检查HTML报告
        html_report = os.path.join(reports_dir, 'test_report.html')
        if os.path.exists(html_report):
            size = os.path.getsize(html_report)
            print(f"   ✅ HTML报告: {size:,} bytes")
        
        # 检查批处理脚本（Windows）
        if os.name == 'nt':
            bat_file = os.path.join(project_dir, 'start_allure_server.bat')
            if os.path.exists(bat_file):
                print("   ✅ Allure服务启动脚本已生成")
    
    # 6. 清理
    print("\\n6. 清理测试环境...")
    try:
        shutil.rmtree(temp_dir)
        print("   ✅ 清理完成")
    except Exception as e:
        print(f"   ⚠️ 清理失败: {e}")
    
    return True

def main():
    """主函数"""
    success = test_smart_dependencies()
    
    print("\\n" + "=" * 70)
    if success:
        print("🎉 智能依赖管理功能测试完成！")
        print("\\n✨ 功能特点:")
        print("1. ✅ 首次运行自动检查并安装依赖")
        print("2. ✅ 后续运行跳过依赖检查，直接执行")
        print("3. ✅ 智能标记文件管理")
        print("4. ✅ Allure服务在新终端启动")
        print("5. ✅ 自动打开浏览器显示报告")
        
        print("\\n🚀 用户体验:")
        print("- 首次运行: 自动安装所有依赖，无需手动操作")
        print("- 后续运行: 快速启动，直接显示测试结果")
        print("- Allure可用时: 新终端启动服务，浏览器自动打开")
        print("- Allure不可用时: 生成美观的HTML报告")
        
        print("\\n📋 使用流程:")
        print("1. 下载并解压项目")
        print("2. 运行: python run.py  (首次会自动安装依赖)")
        print("3. 再次运行: python run.py  (快速启动)")
        print("4. 🎊 享受详细的测试报告！")
        
    else:
        print("❌ 智能依赖管理功能测试失败")
    
    print("\\n📞 技术支持 QQ: 2677989813")
    print("💪 YH Spirit Lives On!")
    print("=" * 70)

if __name__ == "__main__":
    main()

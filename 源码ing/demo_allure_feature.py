#!/usr/bin/env python3
"""
演示Allure报告功能
"""

import os
import sys
import zipfile
import tempfile
import subprocess
import shutil

def demo_allure_feature():
    """演示Allure报告功能"""
    print("=" * 70)
    print("🚀 YH API测试框架 - Allure报告功能演示")
    print("=" * 70)
    
    # 1. 生成项目
    print("1. 生成带Allure功能的项目...")
    sys.path.append('.')
    from swagger_docs import SwaggerDocsServer
    
    docs_server = SwaggerDocsServer()
    zip_filename = docs_server.generate_project_structure()
    print(f"   ✅ 项目生成: {zip_filename}")
    
    # 2. 解压到临时目录
    print("2. 解压项目...")
    download_dir = os.path.join(os.getcwd(), 'downloads')
    zip_path = os.path.join(download_dir, zip_filename)
    temp_dir = tempfile.mkdtemp(prefix='allure_demo_')
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_dir)
    
    project_dir = os.path.join(temp_dir, 'yh-api-test-project')
    print(f"   ✅ 解压到: {project_dir}")
    
    # 3. 安装依赖
    print("3. 安装依赖...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode == 0:
        print("   ✅ 依赖安装成功")
        
        # 检查安装的包
        installed_packages = []
        if 'requests' in result.stdout or 'Successfully installed' in result.stdout:
            installed_packages.append('requests')
        if 'pyyaml' in result.stdout or 'PyYAML' in result.stdout:
            installed_packages.append('pyyaml')
        if 'colorama' in result.stdout:
            installed_packages.append('colorama')
        if 'allure-pytest' in result.stdout:
            installed_packages.append('allure-pytest')
            
        print(f"   📦 已安装: {', '.join(installed_packages) if installed_packages else '所有依赖'}")
    else:
        print("   ❌ 依赖安装失败")
        print(f"   错误: {result.stderr[:200]}...")
        return False
    
    # 4. 运行项目
    print("4. 运行项目并生成报告...")
    result = subprocess.run(
        [sys.executable, 'run.py'],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if result.returncode == 0:
        print("   ✅ 项目运行成功")
        
        # 分析输出
        output_lines = result.stdout.split('\n')
        
        # 检查依赖检查结果
        dependency_ok = []
        for line in output_lines:
            if '[OK]' in line and any(pkg in line for pkg in ['requests', 'pyyaml', 'colorama', 'allure']):
                pkg = line.split('[OK]')[1].strip().split()[0]
                dependency_ok.append(pkg)
        
        if dependency_ok:
            print(f"   ✅ 依赖检查通过: {', '.join(dependency_ok)}")
        
        # 检查测试结果
        test_results = [line for line in output_lines if 'Test Results:' in line or 'Success Rate:' in line or '[PASS]' in line]
        if test_results:
            print("   ✅ 测试执行成功:")
            for line in test_results[:3]:
                if line.strip():
                    print(f"     {line.strip()}")
        
        # 检查报告生成
        report_lines = [line for line in output_lines if any(keyword in line.lower() for keyword in 
                       ['report', 'generated', 'browser', 'allure'])]
        if report_lines:
            print("   📊 报告生成:")
            for line in report_lines[:5]:
                if line.strip():
                    print(f"     {line.strip()}")
        
    else:
        print("   ❌ 项目运行失败")
        print(f"   错误: {result.stderr[:300]}...")
        return False
    
    # 5. 检查生成的文件
    print("5. 检查生成的报告文件...")
    reports_dir = os.path.join(project_dir, 'reports')
    
    if os.path.exists(reports_dir):
        print("   📁 reports/ 目录存在")
        
        # 检查Allure结果
        allure_results_dir = os.path.join(reports_dir, 'allure-results')
        if os.path.exists(allure_results_dir):
            json_files = [f for f in os.listdir(allure_results_dir) if f.endswith('.json')]
            print(f"   ✅ Allure结果文件: {len(json_files)} 个")
            
            # 显示一个结果文件的内容示例
            if json_files:
                import json
                with open(os.path.join(allure_results_dir, json_files[0]), 'r', encoding='utf-8') as f:
                    sample_result = json.load(f)
                    print(f"   📄 示例测试: {sample_result.get('name', 'Unknown')}")
                    print(f"     状态: {sample_result.get('status', 'Unknown')}")
                    print(f"     描述: {sample_result.get('description', 'No description')[:50]}...")
        
        # 检查HTML报告
        html_report = os.path.join(reports_dir, 'test_report.html')
        if os.path.exists(html_report):
            size = os.path.getsize(html_report)
            print(f"   ✅ HTML报告: test_report.html ({size:,} bytes)")
            
            # 检查HTML内容
            with open(html_report, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'YH API Testing Framework' in content:
                    print("   ✅ HTML报告内容正确")
                    
                    # 尝试在浏览器中打开
                    try:
                        import webbrowser
                        full_path = os.path.abspath(html_report)
                        webbrowser.open(f'file://{full_path}')
                        print("   🌐 HTML报告已在浏览器中打开")
                    except Exception as e:
                        print(f"   ⚠️ 无法自动打开浏览器: {e}")
                        print(f"   📍 手动打开: file://{os.path.abspath(html_report)}")
                else:
                    print("   ❌ HTML报告内容异常")
        else:
            print("   ❌ HTML报告未生成")
    else:
        print("   ❌ reports/ 目录不存在")
    
    # 6. 清理
    print("6. 清理临时文件...")
    try:
        shutil.rmtree(temp_dir)
        print("   ✅ 清理完成")
    except Exception as e:
        print(f"   ⚠️ 清理失败: {e}")
    
    return True

def main():
    """主函数"""
    success = demo_allure_feature()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 Allure报告功能演示完成！")
        print("\n✨ 功能特点:")
        print("1. ✅ 自动生成Allure测试结果")
        print("2. ✅ 生成美观的HTML报告")
        print("3. ✅ 自动在浏览器中打开报告")
        print("4. ✅ 支持Allure CLI高级功能")
        print("5. ✅ 提供详细的安装指导")
        
        print("\n🚀 用户使用流程:")
        print("1. 访问 http://localhost:8080/generate-project")
        print("2. 下载并解压项目")
        print("3. 运行: pip install -r requirements.txt")
        print("4. 运行: python run.py")
        print("5. 🎊 自动打开详细测试报告！")
        
        print("\n📈 高级功能:")
        print("- 安装 Allure CLI 获得更强大的报告功能")
        print("- 支持测试趋势分析和历史对比")
        print("- 提供丰富的图表和统计信息")
        
    else:
        print("❌ Allure报告功能演示失败")
    
    print("\n📞 技术支持 QQ: 2677989813")
    print("💪 YH Spirit Lives On!")
    print("=" * 70)

if __name__ == "__main__":
    main()

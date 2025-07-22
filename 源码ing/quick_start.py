#!/usr/bin/env python3
"""
API测试框架一键启动脚本
Quick Start Script for API Testing Framework
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path
import argparse

def print_banner():
    """显示启动横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║    🚀 API Testing - 专业接口测试工具                                                   ║
║    ⚡ 智能化 • 高效率 • 企业级                                                          ║
║                                                                                       ║
║    🔧 HTTP/Socket测试  📊 智能报告  🤖 AI自动化  💬 企业微信通知                        ║
║                                                                                       ║
║                                                                                       ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    required_modules = [
        "requests", "yaml", "fastapi", "uvicorn", "colorama", "faker"
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ {module}")
    
    if missing:
        print(f"\n⚠️  缺少依赖: {', '.join(missing)}")
        print("正在安装缺少的依赖...")
        
        for module in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                print(f"  ✅ {module} 安装成功")
            except subprocess.CalledProcessError:
                print(f"  ❌ {module} 安装失败")
                return False
    
    print("✅ 所有依赖检查完成")
    return True

def start_yh_shell():
    """启动YH Shell"""
    print("🚀 启动YH Shell...")
    try:
        from yh_shell import main as yh_main
        yh_main()
    except ImportError:
        print("❌ 无法导入YH Shell，尝试直接运行...")
        subprocess.run([sys.executable, "yh_shell.py"])

def start_docs_server(port: int = 8080):
    """启动文档服务器"""
    print(f"📚 启动文档服务器 (端口: {port})...")
    try:
        from swagger_docs import SwaggerDocsServer
        server = SwaggerDocsServer(port=port)
        
        # 在新线程中启动服务器
        def run_server():
            server.run()
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 自动打开浏览器
        url = f"http://127.0.0.1:{port}"
        print(f"📖 文档服务器已启动: {url}")

        try:
            webbrowser.open(url)
            print("🌐 已自动打开浏览器")
        except:
            print("⚠️  无法自动打开浏览器，请手动访问上述地址")
        
        return server_thread
        
    except ImportError:
        print("❌ 无法导入文档服务器，尝试直接运行...")
        subprocess.Popen([sys.executable, "swagger_docs.py"])

def generate_test_project():
    """生成测试项目"""
    print("🏗️ 生成测试项目...")
    try:
        import tkinter as tk
        from tkinter import filedialog

        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()

        # 选择目录
        project_dir = filedialog.askdirectory(title="选择测试项目保存目录")

        if not project_dir:
            print("❌ 未选择目录，操作取消")
            return

        # 导入项目生成器
        from yh_shell import YHShell
        shell = YHShell()

        # 生成项目
        project_name = "api_test_project"
        full_path = Path(project_dir) / project_name

        print(f"📁 在目录创建项目: {full_path}")

        if hasattr(shell, '_create_project_files'):
            # 创建项目目录结构
            full_path.mkdir(exist_ok=True)
            (full_path / "config").mkdir(exist_ok=True)
            (full_path / "tests").mkdir(exist_ok=True)
            (full_path / "reports").mkdir(exist_ok=True)
            (full_path / "data").mkdir(exist_ok=True)
            (full_path / "utils").mkdir(exist_ok=True)

            # 生成项目文件
            shell._create_project_files(full_path)
            print("✅ 测试项目生成成功！")
            print(f"📂 项目路径: {full_path}")
            print("💡 使用说明:")
            print("   1. 编辑 config/test_config.yaml 配置文件")
            print("   2. 修改 tests/api_tests.yaml 测试用例")
            print("   3. 运行 python run.py 执行测试")

            # 询问是否立即测试
            test_now = input("\n🚀 是否立即测试生成的项目？(y/n): ").strip().lower()
            if test_now == 'y':
                test_run_py(full_path / "run.py")
        else:
            print("❌ 项目生成功能不可用")

    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("💡 请安装: pip install tkinter")
    except Exception as e:
        print(f"❌ 项目生成失败: {e}")

def test_run_py(run_py_path):
    """测试run.py文件"""
    print(f"🧪 测试运行脚本: {run_py_path}")
    try:
        if run_py_path.exists():
            result = subprocess.run([sys.executable, str(run_py_path)],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ run.py 执行成功！")
                print("📊 输出:")
                print(result.stdout)
            else:
                print("⚠️ run.py 执行有警告:")
                print(result.stderr)
        else:
            print("❌ run.py 文件不存在")
    except subprocess.TimeoutExpired:
        print("⏰ 执行超时，但项目结构正常")
    except Exception as e:
        print(f"❌ 测试执行失败: {e}")

def run_ai_test(target_url: str):
    """运行AI测试"""
    print(f"🤖 运行AI智能测试: {target_url}")
    try:
        from ai_tester import AITester, AITestConfig
        
        # 创建AI测试器
        ai_tester = AITester()
        
        # 配置测试
        config = AITestConfig(
            target_url=target_url,
            test_depth="basic",
            test_types=["functional", "negative"],
            max_tests=10
        )
        
        print("🔍 分析API结构...")
        tests = ai_tester.generate_smart_tests(config)
        print(f"✅ 生成了 {len(tests)} 个智能测试用例")
        
        print("🚀 执行测试...")
        results = ai_tester.run_ai_tests(tests)
        
        print("📊 生成报告...")
        report = ai_tester.generate_test_report(results)
        
        # 保存报告
        report_file = f"ai_test_report_{int(time.time())}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 报告已保存: {report_file}")
        print(f"🏆 测试完成: {results['passed']}/{results['total_tests']} 通过 ({results['success_rate']:.1f}%)")
        
    except ImportError as e:
        print(f"❌ 无法导入AI测试器: {e}")
    except Exception as e:
        print(f"❌ AI测试执行失败: {e}")

def show_menu():
    """显示菜单"""
    menu = """
🎯 选择启动模式:

1. 🚀 YH Shell (交互式命令行界面)
2. 📚 文档服务器 (在线文档和API测试)
0. 🚪 退出

请输入选项 (0-2): """

    return input(menu).strip()

def show_help():
    """显示帮助信息"""
    help_text = """
🏀 API测试框架使用指南

📋 命令行参数:
  --shell         直接启动YH Shell
  --docs          启动文档服务器
  --test          运行快速测试
  --ai <URL>      运行AI测试 (指定目标URL)
  --port <PORT>   指定文档服务器端口 (默认8080)
  --help          显示帮助信息

🎯 功能说明:

  🚀 YH Shell:
     - YH主题的交互式命令行界面
     - 支持加载、运行、并发测试等命令
     - 智能高效的交互式测试体验
  
  📚 文档服务器:
     - Swagger风格的在线API文档
     - 交互式API测试界面
     - 支持在线调试和参数配置
  
  🧪 快速测试:
     - 验证框架核心功能
     - 检查模块导入和基础API调用
     - 生成功能测试报告
  
  🤖 AI智能测试:
     - 自动分析API结构
     - 智能生成测试用例
     - 包含功能、边界、负面测试
     - 生成详细测试报告

📦 安装和配置:
  pip install -r requirements-enhanced.txt
  pip install .

🔗 相关文件:
  - yh_shell.py: YH主题Shell
  - swagger_docs.py: 文档服务器
  - ai_tester.py: AI智能测试
  - test_framework_basic.py: 基础功能测试

🚀 开始您的API测试之旅！
"""
    print(help_text)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="API测试框架一键启动")
    parser.add_argument("--shell", action="store_true", help="启动YH Shell")
    parser.add_argument("--docs", action="store_true", help="启动文档服务器")
    parser.add_argument("--test", action="store_true", help="运行快速测试")
    parser.add_argument("--ai", type=str, help="运行AI测试 (指定目标URL)")
    parser.add_argument("--port", type=int, default=8080, help="文档服务器端口")
    parser.add_argument("--help-detail", action="store_true", help="显示详细帮助")
    
    args = parser.parse_args()
    
    # 显示横幅
    print_banner()
    
    # 显示详细帮助
    if args.help_detail:
        show_help()
        return
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请手动安装缺少的依赖")
        return
    
    # 根据参数启动相应功能
    if args.shell:
        start_yh_shell()
        return
    
    if args.docs:
        server_thread = start_docs_server(args.port)
        if server_thread:
            try:
                print("按 Ctrl+C 停止服务器...")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 服务器已停止")
        return
    
    if args.test:
        # 运行基础测试
        print("🧪 运行基础功能测试...")
        try:
            subprocess.run([sys.executable, "test_framework_basic.py"])
        except FileNotFoundError:
            print("❌ 测试文件不存在")
        return
    
    if args.ai:
        run_ai_test(args.ai)
        return
    
    # 交互式菜单
    while True:
        try:
            choice = show_menu()

            if choice == "0":
                print("👋 再见！感谢使用！")
                break
            elif choice == "1":
                start_yh_shell()
            elif choice == "2":
                server_thread = start_docs_server(args.port)
                if server_thread:
                    try:
                        print("按 Ctrl+C 返回菜单...")
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n🛑 服务器已停止，返回菜单")
            else:
                print("❌ 无效选项，请重新选择")
                
        except KeyboardInterrupt:
            print("\n👋 再见！感谢使用！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()

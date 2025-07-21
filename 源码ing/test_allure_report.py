#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Allure报告功能
"""

import sys
import os
import webbrowser
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import SwaggerDocsServer
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保swagger_docs.py文件存在")
    sys.exit(1)

class TestHandler(BaseHTTPRequestHandler):
    """测试用的HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        self.docs_server = SwaggerDocsServer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == '/allure-report':
                # 获取Allure报告HTML
                html_content = self.docs_server.get_allure_report_html()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
                
            elif self.path == '/':
                # 主页重定向到Allure报告
                self.send_response(302)
                self.send_header('Location', '/allure-report')
                self.end_headers()
                
            else:
                # 404页面
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'<h1>404 - Page Not Found</h1>')
                
        except Exception as e:
            print(f"处理请求时出错: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'<h1>500 - Internal Server Error</h1><p>{str(e)}</p>'.encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def start_test_server(port=8899):
    """启动测试服务器"""
    try:
        server = HTTPServer(('localhost', port), TestHandler)
        print(f"🚀 测试服务器启动成功")
        print(f"📊 Allure报告地址: http://localhost:{port}/allure-report")
        print(f"🌐 服务器地址: http://localhost:{port}")
        print("=" * 50)
        
        # 在新线程中启动服务器
        def run_server():
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 服务器已停止")
                server.shutdown()
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(1)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}/allure-report')
            print("🌐 浏览器已自动打开Allure报告页面")
        except Exception as e:
            print(f"⚠️ 无法自动打开浏览器: {e}")
            print(f"请手动访问: http://localhost:{port}/allure-report")
        
        return server, server_thread
        
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，请尝试其他端口")
            return start_test_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")
            return None, None
    except Exception as e:
        print(f"❌ 启动服务器时出现未知错误: {e}")
        return None, None

def test_allure_report_functionality():
    """测试Allure报告功能"""
    print("🧪 开始测试Allure报告功能...")
    
    try:
        # 创建SwaggerDocsServer实例
        docs_server = SwaggerDocsServer()
        
        # 测试获取Allure报告HTML
        print("📋 测试获取Allure报告HTML...")
        html_content = docs_server.get_allure_report_html()
        
        # 基本验证
        assert isinstance(html_content, str), "HTML内容应该是字符串类型"
        assert len(html_content) > 1000, "HTML内容长度应该大于1000字符"
        assert "Allure测试报告" in html_content, "HTML应该包含标题"
        assert "toggleTestDetails" in html_content, "HTML应该包含JavaScript函数"
        assert "test-item-detailed" in html_content, "HTML应该包含测试项样式类"
        
        print("✅ Allure报告HTML生成测试通过")
        
        # 测试HTML结构
        print("🔍 测试HTML结构...")
        required_elements = [
            "test-results",
            "test-item-detailed", 
            "test-header",
            "test-details",
            "detail-section",
            "error-section",
            "code-block",
            "error-block"
        ]
        
        for element in required_elements:
            assert element in html_content, f"HTML应该包含 {element} 元素"
        
        print("✅ HTML结构测试通过")
        
        # 测试JavaScript功能
        print("⚙️ 测试JavaScript功能...")
        js_functions = [
            "toggleTestDetails",
            "DOMContentLoaded"
        ]
        
        for func in js_functions:
            assert func in html_content, f"HTML应该包含 {func} JavaScript功能"
        
        print("✅ JavaScript功能测试通过")
        
        print("🎉 所有Allure报告功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Allure报告功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 YH API测试框架 - Allure报告测试工具")
    print("=" * 60)
    
    # 先进行功能测试
    if not test_allure_report_functionality():
        print("❌ 功能测试失败，退出程序")
        return
    
    print("\n" + "=" * 50)
    print("🚀 启动测试服务器...")
    
    # 启动测试服务器
    server, server_thread = start_test_server()
    
    if server is None:
        print("❌ 无法启动测试服务器")
        return
    
    try:
        print("\n📝 测试说明:")
        print("1. 点击测试项可展开/收起详细信息")
        print("2. 查看失败测试的堆栈信息")
        print("3. 验证所有接口详情显示正常")
        print("4. 测试响应式布局和交互功能")
        print("\n⌨️ 按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        # 保持服务器运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务器...")
        if server:
            server.shutdown()
        print("✅ 服务器已停止")

if __name__ == "__main__":
    main()

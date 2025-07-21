#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试项目下载功能
"""

import os
import sys
import time
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import SwaggerDocsServer
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)

class TestDownloadHandler(BaseHTTPRequestHandler):
    """测试下载功能的HTTP处理器"""
    
    def __init__(self, *args, **kwargs):
        self.docs_server = SwaggerDocsServer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == '/':
                # 主页 - 项目生成页面
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                html = self.docs_server.get_generate_project_html()
                self.wfile.write(html.encode('utf-8'))
                
            elif self.path == '/generate-project':
                # 项目生成页面
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                html = self.docs_server.get_generate_project_html()
                self.wfile.write(html.encode('utf-8'))
                
            elif self.path.startswith('/download/'):
                # 文件下载
                filename = self.path.split('/')[-1]
                download_dir = os.path.join(os.getcwd(), "downloads")
                file_path = os.path.join(download_dir, filename)
                
                if os.path.exists(file_path):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/zip')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Content-Length', str(os.path.getsize(file_path)))
                    self.end_headers()
                    
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(b'<h1>404 - File Not Found</h1>')
            
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
    
    def do_POST(self):
        """处理POST请求"""
        try:
            if self.path == '/api/generate-project/download':
                # 生成项目并返回下载链接
                try:
                    zip_filename = self.docs_server.generate_project_structure()
                    
                    response_data = f'''{{
                        "success": true,
                        "download_url": "/download/{zip_filename}",
                        "filename": "{zip_filename}",
                        "message": "项目生成成功！"
                    }}'''
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(response_data.encode('utf-8'))
                    
                except Exception as e:
                    error_response = f'''{{
                        "success": false,
                        "message": "生成失败: {str(e)}"
                    }}'''
                    
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(error_response.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            print(f"处理POST请求时出错: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def start_test_server(port=8901):
    """启动测试服务器"""
    try:
        server = HTTPServer(('localhost', port), TestDownloadHandler)
        print(f"🚀 测试服务器启动成功")
        print(f"🌐 访问地址: http://localhost:{port}")
        print(f"📦 项目生成页面: http://localhost:{port}/generate-project")
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
            webbrowser.open(f'http://localhost:{port}/generate-project')
            print("🌐 浏览器已自动打开项目生成页面")
        except Exception as e:
            print(f"⚠️ 无法自动打开浏览器: {e}")
            print(f"请手动访问: http://localhost:{port}/generate-project")
        
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

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 YH API测试框架 - 项目下载功能测试")
    print("=" * 60)
    
    # 启动测试服务器
    server, server_thread = start_test_server()
    
    if server is None:
        print("❌ 无法启动测试服务器")
        return
    
    try:
        print("\n📝 测试说明:")
        print("1. 浏览器会自动打开项目生成页面")
        print("2. 点击 '生成项目' 按钮测试项目生成功能")
        print("3. 点击 '下载项目' 按钮测试文件下载功能")
        print("4. 下载完成后解压文件验证内容完整性")
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

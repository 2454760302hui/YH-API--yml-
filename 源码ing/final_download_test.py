#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终下载功能测试
"""

import os
import sys
import time
import threading
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import SwaggerDocsServer
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)

class FinalTestHandler(BaseHTTPRequestHandler):
    """最终测试的HTTP处理器"""
    
    def __init__(self, *args, **kwargs):
        self.docs_server = SwaggerDocsServer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == '/' or self.path == '/generate-project':
                # 项目生成页面
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                
                html = self.get_test_page_html()
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
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    
                    print(f"✅ 文件下载成功: {filename} ({os.path.getsize(file_path)} bytes)")
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
            print(f"处理GET请求时出错: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'<h1>500 - Internal Server Error</h1><p>{str(e)}</p>'.encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        try:
            if self.path == '/api/generate-project/download':
                # 生成项目并返回下载链接
                print("🔧 开始生成项目...")
                
                try:
                    zip_filename = self.docs_server.generate_project_structure()
                    
                    response_data = {
                        "success": True,
                        "download_url": f"/download/{zip_filename}",
                        "filename": zip_filename,
                        "message": "项目生成成功！点击下载按钮下载项目文件。"
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
                    
                    print(f"✅ 项目生成成功: {zip_filename}")
                    
                except Exception as e:
                    print(f"❌ 项目生成失败: {e}")
                    error_response = {
                        "success": False,
                        "message": f"生成失败: {str(e)}"
                    }
                    
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            print(f"处理POST请求时出错: {e}")
            self.send_response(500)
            self.end_headers()
    
    def get_test_page_html(self):
        """获取测试页面HTML"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YH API测试框架 - 项目下载测试</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 16px;
        }
        .test-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .result.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .download-link {
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s ease;
        }
        .download-link:hover {
            background: #218838;
        }
        .instructions {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin-bottom: 20px;
        }
        .instructions h3 {
            margin-top: 0;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 YH API测试框架</h1>
            <p>项目下载功能测试</p>
        </div>
        
        <div class="instructions">
            <h3>📝 测试说明</h3>
            <ol>
                <li>点击"生成项目"按钮，系统会生成完整的测试项目</li>
                <li>生成成功后会显示下载链接</li>
                <li>点击下载链接下载ZIP文件</li>
                <li>下载完成后解压文件，验证内容完整性</li>
                <li>解压后的项目可以直接使用</li>
            </ol>
        </div>
        
        <div class="test-section">
            <h3>🚀 项目生成与下载</h3>
            <button id="generateBtn" class="btn" onclick="generateProject()">
                📦 生成项目
            </button>
            
            <div id="result" class="result">
                <div id="resultMessage"></div>
            </div>
        </div>
    </div>

    <script>
        async function generateProject() {
            const btn = document.getElementById('generateBtn');
            const result = document.getElementById('result');
            const resultMessage = document.getElementById('resultMessage');
            
            // 禁用按钮
            btn.disabled = true;
            btn.textContent = '⏳ 生成中...';
            
            // 隐藏之前的结果
            result.style.display = 'none';
            
            try {
                const response = await fetch('/api/generate-project/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    result.className = 'result success';
                    resultMessage.innerHTML = `
                        <strong>✅ ${data.message}</strong><br>
                        <a href="${data.download_url}" class="download-link" download="${data.filename}">
                            📥 下载项目文件 (${data.filename})
                        </a>
                        <p><small>💡 下载完成后请解压文件并验证内容完整性</small></p>
                    `;
                } else {
                    result.className = 'result error';
                    resultMessage.innerHTML = `<strong>❌ ${data.message}</strong>`;
                }
                
                result.style.display = 'block';
                
            } catch (error) {
                result.className = 'result error';
                resultMessage.innerHTML = `<strong>❌ 请求失败: ${error.message}</strong>`;
                result.style.display = 'block';
            }
            
            // 恢复按钮
            btn.disabled = false;
            btn.textContent = '📦 生成项目';
        }
    </script>
</body>
</html>'''
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def start_final_test_server(port=8902):
    """启动最终测试服务器"""
    try:
        server = HTTPServer(('localhost', port), FinalTestHandler)
        print(f"🚀 最终测试服务器启动成功")
        print(f"🌐 访问地址: http://localhost:{port}")
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
            webbrowser.open(f'http://localhost:{port}')
            print("🌐 浏览器已自动打开测试页面")
        except Exception as e:
            print(f"⚠️ 无法自动打开浏览器: {e}")
            print(f"请手动访问: http://localhost:{port}")
        
        return server, server_thread
        
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，请尝试其他端口")
            return start_final_test_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")
            return None, None
    except Exception as e:
        print(f"❌ 启动服务器时出现未知错误: {e}")
        return None, None

def main():
    """主函数"""
    print("=" * 60)
    print("🧪 YH API测试框架 - 最终下载功能测试")
    print("=" * 60)
    
    # 启动测试服务器
    server, server_thread = start_final_test_server()
    
    if server is None:
        print("❌ 无法启动测试服务器")
        return
    
    try:
        print("\n📝 测试步骤:")
        print("1. 浏览器会自动打开测试页面")
        print("2. 点击 '生成项目' 按钮")
        print("3. 等待项目生成完成")
        print("4. 点击下载链接下载ZIP文件")
        print("5. 解压文件验证内容完整性")
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

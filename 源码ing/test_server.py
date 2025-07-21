#!/usr/bin/env python3
"""
测试服务器启动
"""

import sys
import traceback
from swagger_docs import SwaggerDocsServer

def test_server():
    """测试服务器启动"""
    try:
        print("正在创建服务器实例...")
        server = SwaggerDocsServer(port=8083, host="127.0.0.1")
        
        print("正在初始化...")
        server._ensure_initialized()
        
        print("检查FastAPI应用...")
        if server.app is None:
            print("❌ FastAPI应用未创建")
            return False
        
        print("检查OpenAPI规范...")
        openapi_spec = server.app.openapi()
        print(f"OpenAPI版本: {openapi_spec.get('openapi', 'NOT SET')}")
        
        print("✅ 服务器初始化成功")
        print("正在启动服务器...")
        
        # 启动服务器
        server.run()
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_server()

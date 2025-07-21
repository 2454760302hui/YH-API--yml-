#!/usr/bin/env python3
"""
测试服务器启动
"""

try:
    print("正在导入模块...")
    from swagger_docs import SwaggerDocsServer
    print("✅ 模块导入成功")
    
    print("正在创建服务器实例...")
    server = SwaggerDocsServer()
    print("✅ 服务器实例创建成功")
    
    print("正在启动服务器...")
    server.run()
    print("✅ 服务器启动成功")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

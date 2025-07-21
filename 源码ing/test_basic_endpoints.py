#!/usr/bin/env python3
"""
测试基本端点功能
"""

import requests
import json

def test_basic_endpoints():
    """测试基本端点"""
    print("🚀 测试基本端点功能")
    print("=" * 50)
    
    # 测试端口
    ports = [8100, 8099, 8098, 8097]
    active_port = None
    
    for port in ports:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/", timeout=3)
            if response.status_code == 200:
                active_port = port
                print(f"✅ 找到活动服务器: 端口 {port}")
                break
        except:
            continue
    
    if not active_port:
        print("❌ 未找到活动服务器")
        return
    
    base_url = f"http://127.0.0.1:{active_port}"
    
    # 测试基本端点
    endpoints = [
        ("/", "主页"),
        ("/docs", "文档页面"),
        ("/openapi.json", "OpenAPI规范"),
    ]
    
    for path, name in endpoints:
        try:
            response = requests.get(f"{base_url}{path}", timeout=5)
            print(f"✅ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    # 测试新增端点（如果可用）
    new_endpoints = [
        ("/examples/config", "配置示例"),
        ("/examples/quickstart", "快速开始"),
        ("/examples/best-practices", "最佳实践"),
    ]
    
    print(f"\n📋 测试新增端点")
    print("-" * 30)
    
    for path, name in new_endpoints:
        try:
            response = requests.get(f"{base_url}{path}", timeout=5)
            if response.status_code == 200:
                try:
                    data = response.json()
                    content_size = len(json.dumps(data))
                    print(f"✅ {name}: {response.status_code} ({content_size} 字符)")
                except:
                    print(f"✅ {name}: {response.status_code} (非JSON响应)")
            else:
                print(f"❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    print(f"\n🔗 访问地址: {base_url}/docs")

if __name__ == "__main__":
    test_basic_endpoints()

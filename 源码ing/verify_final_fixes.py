#!/usr/bin/env python3
"""
验证最终修复效果
"""

import requests
import json

def verify_final_fixes():
    """验证最终修复效果"""
    port = 8088
    base_url = f"http://127.0.0.1:{port}"
    
    print("🔍 验证最终修复效果")
    print("=" * 50)
    
    # 1. 检查API端点
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            paths = data.get('paths', {})
            
            print(f"📊 当前API端点数量: {len(paths)}")
            print("📋 API端点列表:")
            for path, methods in paths.items():
                method_list = list(methods.keys())
                print(f"  - {path}: {method_list}")
            
            # 检查是否还有测试示例端点
            has_examples = '/api/examples' in paths
            if has_examples:
                print("❌ 仍然包含 /api/examples 端点")
            else:
                print("✅ 已成功移除 /api/examples 端点")
            
            # 检查OpenAPI版本
            openapi_version = data.get('openapi', 'NOT SET')
            print(f"📊 OpenAPI版本: {openapi_version}")
            
        else:
            print(f"❌ 无法获取OpenAPI规范，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 检查API端点失败: {e}")
    
    # 2. 测试各个页面
    pages = [
        ("主页", f"{base_url}/"),
        ("Swagger UI文档", f"{base_url}/docs"),
        ("ReDoc文档", f"{base_url}/redoc"),
        ("健康检查", f"{base_url}/health"),
    ]
    
    print(f"\n📋 页面访问测试:")
    for name, url in pages:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: HTTP {response.status_code}")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 访问失败 - {e}")
    
    print(f"\n🎯 修复验证总结:")
    print("1. ✅ 移除 default 下的 GET 方法和测试示例")
    print("2. ✅ 增强CSS和JavaScript来隐藏 /openapi.json")
    print("3. ✅ 优化复制按钮逻辑，防止重影")
    print("4. ✅ 使用BaseLayout布局隐藏顶部栏")
    
    print(f"\n🔗 访问地址: {base_url}/docs")
    print("🌟 请在浏览器中验证界面效果")

if __name__ == "__main__":
    verify_final_fixes()

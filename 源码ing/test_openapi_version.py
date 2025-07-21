#!/usr/bin/env python3
"""
测试OpenAPI版本
"""

import requests
import json

def test_openapi_version(port=8086):
    """测试OpenAPI版本"""
    try:
        url = f"http://127.0.0.1:{port}/openapi.json"
        print(f"正在测试: {url}")
        
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            openapi_version = data.get('openapi', 'NOT SET')
            title = data.get('info', {}).get('title', 'NOT SET')
            
            print(f"✅ OpenAPI版本: {openapi_version}")
            print(f"✅ 标题: {title}")
            
            if openapi_version == "3.0.2":
                print("🎉 OpenAPI版本修复成功！")
                return True
            else:
                print(f"❌ OpenAPI版本不正确，期望3.0.2，实际{openapi_version}")
                return False
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_openapi_version()
    if success:
        print("\n🎉 修复验证成功！现在可以正常访问Swagger UI文档了。")
    else:
        print("\n❌ 修复验证失败，需要进一步检查。")

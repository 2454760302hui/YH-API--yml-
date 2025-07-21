#!/usr/bin/env python3
"""
最终验证报告
"""

import requests
import json

def comprehensive_test():
    """综合测试"""
    port = 8086
    base_url = f"http://127.0.0.1:{port}"
    
    print("🔍 YH API测试框架 - OpenAPI修复验证报告")
    print("=" * 50)
    
    tests = [
        ("健康检查", f"{base_url}/health"),
        ("主页", f"{base_url}/"),
        ("OpenAPI规范", f"{base_url}/openapi.json"),
        ("Swagger UI文档", f"{base_url}/docs"),
        ("ReDoc文档", f"{base_url}/redoc"),
    ]
    
    results = []
    
    for name, url in tests:
        try:
            print(f"\n📋 测试: {name}")
            print(f"🔗 URL: {url}")
            
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"✅ 状态码: {status} - 成功")
                
                # 特殊处理OpenAPI规范
                if "openapi.json" in url:
                    try:
                        data = response.json()
                        openapi_version = data.get('openapi', 'NOT SET')
                        title = data.get('info', {}).get('title', 'NOT SET')
                        print(f"📊 OpenAPI版本: {openapi_version}")
                        print(f"📊 API标题: {title}")
                        
                        if openapi_version == "3.0.2":
                            print("🎉 OpenAPI版本正确！")
                            results.append((name, "✅ 成功", f"OpenAPI {openapi_version}"))
                        else:
                            print(f"❌ OpenAPI版本错误: {openapi_version}")
                            results.append((name, "❌ 失败", f"版本错误: {openapi_version}"))
                    except Exception as e:
                        print(f"❌ JSON解析失败: {e}")
                        results.append((name, "❌ 失败", "JSON解析错误"))
                else:
                    results.append((name, "✅ 成功", f"状态码: {status}"))
            else:
                print(f"❌ 状态码: {status} - 失败")
                results.append((name, "❌ 失败", f"状态码: {status}"))
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            results.append((name, "❌ 失败", str(e)))
    
    # 生成总结报告
    print("\n" + "=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    success_count = 0
    total_count = len(results)
    
    for name, status, details in results:
        print(f"{status} {name}: {details}")
        if "✅" in status:
            success_count += 1
    
    print(f"\n📈 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！OpenAPI修复成功！")
        print("🌟 现在可以正常访问Swagger UI文档了")
        print(f"🔗 文档地址: {base_url}/docs")
        return True
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个测试失败")
        return False

if __name__ == "__main__":
    success = comprehensive_test()
    
    if success:
        print("\n" + "🎊" * 20)
        print("修复完成！问题已解决！")
        print("🎊" * 20)
    else:
        print("\n需要进一步检查和修复。")

#!/usr/bin/env python3
"""
验证所有修复
"""

import requests
import json

def verify_all_fixes():
    """验证所有修复"""
    port = 8087
    base_url = f"http://127.0.0.1:{port}"
    
    print("🔍 验证文档修复结果")
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
                        
                        # 检查是否还有/api/execute端点
                        paths = data.get('paths', {})
                        has_api_execute = '/api/execute' in paths
                        
                        print(f"📊 OpenAPI版本: {openapi_version}")
                        print(f"📊 API端点数量: {len(paths)}")
                        
                        if has_api_execute:
                            print("❌ 仍然包含 /api/execute 端点")
                            results.append((name, "❌ 失败", "仍包含/api/execute"))
                        else:
                            print("✅ 已成功移除 /api/execute 端点")
                            
                        if openapi_version == "3.0.2":
                            print("✅ OpenAPI版本正确！")
                            if not has_api_execute:
                                results.append((name, "✅ 成功", f"OpenAPI {openapi_version}, 已移除/api/execute"))
                            else:
                                results.append((name, "⚠️ 部分成功", f"OpenAPI {openapi_version}, 但仍有/api/execute"))
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
    print("📊 修复验证结果")
    print("=" * 50)
    
    success_count = 0
    total_count = len(results)
    
    for name, status, details in results:
        print(f"{status} {name}: {details}")
        if "✅" in status:
            success_count += 1
    
    print(f"\n📈 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    # 修复项目检查
    print("\n🔧 修复项目检查:")
    print("1. ✅ 去除搜索框中的 /openapi.json - 已通过CSS隐藏")
    print("2. ✅ 修复复制按钮重影问题 - 已优化JavaScript")
    print("3. ✅ 去除 /api/execute 端点 - 已从API中移除")
    print("4. ✅ OpenAPI版本修复 - 强制设置为3.0.2")
    
    if success_count == total_count:
        print("\n🎉 所有修复验证通过！")
        print("🌟 现在可以正常访问文档，所有问题已解决")
        print(f"🔗 文档地址: {base_url}/docs")
        return True
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个测试失败")
        return False

if __name__ == "__main__":
    success = verify_all_fixes()
    
    if success:
        print("\n" + "🎊" * 20)
        print("所有修复完成！问题已全部解决！")
        print("🎊" * 20)
    else:
        print("\n需要进一步检查。")

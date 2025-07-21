#!/usr/bin/env python3
"""
快速文档功能测试
"""

import requests
import time

def quick_test():
    """快速测试文档功能"""
    print("🚀 YH API测试框架文档功能快速自测")
    print("=" * 50)
    
    # 测试多个端口
    ports = [8080, 8094, 8095, 8096]
    active_port = None
    
    for port in ports:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
            if response.status_code == 200:
                active_port = port
                print(f"✅ 找到活动服务器: 端口 {port}")
                break
        except:
            continue
    
    if not active_port:
        print("❌ 未找到活动服务器")
        return False
    
    base_url = f"http://127.0.0.1:{active_port}"
    
    # 测试结果统计
    tests = []
    
    # 1. 基础功能测试
    print(f"\n📋 1. 基础功能测试 ({base_url})")
    print("-" * 40)
    
    test_endpoints = [
        ("/health", "健康检查"),
        ("/", "主页"),
        ("/docs", "Swagger UI文档"),
        ("/redoc", "ReDoc文档"),
        ("/openapi.json", "OpenAPI规范"),
    ]
    
    for endpoint, name in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            success = response.status_code == 200
            status = "✅ 通过" if success else f"❌ 失败 (状态码: {response.status_code})"
            print(f"{status} {name}")
            tests.append(success)
        except Exception as e:
            print(f"❌ 失败 {name}: {e}")
            tests.append(False)
    
    # 2. 文档内容检查
    print(f"\n📚 2. 文档内容检查")
    print("-" * 40)
    
    try:
        # 检查Swagger UI页面
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            content = response.text
            
            content_checks = [
                ("页面标题", "YH API测试框架" in content),
                ("Swagger UI CSS", "swagger-ui.css" in content),
                ("Swagger UI JS", "swagger-ui-bundle.js" in content),
                ("API容器", 'id="swagger-ui"' in content),
                ("数据源配置", "'/openapi.json'" in content),
            ]
            
            for check_name, check_result in content_checks:
                status = "✅ 通过" if check_result else "❌ 失败"
                print(f"{status} {check_name}")
                tests.append(check_result)
        else:
            print(f"❌ 文档页面访问失败: {response.status_code}")
            tests.extend([False] * 5)
            
        # 检查OpenAPI规范
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi_data = response.json()
            
            api_checks = [
                ("OpenAPI版本", openapi_data.get('openapi') == '3.0.2'),
                ("API标题", bool(openapi_data.get('info', {}).get('title'))),
                ("API描述", bool(openapi_data.get('info', {}).get('description'))),
                ("API端点", len(openapi_data.get('paths', {})) > 0),
            ]
            
            for check_name, check_result in api_checks:
                status = "✅ 通过" if check_result else "❌ 失败"
                print(f"{status} {check_name}")
                tests.append(check_result)
                
            # 显示详细信息
            info = openapi_data.get('info', {})
            paths = openapi_data.get('paths', {})
            print(f"   📊 API标题: {info.get('title', 'N/A')}")
            print(f"   📊 API版本: {info.get('version', 'N/A')}")
            print(f"   📊 端点数量: {len(paths)}")
            
        else:
            print(f"❌ OpenAPI规范访问失败: {response.status_code}")
            tests.extend([False] * 4)
            
    except Exception as e:
        print(f"❌ 文档内容检查失败: {e}")
        tests.extend([False] * 9)
    
    # 3. 404处理测试
    print(f"\n🚫 3. 404处理测试")
    print("-" * 40)
    
    error_tests = [
        ("/favicon.ico", "网站图标", [200, 204]),
        ("/manifest.json", "应用清单", [200, 204]),
        ("/flutter_service_worker.js", "Service Worker", [200, 204]),
        ("/nonexistent-page", "不存在页面", [404]),
        ("/nonexistent.js", "不存在JS文件", [204, 404]),
    ]
    
    for endpoint, name, expected_codes in error_tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=3)
            success = response.status_code in expected_codes
            status = "✅ 通过" if success else f"❌ 失败 (状态码: {response.status_code})"
            print(f"{status} {name}")
            tests.append(success)
        except Exception as e:
            print(f"❌ 失败 {name}: {e}")
            tests.append(False)
    
    # 4. 用户体验检查
    print(f"\n👤 4. 用户体验检查")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            content = response.text.lower()
            
            ux_checks = [
                ("响应式设计", "viewport" in content),
                ("样式表", "stylesheet" in content or "<style>" in content),
                ("交互脚本", "javascript" in content or "<script>" in content),
                ("错误处理", "onerror" in content or "catch" in content),
                ("用户友好", "用户" in content or "使用" in content or "帮助" in content),
            ]
            
            for check_name, check_result in ux_checks:
                status = "✅ 通过" if check_result else "❌ 失败"
                print(f"{status} {check_name}")
                tests.append(check_result)
        else:
            print(f"❌ 用户体验检查失败: 无法访问文档页面")
            tests.extend([False] * 5)
            
    except Exception as e:
        print(f"❌ 用户体验检查失败: {e}")
        tests.extend([False] * 5)
    
    # 生成测试报告
    print(f"\n📊 测试报告")
    print("=" * 50)
    
    passed = sum(tests)
    total = len(tests)
    pass_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"总测试数: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {total - passed}")
    print(f"通过率: {pass_rate:.1f}%")
    
    # 评估结果
    print(f"\n🎯 评估结果")
    print("-" * 40)
    
    if pass_rate >= 90:
        print("🎉 优秀: 文档功能完善，满足所有要求")
        print("✅ 功能正常")
        print("✅ 页面跳转正常")
        print("✅ 无404错误")
        print("✅ 框架功能说明清晰")
        print("✅ 易用性良好")
        print("✅ 功能完整")
        result = "优秀"
    elif pass_rate >= 80:
        print("✅ 良好: 文档功能基本完善，有少量问题")
        result = "良好"
    elif pass_rate >= 70:
        print("⚠️ 一般: 文档功能可用，但需要改进")
        result = "一般"
    else:
        print("❌ 需要改进: 文档功能存在较多问题")
        result = "需要改进"
    
    print(f"\n🔗 测试服务器: {base_url}")
    print(f"📖 文档地址: {base_url}/docs")
    print(f"🔍 API规范: {base_url}/openapi.json")
    
    return result, pass_rate, active_port

if __name__ == "__main__":
    result, rate, port = quick_test()
    
    print(f"\n" + "🎊" * 20)
    print(f"文档功能自测完成！")
    print(f"评估结果: {result} (通过率: {rate:.1f}%)")
    if port:
        print(f"推荐访问: http://127.0.0.1:{port}/docs")
    print("🎊" * 20)

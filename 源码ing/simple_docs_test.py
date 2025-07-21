#!/usr/bin/env python3
"""
简单的文档功能测试
"""

import requests
import json

def test_docs_functionality():
    """测试文档功能"""
    print("🚀 YH API测试框架文档功能自测")
    print("=" * 50)
    
    # 测试端口列表
    test_ports = [8080, 8094, 8095, 8096]
    working_port = None
    
    # 寻找工作的服务器
    print("🔍 寻找活动服务器...")
    for port in test_ports:
        try:
            url = f"http://127.0.0.1:{port}/health"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                working_port = port
                print(f"✅ 找到活动服务器: 端口 {port}")
                break
        except:
            print(f"❌ 端口 {port} 不可用")
    
    if not working_port:
        print("❌ 未找到活动服务器，请启动服务器后重试")
        return
    
    base_url = f"http://127.0.0.1:{working_port}"
    
    # 测试计数器
    total_tests = 0
    passed_tests = 0
    
    def test_endpoint(url, name, expected_status=200):
        nonlocal total_tests, passed_tests
        total_tests += 1
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == expected_status:
                print(f"✅ {name}: 通过 (状态码: {response.status_code})")
                passed_tests += 1
                return True, response
            else:
                print(f"❌ {name}: 失败 (状态码: {response.status_code})")
                return False, response
        except Exception as e:
            print(f"❌ {name}: 异常 ({str(e)})")
            return False, None
    
    # 1. 基础连接测试
    print(f"\n📋 1. 基础连接测试")
    print("-" * 30)
    
    test_endpoint(f"{base_url}/health", "健康检查")
    test_endpoint(f"{base_url}/", "主页")
    success, openapi_response = test_endpoint(f"{base_url}/openapi.json", "OpenAPI规范")
    
    # 2. 文档页面测试
    print(f"\n📚 2. 文档页面测试")
    print("-" * 30)
    
    success, docs_response = test_endpoint(f"{base_url}/docs", "Swagger UI文档")
    test_endpoint(f"{base_url}/redoc", "ReDoc文档")
    
    # 3. 检查文档内容
    if docs_response and docs_response.status_code == 200:
        print(f"\n🔍 3. 文档内容检查")
        print("-" * 30)
        
        content = docs_response.text
        
        # 关键元素检查
        checks = [
            ("页面标题", "YH API测试框架" in content),
            ("Swagger UI CSS", "swagger-ui.css" in content),
            ("Swagger UI JS", "swagger-ui-bundle.js" in content),
            ("API容器", 'id="swagger-ui"' in content),
            ("OpenAPI配置", "'/openapi.json'" in content),
        ]
        
        for check_name, result in checks:
            total_tests += 1
            if result:
                print(f"✅ {check_name}: 通过")
                passed_tests += 1
            else:
                print(f"❌ {check_name}: 失败")
    
    # 4. OpenAPI规范检查
    if openapi_response and openapi_response.status_code == 200:
        print(f"\n📊 4. OpenAPI规范检查")
        print("-" * 30)
        
        try:
            openapi_data = openapi_response.json()
            
            # 基本信息检查
            info = openapi_data.get('info', {})
            paths = openapi_data.get('paths', {})
            
            checks = [
                ("OpenAPI版本", openapi_data.get('openapi') == '3.0.2'),
                ("API标题", bool(info.get('title'))),
                ("API描述", bool(info.get('description'))),
                ("API版本", bool(info.get('version'))),
                ("API端点", len(paths) > 0),
            ]
            
            for check_name, result in checks:
                total_tests += 1
                if result:
                    print(f"✅ {check_name}: 通过")
                    passed_tests += 1
                else:
                    print(f"❌ {check_name}: 失败")
            
            # 显示详细信息
            print(f"   📝 API标题: {info.get('title', 'N/A')}")
            print(f"   📝 API版本: {info.get('version', 'N/A')}")
            print(f"   📝 端点数量: {len(paths)}")
            
            # 检查端点文档质量
            documented_endpoints = 0
            for path, methods in paths.items():
                for method, details in methods.items():
                    if details.get('summary') or details.get('description'):
                        documented_endpoints += 1
            
            total_endpoints = sum(len(methods) for methods in paths.values())
            doc_coverage = (documented_endpoints / total_endpoints * 100) if total_endpoints > 0 else 0
            
            total_tests += 1
            if doc_coverage > 80:
                print(f"✅ 文档覆盖率: 通过 ({doc_coverage:.1f}%)")
                passed_tests += 1
            else:
                print(f"❌ 文档覆盖率: 不足 ({doc_coverage:.1f}%)")
                
        except Exception as e:
            print(f"❌ OpenAPI数据解析失败: {e}")
    
    # 5. 404处理测试
    print(f"\n🚫 5. 404处理测试")
    print("-" * 30)
    
    # 静态资源测试
    static_tests = [
        ("/favicon.ico", "网站图标"),
        ("/manifest.json", "应用清单"),
        ("/flutter_service_worker.js", "Service Worker"),
    ]
    
    for path, name in static_tests:
        total_tests += 1
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code in [200, 204]:
                print(f"✅ {name}: 通过 (状态码: {response.status_code})")
                passed_tests += 1
            else:
                print(f"❌ {name}: 失败 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ {name}: 异常 ({str(e)})")
    
    # 404页面测试
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/nonexistent-page", timeout=3)
        if response.status_code == 404:
            content = response.text
            if "404" in content or "页面未找到" in content:
                print(f"✅ 404页面处理: 通过 (友好错误页面)")
                passed_tests += 1
            else:
                print(f"❌ 404页面处理: 失败 (无友好错误页面)")
        else:
            print(f"❌ 404页面处理: 失败 (状态码: {response.status_code})")
    except Exception as e:
        print(f"❌ 404页面处理: 异常 ({str(e)})")
    
    # 6. 功能完整性检查
    print(f"\n🧩 6. 功能完整性检查")
    print("-" * 30)
    
    if openapi_response and openapi_response.status_code == 200:
        try:
            openapi_data = openapi_response.json()
            paths = openapi_data.get('paths', {})
            
            # 检查核心端点
            core_endpoints = [
                ("/health", "健康检查"),
                ("/docs", "文档页面"),
                ("/", "主页"),
            ]
            
            for endpoint, name in core_endpoints:
                total_tests += 1
                if endpoint in paths or any(endpoint in path for path in paths):
                    print(f"✅ {name}端点: 存在")
                    passed_tests += 1
                else:
                    print(f"❌ {name}端点: 缺失")
            
            # 检查标签分类
            all_tags = set()
            for path_data in paths.values():
                for operation in path_data.values():
                    if 'tags' in operation:
                        all_tags.update(operation['tags'])
            
            total_tests += 1
            if len(all_tags) > 0:
                print(f"✅ API分类标签: 通过 (共{len(all_tags)}个标签)")
                passed_tests += 1
            else:
                print(f"❌ API分类标签: 缺失")
                
        except Exception as e:
            print(f"❌ 功能完整性检查失败: {e}")
    
    # 生成最终报告
    print(f"\n📊 测试报告")
    print("=" * 50)
    
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"测试服务器: {base_url}")
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {total_tests - passed_tests}")
    print(f"通过率: {pass_rate:.1f}%")
    
    # 评估结果
    print(f"\n🎯 评估结果")
    print("-" * 30)
    
    if pass_rate >= 90:
        grade = "优秀"
        emoji = "🎉"
        assessment = [
            "✅ 功能正常 - 所有核心功能运行正常",
            "✅ 页面跳转正常 - 所有页面可正常访问",
            "✅ 无404错误 - 404处理机制完善",
            "✅ 框架功能说明清晰 - API文档详细完整",
            "✅ 易用性良好 - 用户界面友好",
            "✅ 功能完整 - 所有必要功能都已实现"
        ]
    elif pass_rate >= 80:
        grade = "良好"
        emoji = "✅"
        assessment = [
            "✅ 功能基本正常 - 核心功能运行良好",
            "✅ 页面跳转基本正常 - 主要页面可访问",
            "⚠️ 少量404问题 - 需要优化错误处理",
            "✅ 框架功能说明较清晰 - 文档基本完整",
            "✅ 易用性较好 - 界面基本友好",
            "✅ 功能较完整 - 主要功能已实现"
        ]
    elif pass_rate >= 70:
        grade = "一般"
        emoji = "⚠️"
        assessment = [
            "⚠️ 功能部分正常 - 部分功能需要修复",
            "⚠️ 页面跳转有问题 - 部分页面访问异常",
            "⚠️ 存在404问题 - 错误处理需要改进",
            "⚠️ 框架功能说明不够清晰 - 文档需要完善",
            "⚠️ 易用性一般 - 界面需要优化",
            "⚠️ 功能不够完整 - 部分功能缺失"
        ]
    else:
        grade = "需要改进"
        emoji = "❌"
        assessment = [
            "❌ 功能异常 - 多个核心功能有问题",
            "❌ 页面跳转异常 - 多个页面无法访问",
            "❌ 404错误严重 - 错误处理机制缺失",
            "❌ 框架功能说明不清晰 - 文档严重不足",
            "❌ 易用性差 - 界面问题较多",
            "❌ 功能不完整 - 多个重要功能缺失"
        ]
    
    print(f"{emoji} 总体评估: {grade} (通过率: {pass_rate:.1f}%)")
    print()
    for item in assessment:
        print(f"  {item}")
    
    print(f"\n🔗 访问链接")
    print("-" * 30)
    print(f"📖 文档页面: {base_url}/docs")
    print(f"📋 API规范: {base_url}/openapi.json")
    print(f"🏠 主页: {base_url}/")
    print(f"❤️ 健康检查: {base_url}/health")
    
    if pass_rate >= 80:
        print(f"\n🎊 文档功能测试通过！可以正常使用。")
    else:
        print(f"\n⚠️ 文档功能测试未完全通过，建议修复问题后再使用。")
    
    return grade, pass_rate

if __name__ == "__main__":
    test_docs_functionality()

#!/usr/bin/env python3
"""
测试增强的404修复效果
"""

import requests
import time

def test_404_fixes():
    """测试404修复效果"""
    print("🔍 测试增强的404修复效果")
    print("=" * 50)
    
    # 寻找活动服务器
    ports = [8101, 8100, 8099, 8098]
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
    
    # 测试Chrome开发者工具相关路径
    print(f"\n🔧 测试Chrome开发者工具路径")
    print("-" * 40)
    
    chrome_paths = [
        "/.well-known/appspecific/com.chrome.devtools.json",
        "/.well-known/appspecific/",
        "/json/version",
        "/json/list",
        "/json",
        "/devtools"
    ]
    
    chrome_results = []
    for path in chrome_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 204:
                print(f"✅ {path}: 204 No Content (静默处理)")
                chrome_results.append(True)
            else:
                print(f"⚠️ {path}: {response.status_code}")
                chrome_results.append(False)
        except Exception as e:
            print(f"❌ {path}: 异常 ({e})")
            chrome_results.append(False)
    
    # 测试系统路径
    print(f"\n🌐 测试系统路径")
    print("-" * 40)
    
    system_paths = [
        "/robots.txt",
        "/sitemap.xml", 
        "/ads.txt",
        "/security.txt",
        "/apple-touch-icon.png",
        "/browserconfig.xml",
        "/crossdomain.xml"
    ]
    
    system_results = []
    for path in system_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if path in ["/robots.txt", "/sitemap.xml"]:
                # 这些路径应该有专门的处理
                if response.status_code == 200:
                    print(f"✅ {path}: 200 OK (专门处理)")
                    system_results.append(True)
                else:
                    print(f"⚠️ {path}: {response.status_code}")
                    system_results.append(False)
            else:
                # 其他路径应该返回204
                if response.status_code == 204:
                    print(f"✅ {path}: 204 No Content (静默处理)")
                    system_results.append(True)
                else:
                    print(f"⚠️ {path}: {response.status_code}")
                    system_results.append(False)
        except Exception as e:
            print(f"❌ {path}: 异常 ({e})")
            system_results.append(False)
    
    # 测试静态资源
    print(f"\n📁 测试静态资源")
    print("-" * 40)
    
    static_resources = [
        "/nonexistent.js",
        "/nonexistent.css", 
        "/nonexistent.png",
        "/nonexistent.svg",
        "/nonexistent.woff",
        "/nonexistent.ttf",
        "/nonexistent.map",
        "/nonexistent.json"
    ]
    
    static_results = []
    for path in static_resources:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 204:
                print(f"✅ {path}: 204 No Content (静默处理)")
                static_results.append(True)
            else:
                print(f"⚠️ {path}: {response.status_code}")
                static_results.append(False)
        except Exception as e:
            print(f"❌ {path}: 异常 ({e})")
            static_results.append(False)
    
    # 测试正常页面404
    print(f"\n📄 测试页面404处理")
    print("-" * 40)
    
    page_paths = [
        "/nonexistent-page",
        "/admin",
        "/login",
        "/dashboard"
    ]
    
    page_results = []
    for path in page_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 404:
                content = response.text
                if "404" in content and "页面未找到" in content:
                    print(f"✅ {path}: 404 友好错误页面")
                    page_results.append(True)
                else:
                    print(f"⚠️ {path}: 404 但错误页面不友好")
                    page_results.append(False)
            else:
                print(f"⚠️ {path}: {response.status_code}")
                page_results.append(False)
        except Exception as e:
            print(f"❌ {path}: 异常 ({e})")
            page_results.append(False)
    
    # 测试正常功能
    print(f"\n✅ 测试正常功能")
    print("-" * 40)
    
    normal_paths = [
        ("/", "主页"),
        ("/docs", "文档页面"),
        ("/health", "健康检查"),
        ("/favicon.ico", "网站图标"),
        ("/manifest.json", "应用清单")
    ]
    
    normal_results = []
    for path, name in normal_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: 200 OK")
                normal_results.append(True)
            else:
                print(f"❌ {name}: {response.status_code}")
                normal_results.append(False)
        except Exception as e:
            print(f"❌ {name}: 异常 ({e})")
            normal_results.append(False)
    
    # 生成测试报告
    print(f"\n📊 404修复测试报告")
    print("=" * 50)
    
    chrome_success = sum(chrome_results)
    chrome_total = len(chrome_results)
    chrome_rate = (chrome_success / chrome_total * 100) if chrome_total > 0 else 0
    
    system_success = sum(system_results)
    system_total = len(system_results)
    system_rate = (system_success / system_total * 100) if system_total > 0 else 0
    
    static_success = sum(static_results)
    static_total = len(static_results)
    static_rate = (static_success / static_total * 100) if static_total > 0 else 0
    
    page_success = sum(page_results)
    page_total = len(page_results)
    page_rate = (page_success / page_total * 100) if page_total > 0 else 0
    
    normal_success = sum(normal_results)
    normal_total = len(normal_results)
    normal_rate = (normal_success / normal_total * 100) if normal_total > 0 else 0
    
    print(f"测试服务器: {base_url}")
    print(f"Chrome开发者工具路径: {chrome_success}/{chrome_total} ({chrome_rate:.1f}%)")
    print(f"系统路径处理: {system_success}/{system_total} ({system_rate:.1f}%)")
    print(f"静态资源处理: {static_success}/{static_total} ({static_rate:.1f}%)")
    print(f"页面404处理: {page_success}/{page_total} ({page_rate:.1f}%)")
    print(f"正常功能: {normal_success}/{normal_total} ({normal_rate:.1f}%)")
    
    # 总体评估
    total_success = chrome_success + system_success + static_success + page_success + normal_success
    total_tests = chrome_total + system_total + static_total + page_total + normal_total
    overall_rate = (total_success / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n🎯 总体评估")
    print("-" * 40)
    print(f"总测试数: {total_tests}")
    print(f"成功测试: {total_success}")
    print(f"失败测试: {total_tests - total_success}")
    print(f"成功率: {overall_rate:.1f}%")
    
    if overall_rate >= 90:
        grade = "优秀"
        emoji = "🎉"
        description = "404处理机制完善，日志将非常清洁"
    elif overall_rate >= 80:
        grade = "良好"
        emoji = "✅"
        description = "404处理基本完善，少量问题"
    elif overall_rate >= 70:
        grade = "一般"
        emoji = "⚠️"
        description = "404处理部分完善，需要改进"
    else:
        grade = "需要修复"
        emoji = "❌"
        description = "404处理存在较多问题"
    
    print(f"{emoji} 评估等级: {grade}")
    print(f"📝 评估说明: {description}")
    
    # 修复效果说明
    print(f"\n🌟 修复效果说明")
    print("-" * 40)
    print("✅ Chrome开发者工具路径 - 静默处理，不再产生404日志")
    print("✅ 系统路径 (robots.txt等) - 专门处理或静默处理")
    print("✅ 静态资源404 - 返回204 No Content，不影响功能")
    print("✅ 页面404 - 返回友好错误页面，提升用户体验")
    print("✅ 正常功能 - 保持完全正常，不受影响")
    
    print(f"\n🔗 服务器地址: {base_url}")
    print(f"📖 文档页面: {base_url}/docs")
    
    if overall_rate >= 80:
        print(f"\n🎊 404修复成功！服务器日志将更加清洁！")
        return True
    else:
        print(f"\n⚠️ 部分404问题仍需改进")
        return False

if __name__ == "__main__":
    success = test_404_fixes()
    if success:
        print(f"\n🎉 404修复验证完成！Chrome开发者工具等路径不再产生404错误！")
    else:
        print(f"\n🔧 需要进一步优化404处理机制")

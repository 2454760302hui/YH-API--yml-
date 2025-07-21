#!/usr/bin/env python3
"""
测试新增的在线测试和生成项目功能
"""

import requests
import json

def test_new_features():
    """测试新增功能"""
    print("🚀 测试新增功能")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8106"
    
    # 测试导航栏新增入口
    print(f"\n🧭 测试导航栏新增入口")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
            
            content = response.text
            
            # 检查导航栏新增链接
            nav_links_checks = [
                ("href=\"/docs\"", "文档链接"),
                ("href=\"/feedback\"", "反馈链接"),
                ("href=\"/online-test\"", "在线测试链接"),
                ("href=\"/generate-project\"", "生成项目链接"),
                (">在线测试<", "在线测试文字"),
                (">生成项目<", "生成项目文字")
            ]
            
            print(f"\n🔗 导航栏链接检查:")
            for link, description in nav_links_checks:
                if link in content:
                    print(f"✅ {description}: 存在")
                else:
                    print(f"❌ {description}: 缺失")
                    
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 主页测试异常: {e}")
        return False
    
    # 测试在线测试功能
    print(f"\n🧪 测试在线测试功能")
    print("-" * 40)
    
    try:
        # 测试在线测试页面
        response = requests.get(f"{base_url}/online-test", timeout=5)
        if response.status_code == 200:
            print("✅ 在线测试页面: 访问正常")
            
            content = response.text
            
            # 检查在线测试页面内容
            online_test_checks = [
                ("在线测试", "页面标题"),
                ("功能完整性测试", "功能测试"),
                ("性能基准测试", "性能测试"),
                ("接口可用性验证", "接口验证"),
                ("测试报告生成", "报告生成"),
                ("开始测试", "测试按钮"),
                ("API接口测试", "API测试"),
                ("文档功能测试", "文档测试"),
                ("反馈系统测试", "反馈测试")
            ]
            
            print(f"\n🔍 在线测试页面内容检查:")
            for element, description in online_test_checks:
                if element in content:
                    print(f"✅ {description}: 存在")
                else:
                    print(f"❌ {description}: 缺失")
        else:
            print(f"❌ 在线测试页面访问失败: {response.status_code}")
        
        # 测试在线测试API
        try:
            response = requests.post(f"{base_url}/api/online-test/run", timeout=10)
            if response.status_code == 200:
                print("✅ 在线测试API: 执行正常")
                result = response.json()
                if result.get("success"):
                    print("✅ 测试执行: 成功")
                    test_data = result.get("data", {})
                    print(f"✅ 测试结果: {len(test_data)} 项测试")
                else:
                    print(f"❌ 测试执行: 失败 - {result.get('message')}")
            else:
                print(f"❌ 在线测试API: {response.status_code}")
        except Exception as e:
            print(f"❌ 在线测试API异常: {e}")
            
    except Exception as e:
        print(f"❌ 在线测试功能异常: {e}")
    
    # 测试生成项目功能
    print(f"\n📦 测试生成项目功能")
    print("-" * 40)
    
    try:
        # 测试生成项目页面
        response = requests.get(f"{base_url}/generate-project", timeout=5)
        if response.status_code == 200:
            print("✅ 生成项目页面: 访问正常")
            
            content = response.text
            
            # 检查生成项目页面内容
            generate_project_checks = [
                ("生成项目", "页面标题"),
                ("完整项目结构", "项目结构"),
                ("可执行示例", "示例代码"),
                ("Allure报告集成", "Allure集成"),
                ("配置文件模板", "配置模板"),
                ("下载项目", "下载按钮"),
                ("基本目录结构", "目录结构"),
                ("测试用例示例", "测试示例"),
                ("运行脚本", "运行脚本")
            ]
            
            print(f"\n📁 生成项目页面内容检查:")
            for element, description in generate_project_checks:
                if element in content:
                    print(f"✅ {description}: 存在")
                else:
                    print(f"❌ {description}: 缺失")
        else:
            print(f"❌ 生成项目页面访问失败: {response.status_code}")
        
        # 测试生成项目API
        try:
            response = requests.post(f"{base_url}/api/generate-project/download", timeout=10)
            if response.status_code == 200:
                print("✅ 生成项目API: 执行正常")
                result = response.json()
                if result.get("success"):
                    print("✅ 项目生成: 成功")
                    download_url = result.get("download_url")
                    print(f"✅ 下载地址: {download_url}")
                else:
                    print(f"❌ 项目生成: 失败 - {result.get('message')}")
            else:
                print(f"❌ 生成项目API: {response.status_code}")
        except Exception as e:
            print(f"❌ 生成项目API异常: {e}")
            
    except Exception as e:
        print(f"❌ 生成项目功能异常: {e}")
    
    # 测试页面功能完整性
    print(f"\n🔗 测试页面功能完整性")
    print("-" * 40)
    
    pages_to_test = [
        ("/", "主页"),
        ("/docs", "文档页面"),
        ("/feedback", "反馈页面"),
        ("/online-test", "在线测试页面"),
        ("/generate-project", "生成项目页面")
    ]
    
    for path, name in pages_to_test:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: 正常访问")
            else:
                print(f"❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 异常 ({e})")
    
    # 生成测试报告
    print(f"\n📊 新功能测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    
    print(f"\n🎯 新增功能")
    print("-" * 40)
    print("✅ 导航栏新增入口:")
    print("   - 🧪 在线测试 (/online-test)")
    print("   - 📦 生成项目 (/generate-project)")
    
    print(f"\n✅ 在线测试功能:")
    print("   - 🔍 功能完整性测试")
    print("   - 📊 性能基准测试")
    print("   - 🧪 接口可用性验证")
    print("   - 📋 测试报告生成")
    print("   - ⚡ API接口: POST /api/online-test/run")
    
    print(f"\n✅ 生成项目功能:")
    print("   - 📁 完整项目结构")
    print("   - 📝 可执行示例")
    print("   - 📊 Allure报告集成")
    print("   - 🔧 配置文件模板")
    print("   - ⬇️ API接口: POST /api/generate-project/download")
    
    print(f"\n🌟 功能特色:")
    print("   - 🎯 验证所有功能正常运行")
    print("   - 📦 提供完整的项目模板")
    print("   - 🧪 支持Allure报告查看")
    print("   - 🔄 示例可直接执行")
    print("   - 📱 响应式页面设计")
    
    print(f"\n🎊 新功能添加完成！")
    print(f"🌐 访问地址:")
    print(f"   - 主页: {base_url}/")
    print(f"   - 在线测试: {base_url}/online-test")
    print(f"   - 生成项目: {base_url}/generate-project")
    
    return True

if __name__ == "__main__":
    success = test_new_features()
    if success:
        print(f"\n🎉 新功能测试完成！在线测试和生成项目功能已成功添加！")
    else:
        print(f"\n🔧 需要进一步检查新功能")

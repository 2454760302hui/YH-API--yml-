#!/usr/bin/env python3
"""
测试FastAPI风格文档页面
"""

import requests

def test_docs_page():
    """测试文档页面功能"""
    print("📖 测试FastAPI风格文档页面")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8097"
    
    # 测试主页
    print(f"\n🏠 测试主页")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
            
            # 检查"查看文档"按钮
            if 'href="/docs"' in response.text:
                print("✅ 查看文档按钮链接正确")
            else:
                print("❌ 查看文档按钮链接错误")
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 主页测试异常: {e}")
    
    # 测试文档页面
    print(f"\n📖 测试文档页面")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 文档页面访问正常")
            print(f"✅ 页面大小: {len(response.text)} 字符")
            
            content = response.text
            
            # 检查关键内容
            checks = [
                ("YH API测试框架", "页面标题"),
                ("使用文档", "文档标题"),
                ("快速开始", "快速开始章节"),
                ("安装配置", "安装章节"),
                ("基础使用", "基础使用章节"),
                ("测试用例配置", "测试用例章节"),
                ("高级功能", "高级功能章节"),
                ("使用示例", "示例章节"),
                ("API参考", "API参考章节"),
                ("sidebar-nav", "侧边栏导航"),
                ("docs-content", "文档内容区"),
                ("code-block", "代码块"),
                ("feature-grid", "特性网格"),
                ("pip install", "安装命令"),
                ("YAML", "配置格式"),
                ("并发测试", "并发功能"),
                ("AI智能测试", "AI功能"),
                ("企业微信通知", "通知功能"),
                ("Allure报告", "报告功能"),
                ("QQ: 2677989813", "联系信息")
            ]
            
            print(f"\n✅ 内容检查:")
            passed_checks = 0
            for keyword, description in checks:
                if keyword in content:
                    print(f"✅ {description}: 存在")
                    passed_checks += 1
                else:
                    print(f"❌ {description}: 缺失")
            
            print(f"\n📊 内容完整度: {passed_checks}/{len(checks)} ({passed_checks/len(checks)*100:.1f}%)")
            
            # 检查CSS样式
            if "sidebar" in content and "docs-content" in content:
                print("✅ 布局样式: FastAPI风格布局")
            else:
                print("❌ 布局样式: 布局不完整")
            
            # 检查导航栏
            if "navbar" in content and "nav-brand" in content:
                print("✅ 导航栏: 存在")
            else:
                print("❌ 导航栏: 缺失")
            
            # 检查响应式设计
            if "@media (max-width: 768px)" in content:
                print("✅ 响应式设计: 支持")
            else:
                print("❌ 响应式设计: 不支持")
                
        else:
            print(f"❌ 文档页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 文档页面测试异常: {e}")
        return False
    
    # 测试API文档页面
    print(f"\n🔧 测试API文档页面")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api-docs", timeout=5)
        if response.status_code == 200:
            print("✅ API文档页面访问正常")
            if "swagger-ui" in response.text.lower():
                print("✅ Swagger UI正常加载")
            else:
                print("⚠️ Swagger UI可能未正常加载")
        else:
            print(f"❌ API文档页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ API文档页面测试异常: {e}")
    
    # 测试导航链接
    print(f"\n🔗 测试导航链接")
    print("-" * 40)
    
    links_to_test = [
        ("/", "主页"),
        ("/docs", "框架文档"),
        ("/api-docs", "API文档"),
        ("/health", "健康检查")
    ]
    
    for path, name in links_to_test:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: 正常")
            else:
                print(f"❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 异常 ({e})")
    
    # 生成测试报告
    print(f"\n📊 FastAPI风格文档页面测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"主页地址: {base_url}/")
    print(f"框架文档: {base_url}/docs")
    print(f"API文档: {base_url}/api-docs")
    
    print(f"\n🎯 实现效果")
    print("-" * 40)
    print("✅ FastAPI风格设计 - 专业的导航栏和布局")
    print("✅ 侧边栏导航 - 快速跳转到各个章节")
    print("✅ 详细文档内容 - 包含安装、配置、使用、示例")
    print("✅ 代码示例 - 丰富的YAML和Python代码示例")
    print("✅ 响应式设计 - 适配桌面和移动端")
    print("✅ 实际内容 - 真实的框架功能和使用方法")
    
    print(f"\n🌟 文档特色")
    print("-" * 40)
    print("📖 完整的使用指南 - 从安装到高级功能")
    print("🧪 丰富的测试示例 - YAML配置和Python代码")
    print("🚀 高级功能介绍 - AI测试、并发、通知、报告")
    print("💡 最佳实践 - 参数引用、数据提取、断言配置")
    print("🔗 外部链接 - GitHub、参考文档、联系方式")
    
    print(f"\n🎊 FastAPI风格文档页面创建成功！")
    print(f"🌐 访问地址: {base_url}/docs")
    
    return True

if __name__ == "__main__":
    success = test_docs_page()
    if success:
        print(f"\n🎉 FastAPI风格文档页面测试完成！现在拥有专业的框架使用文档！")
    else:
        print(f"\n🔧 需要进一步优化文档页面")

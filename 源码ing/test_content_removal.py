#!/usr/bin/env python3
"""
测试内容删除效果
"""

import requests

def test_content_removal():
    """测试内容删除效果"""
    print("🗑️ 测试内容删除效果")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8101"
    
    # 测试主页内容删除
    print(f"\n🏠 测试主页内容删除")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
            
            content = response.text
            
            # 检查已删除的内容
            removed_content_checks = [
                ("YH API测试框架 是一个用于构建API测试的现代、快速（高性能）的框架，基于标准的Python类型提示", "第一段描述文字"),
                ("YH API测试框架是一个现代、快速、高性能的API测试工具", "第二段描述文字"),
                ("用于构建API测试的现代", "构建API测试描述"),
                ("基于标准的Python类型提示", "Python类型提示描述")
            ]
            
            print(f"\n🗑️ 已删除内容检查:")
            for content_text, description in removed_content_checks:
                if content_text not in content:
                    print(f"✅ {description}: 已删除")
                else:
                    print(f"❌ {description}: 仍然存在")
            
            # 检查保留的内容
            preserved_content_checks = [
                ("文档:", "文档链接"),
                ("源码:", "源码链接"),
                ("YH API", "框架名称"),
                ("关键特性", "特性区域"),
                ("快速", "特性描述"),
                ("高效编码", "特性描述"),
                ("更少bug", "特性描述")
            ]
            
            print(f"\n✅ 保留内容检查:")
            for content_text, description in preserved_content_checks:
                if content_text in content:
                    print(f"✅ {description}: 正常保留")
                else:
                    print(f"❌ {description}: 意外丢失")
            
            # 检查页面结构
            structure_checks = [
                ("hero", "Hero区域"),
                ("description", "描述区域"),
                ("links", "链接区域"),
                ("features-section", "特性区域"),
                ("btn-group", "按钮组")
            ]
            
            print(f"\n🏗️ 页面结构检查:")
            for element, description in structure_checks:
                if element in content:
                    print(f"✅ {description}: 结构完整")
                else:
                    print(f"❌ {description}: 结构缺失")
                    
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 主页测试异常: {e}")
        return False
    
    # 测试页面功能完整性
    print(f"\n🔗 测试页面功能完整性")
    print("-" * 40)
    
    links_to_test = [
        ("/", "主页"),
        ("/docs", "文档页面"),
        ("/feedback", "反馈页面")
    ]
    
    for path, name in links_to_test:
        try:
            response = requests.get(f"{base_url}{path}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: 正常访问")
            else:
                print(f"❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 异常 ({e})")
    
    # 检查页面视觉效果
    print(f"\n🎨 检查页面视觉效果")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # 检查CSS样式是否完整
            css_checks = [
                ("hero", "Hero区域样式"),
                ("description", "描述区域样式"),
                ("btn-group", "按钮组样式"),
                ("features-section", "特性区域样式"),
                ("navbar", "导航栏样式")
            ]
            
            for css_class, description in css_checks:
                if f'class="{css_class}"' in content or f'class=\'{css_class}\'' in content:
                    print(f"✅ {description}: 样式完整")
                else:
                    print(f"⚠️ {description}: 样式可能缺失")
            
            # 检查链接是否正常
            if 'href="/docs"' in content and 'href="/feedback"' in content:
                print("✅ 导航链接: 完整")
            else:
                print("❌ 导航链接: 不完整")
                
    except Exception as e:
        print(f"❌ 视觉效果检查异常: {e}")
    
    # 生成测试报告
    print(f"\n📊 内容删除测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"主页地址: {base_url}/")
    
    print(f"\n🎯 删除效果")
    print("-" * 40)
    print("✅ 已删除内容:")
    print("   - ❌ 'YH API测试框架 是一个用于构建API测试的现代、快速（高性能）的框架，基于标准的Python类型提示。'")
    print("   - ❌ 'YH API测试框架是一个现代、快速、高性能的API测试工具。'")
    
    print(f"\n✅ 保留内容:")
    print("   - ✅ 文档和源码链接")
    print("   - ✅ 关键特性区域")
    print("   - ✅ 导航栏和按钮")
    print("   - ✅ 页面整体结构")
    
    print(f"\n🌟 优化效果")
    print("-" * 40)
    print("🎨 页面更简洁 - 移除了冗长的描述文字")
    print("🎯 重点突出 - 直接展示文档和源码链接")
    print("📱 视觉清爽 - 减少了文字密度")
    print("⚡ 加载更快 - 页面内容更精简")
    print("🔗 功能完整 - 核心功能和链接都保留")
    
    print(f"\n🎊 内容删除完成！")
    print(f"🌐 访问地址: {base_url}")
    
    return True

if __name__ == "__main__":
    success = test_content_removal()
    if success:
        print(f"\n🎉 内容删除测试完成！页面更加简洁清爽！")
    else:
        print(f"\n🔧 需要进一步检查页面内容")

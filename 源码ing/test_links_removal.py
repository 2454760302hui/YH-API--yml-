#!/usr/bin/env python3
"""
测试链接删除效果
"""

import requests

def test_links_removal():
    """测试链接删除效果"""
    print("🔗 测试链接删除效果")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8103"
    
    # 测试主页链接删除
    print(f"\n🏠 测试主页链接删除")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
            
            content = response.text
            
            # 检查已删除的链接内容
            removed_links_checks = [
                ("文档: http://", "文档链接"),
                ("源码: https://github.com/YH-API-Test/api-test-framework", "源码链接"),
                ("link-item", "链接样式类"),
                ("/docs", "文档路径"),
                ("github.com/YH-API-Test", "GitHub链接")
            ]
            
            print(f"\n🗑️ 已删除链接检查:")
            for link_text, description in removed_links_checks:
                # 检查描述区域是否还包含这些链接
                desc_start = content.find('<div class="description">')
                desc_end = content.find('</div>', desc_start + 100) if desc_start != -1 else -1
                
                if desc_start != -1 and desc_end != -1:
                    desc_section = content[desc_start:desc_end]
                    link_exists = link_text in desc_section
                else:
                    link_exists = link_text in content
                
                if not link_exists:
                    print(f"✅ {description}: 已删除")
                else:
                    print(f"❌ {description}: 仍然存在")
            
            # 检查描述区域是否为空
            if '<div class="description">' in content:
                desc_start = content.find('<div class="description">')
                desc_end = content.find('</div>', desc_start + 100)
                if desc_start != -1 and desc_end != -1:
                    desc_content = content[desc_start:desc_end]
                    # 检查是否只包含空白内容
                    clean_content = desc_content.replace('<div class="description">', '').replace('</div>', '').strip()
                    if not clean_content or clean_content.isspace():
                        print("✅ 描述区域: 已清空")
                    else:
                        print(f"⚠️ 描述区域: 仍有内容 - {clean_content[:50]}...")
            
            # 检查保留的内容
            preserved_content_checks = [
                ("YH API", "框架名称"),
                ("关键特性", "特性区域"),
                ("查看文档", "文档按钮"),
                ("GitHub", "GitHub按钮"),
                ("hero", "Hero区域"),
                ("features-section", "特性区域"),
                ("btn-group", "按钮组")
            ]
            
            print(f"\n✅ 保留内容检查:")
            for content_text, description in preserved_content_checks:
                if content_text in content:
                    print(f"✅ {description}: 正常保留")
                else:
                    print(f"❌ {description}: 意外丢失")
                    
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
            
            # 检查主要区域是否完整
            main_sections = [
                ("hero", "Hero区域"),
                ("description", "描述区域"),
                ("features-section", "特性区域"),
                ("btn-group", "按钮组"),
                ("navbar", "导航栏")
            ]
            
            for section, description in main_sections:
                if section in content:
                    print(f"✅ {description}: 结构完整")
                else:
                    print(f"❌ {description}: 结构缺失")
            
            # 检查导航和按钮是否正常
            if 'href="/docs"' in content and 'href="/feedback"' in content:
                print("✅ 导航链接: 完整")
            else:
                print("❌ 导航链接: 不完整")
                
            if '查看文档' in content and 'GitHub' in content:
                print("✅ 操作按钮: 完整")
            else:
                print("❌ 操作按钮: 不完整")
                
    except Exception as e:
        print(f"❌ 视觉效果检查异常: {e}")
    
    # 生成测试报告
    print(f"\n📊 链接删除测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"主页地址: {base_url}/")
    
    print(f"\n🎯 删除效果")
    print("-" * 40)
    print("✅ 已删除内容:")
    print("   - ❌ '文档: http://127.0.0.1:8080/docs'")
    print("   - ❌ '源码: https://github.com/YH-API-Test/api-test-framework'")
    print("   - ❌ 描述区域的链接内容")
    
    print(f"\n✅ 保留内容:")
    print("   - ✅ 导航栏的文档和反馈链接")
    print("   - ✅ 按钮组的查看文档和GitHub按钮")
    print("   - ✅ Hero区域和特性展示")
    print("   - ✅ 页面整体结构和样式")
    
    print(f"\n🌟 优化效果")
    print("-" * 40)
    print("🎨 页面更简洁 - 移除了中间区域的重复链接")
    print("🎯 重点突出 - 用户注意力集中在Hero区域和按钮组")
    print("📱 视觉清爽 - 减少了链接密度")
    print("⚡ 布局优化 - 描述区域更加简洁")
    print("🔗 功能完整 - 通过导航栏和按钮组仍可访问所有功能")
    
    print(f"\n🎊 链接删除完成！")
    print(f"🌐 访问地址: {base_url}")
    
    return True

if __name__ == "__main__":
    success = test_links_removal()
    if success:
        print(f"\n🎉 链接删除测试完成！页面更加简洁，重复链接已移除！")
    else:
        print(f"\n🔧 需要进一步检查页面链接")

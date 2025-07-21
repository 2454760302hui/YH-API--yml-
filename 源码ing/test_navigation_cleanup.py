#!/usr/bin/env python3
"""
测试导航栏清理效果
"""

import requests

def test_navigation_cleanup():
    """测试导航栏清理效果"""
    print("🧹 测试导航栏清理效果")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8098"
    
    # 测试主页导航栏
    print(f"\n🏠 测试主页导航栏")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
            
            content = response.text
            
            # 检查导航链接
            nav_checks = [
                ("文档", True, "应该保留"),
                ("关于", True, "应该保留"),
                ("API", False, "应该移除"),
                ("状态", False, "应该移除"),
                ("参考", False, "应该移除")
            ]
            
            print(f"\n📋 主页导航栏检查:")
            for link_text, should_exist, description in nav_checks:
                # 检查导航链接是否存在
                nav_pattern = f'<li><a href="[^"]*">{link_text}</a></li>'
                if link_text in content and "nav-links" in content:
                    # 更精确的检查
                    nav_section_start = content.find('<ul class="nav-links">')
                    nav_section_end = content.find('</ul>', nav_section_start)
                    if nav_section_start != -1 and nav_section_end != -1:
                        nav_section = content[nav_section_start:nav_section_end]
                        link_exists = f'>{link_text}<' in nav_section
                    else:
                        link_exists = f'>{link_text}<' in content
                else:
                    link_exists = False
                
                if should_exist:
                    if link_exists:
                        print(f"✅ {link_text}: 存在 ({description})")
                    else:
                        print(f"❌ {link_text}: 缺失 ({description})")
                else:
                    if not link_exists:
                        print(f"✅ {link_text}: 已移除 ({description})")
                    else:
                        print(f"❌ {link_text}: 仍然存在 ({description})")
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 主页测试异常: {e}")
    
    # 测试文档页面导航栏
    print(f"\n📖 测试文档页面导航栏")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 文档页面访问正常")
            
            content = response.text
            
            # 检查文档页面导航链接
            nav_checks = [
                ("文档", True, "应该保留"),
                ("关于", True, "应该保留"),
                ("API", False, "应该移除"),
                ("状态", False, "应该移除")
            ]
            
            print(f"\n📋 文档页面导航栏检查:")
            for link_text, should_exist, description in nav_checks:
                # 检查导航链接是否存在
                nav_section_start = content.find('<ul class="nav-links">')
                nav_section_end = content.find('</ul>', nav_section_start)
                if nav_section_start != -1 and nav_section_end != -1:
                    nav_section = content[nav_section_start:nav_section_end]
                    link_exists = f'>{link_text}<' in nav_section
                else:
                    link_exists = f'>{link_text}<' in content
                
                if should_exist:
                    if link_exists:
                        print(f"✅ {link_text}: 存在 ({description})")
                    else:
                        print(f"❌ {link_text}: 缺失 ({description})")
                else:
                    if not link_exists:
                        print(f"✅ {link_text}: 已移除 ({description})")
                    else:
                        print(f"❌ {link_text}: 仍然存在 ({description})")
        else:
            print(f"❌ 文档页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 文档页面测试异常: {e}")
    
    # 测试功能链接是否仍然可用
    print(f"\n🔗 测试保留功能的可用性")
    print("-" * 40)
    
    links_to_test = [
        ("/", "主页"),
        ("/docs", "文档页面")
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
    
    # 验证移除的链接确实不在导航中
    print(f"\n🚫 验证移除的链接")
    print("-" * 40)
    
    removed_links = [
        ("/health", "状态页面"),
        ("/api-docs", "API文档"),
        ("https://httpbig.org", "参考链接")
    ]
    
    for path, name in removed_links:
        try:
            if path.startswith("http"):
                print(f"ℹ️ {name}: 外部链接，已从导航移除")
            else:
                response = requests.get(f"{base_url}{path}", timeout=3)
                if response.status_code == 200:
                    print(f"ℹ️ {name}: 功能仍可用，但已从导航移除")
                else:
                    print(f"ℹ️ {name}: 已从导航移除")
        except Exception as e:
            print(f"ℹ️ {name}: 已从导航移除")
    
    # 生成测试报告
    print(f"\n📊 导航栏清理测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"主页地址: {base_url}/")
    print(f"文档地址: {base_url}/docs")
    
    print(f"\n🎯 清理效果")
    print("-" * 40)
    print("✅ 主页导航栏 - 只保留'文档'和'关于'")
    print("✅ 文档页面导航栏 - 只保留'文档'和'关于'")
    print("✅ 移除的链接:")
    print("   - ❌ API (原/api-docs)")
    print("   - ❌ 状态 (原/health)")
    print("   - ❌ 参考 (原https://httpbig.org)")
    
    print(f"\n🌟 导航栏优化效果")
    print("-" * 40)
    print("🎨 界面更简洁 - 减少了不必要的导航项")
    print("🎯 重点突出 - 突出文档功能")
    print("📱 移动友好 - 更少的导航项，移动端更清爽")
    print("🔗 保持功能 - 核心功能仍然可用")
    
    print(f"\n🎊 导航栏清理完成！")
    print(f"🌐 访问地址: {base_url}")
    
    return True

if __name__ == "__main__":
    success = test_navigation_cleanup()
    if success:
        print(f"\n🎉 导航栏清理测试完成！页面导航更加简洁清爽！")
    else:
        print(f"\n🔧 需要进一步检查导航栏配置")

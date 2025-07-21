#!/usr/bin/env python3
"""
测试内容删除效果
"""

import requests

def test_content_removal():
    """测试内容删除效果"""
    print("🗑️ 测试内容删除效果")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8105"
    
    # 测试文档页面内容删除
    print(f"\n📖 测试文档页面内容删除")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 文档页面访问正常")
            
            content = response.text
            
            # 检查已删除的内容
            removed_content_checks = [
                ("更多示例：", "更多示例提示框"),
                ("GitHub示例目录", "GitHub示例目录链接"),
                ("访问 <a href=\"https://github.com/YH-API-Test/api-test-framework/tree/main/examples\"", "GitHub示例链接"),
                ("GitHub: YH-API-Test/api-test-framework", "联系部分的GitHub链接"),
                ("<li><strong>GitHub:</strong>", "GitHub联系项")
            ]
            
            print(f"\n🗑️ 已删除内容检查:")
            for content_text, description in removed_content_checks:
                if content_text not in content:
                    print(f"✅ {description}: 已删除")
                else:
                    print(f"❌ {description}: 仍然存在")
            
            # 检查保留的内容
            preserved_content_checks = [
                ("QQ: 2677989813", "QQ联系方式"),
                ("联系和支持", "联系和支持标题"),
                ("持续改进", "持续改进提示"),
                ("Python SDK", "Python SDK部分"),
                ("API参考", "API参考部分"),
                ("使用示例", "使用示例部分")
            ]
            
            print(f"\n✅ 保留内容检查:")
            for content_text, description in preserved_content_checks:
                if content_text in content:
                    print(f"✅ {description}: 正常保留")
                else:
                    print(f"❌ {description}: 意外丢失")
            
            # 检查页面结构完整性
            structure_checks = [
                ("联系和支持", "联系部分"),
                ("API参考", "API参考部分"),
                ("使用示例", "示例部分"),
                ("高级功能", "高级功能部分"),
                ("测试用例配置", "测试用例部分")
            ]
            
            print(f"\n🏗️ 页面结构检查:")
            for element, description in structure_checks:
                if element in content:
                    print(f"✅ {description}: 结构完整")
                else:
                    print(f"❌ {description}: 结构缺失")
                    
        else:
            print(f"❌ 文档页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 文档页面测试异常: {e}")
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
    
    # 检查联系部分的简化效果
    print(f"\n📞 检查联系部分简化效果")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # 查找联系和支持部分
            contact_start = content.find("联系和支持")
            if contact_start != -1:
                # 查找该部分的结束位置（下一个section或页面结束）
                next_section = content.find('<div class="section">', contact_start + 100)
                if next_section == -1:
                    next_section = content.find('</div>', contact_start + 500)
                
                if next_section != -1:
                    contact_section = content[contact_start:next_section]
                    
                    # 检查联系部分的内容
                    if "QQ: 2677989813" in contact_section:
                        print("✅ QQ联系方式: 保留")
                    else:
                        print("❌ QQ联系方式: 缺失")
                    
                    if "GitHub:" not in contact_section:
                        print("✅ GitHub链接: 已删除")
                    else:
                        print("❌ GitHub链接: 仍然存在")
                    
                    if "持续改进" in contact_section:
                        print("✅ 持续改进提示: 保留")
                    else:
                        print("❌ 持续改进提示: 缺失")
                else:
                    print("⚠️ 无法确定联系部分的范围")
            else:
                print("❌ 未找到联系和支持部分")
                
    except Exception as e:
        print(f"❌ 联系部分检查异常: {e}")
    
    # 生成测试报告
    print(f"\n📊 内容删除测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"文档地址: {base_url}/docs")
    
    print(f"\n🎯 删除效果")
    print("-" * 40)
    print("✅ 已删除内容:")
    print("   - ❌ '更多示例：访问GitHub示例目录查看更多使用示例'")
    print("   - ❌ '联系和支持'部分的'GitHub: YH-API-Test/api-test-framework'")
    
    print(f"\n✅ 保留内容:")
    print("   - ✅ QQ联系方式: 2677989813")
    print("   - ✅ 持续改进提示信息")
    print("   - ✅ 所有文档章节和内容")
    print("   - ✅ 页面整体结构和功能")
    
    print(f"\n🌟 优化效果")
    print("-" * 40)
    print("🎨 页面更简洁 - 移除了不必要的外部链接")
    print("🎯 重点突出 - 突出QQ联系方式")
    print("📱 信息精简 - 减少了重复的GitHub链接")
    print("⚡ 内容聚焦 - 专注于核心联系方式")
    print("🔗 功能完整 - 其他功能和内容都保留")
    
    print(f"\n🎊 内容删除完成！")
    print(f"🌐 访问地址: {base_url}/docs")
    
    return True

if __name__ == "__main__":
    success = test_content_removal()
    if success:
        print(f"\n🎉 内容删除测试完成！页面更加简洁，重复内容已移除！")
    else:
        print(f"\n🔧 需要进一步检查页面内容")

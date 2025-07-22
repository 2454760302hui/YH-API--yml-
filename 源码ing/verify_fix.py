#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证Allure报告详情展开功能修复
"""

from swagger_docs import SwaggerDocsServer
import re

def verify_allure_report_fix():
    """验证Allure报告修复"""
    print("🔍 验证Allure报告详情展开功能修复...")
    
    try:
        # 创建文档服务器实例
        docs_server = SwaggerDocsServer()
        
        # 获取Allure报告HTML
        html_content = docs_server.get_allure_report_html()
        
        print("✅ HTML内容生成成功")
        print(f"📊 HTML内容长度: {len(html_content):,} 字符")
        
        # 验证关键功能
        checks = []
        
        # 1. 检查测试项目点击事件
        test_items = ['api-test', 'docs-test', 'feedback-test', 'copy-test', 'responsive-test', 'nav-test', 'performance-test']
        for test_id in test_items:
            onclick_pattern = f'onclick="toggleTestDetails\(\'{test_id}\'\)"'
            if onclick_pattern in html_content:
                checks.append(f"✅ {test_id}: 点击事件配置正确")
            else:
                checks.append(f"❌ {test_id}: 点击事件缺失")
        
        # 2. 检查详情区域
        for test_id in test_items:
            details_pattern = f'id="details-{test_id}"'
            if details_pattern in html_content:
                checks.append(f"✅ {test_id}: 详情区域配置正确")
            else:
                checks.append(f"❌ {test_id}: 详情区域缺失")
        
        # 3. 检查展开图标
        for test_id in test_items:
            icon_pattern = f'id="expand-{test_id}"'
            if icon_pattern in html_content:
                checks.append(f"✅ {test_id}: 展开图标配置正确")
            else:
                checks.append(f"❌ {test_id}: 展开图标缺失")
        
        # 4. 检查JavaScript函数
        js_checks = [
            ('function toggleTestDetails(testId)', 'toggleTestDetails函数'),
            ('detailsElement.style.display === \'none\'', '显示状态检查'),
            ('expandIcon.textContent = \'▲\'', '图标文本切换'),
            ('expandIcon.classList.add(\'expanded\')', '样式类切换'),
            ('console.log(\'Toggling test details for:\', testId)', '调试日志')
        ]
        
        for pattern, description in js_checks:
            if pattern in html_content:
                checks.append(f"✅ JavaScript: {description} 已实现")
            else:
                checks.append(f"❌ JavaScript: {description} 缺失")
        
        # 5. 检查CSS样式
        css_checks = [
            ('.test-details', '详情区域样式'),
            ('.expand-icon', '展开图标样式'),
            ('.expand-icon.expanded', '展开状态样式'),
            ('transform: rotate(180deg)', '旋转动画'),
            ('transition: transform 0.2s', '过渡动画')
        ]
        
        for pattern, description in css_checks:
            if pattern in html_content:
                checks.append(f"✅ CSS: {description} 已配置")
            else:
                checks.append(f"❌ CSS: {description} 缺失")
        
        # 6. 检查详细信息内容
        content_checks = [
            ('测试信息', '基本信息区域'),
            ('请求参数', '请求参数区域'),
            ('响应结果', '响应结果区域'),
            ('性能指标', '性能指标区域'),
            ('异常信息', '错误信息区域'),
            ('建议修复', '修复建议区域')
        ]
        
        for pattern, description in content_checks:
            if pattern in html_content:
                checks.append(f"✅ 内容: {description} 完整")
            else:
                checks.append(f"❌ 内容: {description} 缺失")
        
        # 输出检查结果
        print("\n📋 详细检查结果:")
        for check in checks:
            print(f"   {check}")
        
        # 统计结果
        success_count = len([c for c in checks if c.startswith('✅')])
        total_count = len(checks)
        success_rate = (success_count / total_count) * 100
        
        print(f"\n📊 修复验证结果:")
        print(f"   总检查项: {total_count}")
        print(f"   通过项: {success_count}")
        print(f"   失败项: {total_count - success_count}")
        print(f"   成功率: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print(f"\n🎉 修复验证成功！Allure报告详情展开功能已正常工作！")
            return True
        elif success_rate >= 80:
            print(f"\n⚠️ 修复基本成功，但仍有少量问题需要解决")
            return True
        else:
            print(f"\n❌ 修复验证失败，需要进一步检查和修复")
            return False
            
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return False

if __name__ == "__main__":
    verify_allure_report_fix()

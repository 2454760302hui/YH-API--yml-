#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Allure报告详情展开功能
"""

import requests
import time
from swagger_docs import SwaggerDocsServer

def test_allure_report_details():
    """测试Allure报告详情功能"""
    print("🧪 测试Allure报告详情展开功能...")
    
    try:
        # 创建文档服务器实例
        docs_server = SwaggerDocsServer()
        
        # 获取Allure报告HTML
        html_content = docs_server.get_allure_report_html()
        
        # 检查HTML内容
        print("📋 检查HTML内容...")
        
        # 检查测试项目是否存在
        test_items = [
            "api-test",
            "docs-test", 
            "feedback-test",
            "copy-test",
            "responsive-test",
            "nav-test",
            "performance-test"
        ]
        
        for test_id in test_items:
            # 检查测试项目头部
            header_check = f'onclick="toggleTestDetails(\'{test_id}\')"'
            if header_check in html_content:
                print(f"✅ 测试项目 {test_id}: 点击事件已配置")
            else:
                print(f"❌ 测试项目 {test_id}: 点击事件缺失")
            
            # 检查详情区域
            details_check = f'id="details-{test_id}"'
            if details_check in html_content:
                print(f"✅ 测试项目 {test_id}: 详情区域已配置")
            else:
                print(f"❌ 测试项目 {test_id}: 详情区域缺失")
            
            # 检查展开图标
            icon_check = f'id="expand-{test_id}"'
            if icon_check in html_content:
                print(f"✅ 测试项目 {test_id}: 展开图标已配置")
            else:
                print(f"❌ 测试项目 {test_id}: 展开图标缺失")
        
        # 检查JavaScript函数
        print("\n⚙️ 检查JavaScript功能...")
        js_checks = [
            ("toggleTestDetails", "展开/折叠函数"),
            ("console.log('Toggling test details for:', testId)", "调试日志"),
            ("detailsElement.style.display === 'block'", "显示逻辑"),
            ("expandIcon.textContent = '▲'", "图标切换"),
            ("expandIcon.classList.add('expanded')", "样式切换")
        ]
        
        for js_code, description in js_checks:
            if js_code in html_content:
                print(f"✅ {description}: 已实现")
            else:
                print(f"❌ {description}: 缺失")
        
        # 检查CSS样式
        print("\n🎨 检查CSS样式...")
        css_checks = [
            (".test-details", "详情区域样式"),
            (".expand-icon", "展开图标样式"),
            (".expand-icon.expanded", "展开状态样式"),
            ("transform: rotate(180deg)", "旋转动画"),
            ("transition: transform 0.2s", "过渡动画")
        ]
        
        for css_code, description in css_checks:
            if css_code in html_content:
                print(f"✅ {description}: 已配置")
            else:
                print(f"❌ {description}: 缺失")
        
        # 保存HTML文件用于测试
        with open("test_allure_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n📄 HTML文件已保存: test_allure_report.html")
        print(f"📊 HTML文件大小: {len(html_content):,} 字符")
        
        # 检查详细信息内容
        print("\n🔍 检查详细信息内容...")
        detail_content_checks = [
            ("测试信息", "基本信息区域"),
            ("请求参数", "请求参数区域"),
            ("响应结果", "响应结果区域"),
            ("性能指标", "性能指标区域"),
            ("异常信息", "错误信息区域"),
            ("建议修复", "修复建议区域")
        ]
        
        for content, description in detail_content_checks:
            if content in html_content:
                print(f"✅ {description}: 内容完整")
            else:
                print(f"❌ {description}: 内容缺失")
        
        print("\n🎉 Allure报告详情功能测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_allure_report_details()

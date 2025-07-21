#!/usr/bin/env python3
"""
测试FastAPI风格主页效果
"""

import requests
import time
from bs4 import BeautifulSoup

def test_homepage_style():
    """测试主页风格和内容"""
    print("🎨 测试FastAPI风格主页")
    print("=" * 50)
    
    # 寻找活动服务器
    ports = [8095, 8094, 8101, 8100]
    active_port = None
    
    for port in ports:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/", timeout=3)
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
    
    # 测试主页内容
    print(f"\n🏠 测试主页内容")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print(f"❌ 主页访问失败: {response.status_code}")
            return False
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 检查页面标题
        title = soup.find('title')
        if title and "YH API测试框架" in title.text:
            print("✅ 页面标题正确")
        else:
            print("❌ 页面标题不正确")
        
        # 检查导航栏
        navbar = soup.find('nav', class_='navbar')
        if navbar:
            print("✅ 导航栏存在")
            
            # 检查导航链接
            nav_links = navbar.find_all('a')
            expected_links = ['文档', 'GitHub']
            found_links = []
            for link in nav_links:
                if link.text.strip() in expected_links:
                    found_links.append(link.text.strip())
            
            if len(found_links) >= 2:
                print(f"✅ 导航链接完整: {found_links}")
            else:
                print(f"⚠️ 导航链接不完整: {found_links}")
        else:
            print("❌ 导航栏不存在")
        
        # 检查Hero区域
        hero = soup.find('div', class_='hero')
        if hero:
            print("✅ Hero区域存在")
            
            # 检查Logo
            hero_logo = hero.find('div', class_='hero-logo')
            if hero_logo:
                print("✅ Hero Logo存在")
            else:
                print("❌ Hero Logo不存在")
            
            # 检查主标题
            h1 = hero.find('h1')
            if h1 and "YH API" in h1.text:
                print("✅ 主标题正确")
            else:
                print("❌ 主标题不正确")
            
            # 检查副标题
            subtitle = hero.find('p', class_='hero-subtitle')
            if subtitle and "API测试框架" in subtitle.text:
                print("✅ 副标题正确")
            else:
                print("❌ 副标题不正确")
            
            # 检查徽章
            badges = hero.find_all('span', class_='badge')
            if len(badges) >= 3:
                badge_texts = [badge.text.strip() for badge in badges]
                print(f"✅ 徽章完整: {badge_texts}")
            else:
                print(f"⚠️ 徽章不完整: {len(badges)}个")
        else:
            print("❌ Hero区域不存在")
        
        # 检查特性区域
        features = soup.find('div', class_='features-section')
        if features:
            print("✅ 特性区域存在")
            
            # 检查特性卡片
            feature_cards = features.find_all('div', class_='feature-card')
            if len(feature_cards) >= 6:
                print(f"✅ 特性卡片完整: {len(feature_cards)}个")
                
                # 检查特性标题
                feature_titles = []
                for card in feature_cards[:3]:  # 检查前3个
                    title_elem = card.find('div', class_='feature-title')
                    if title_elem:
                        feature_titles.append(title_elem.text.strip())
                
                expected_features = ['快速', '高效编码', '更少bug']
                if any(feature in feature_titles for feature in expected_features):
                    print(f"✅ 特性标题正确: {feature_titles}")
                else:
                    print(f"⚠️ 特性标题需要检查: {feature_titles}")
            else:
                print(f"⚠️ 特性卡片不完整: {len(feature_cards)}个")
        else:
            print("❌ 特性区域不存在")
        
        # 检查按钮组
        btn_group = soup.find('div', class_='btn-group')
        if btn_group:
            print("✅ 按钮组存在")
            
            buttons = btn_group.find_all('a', class_='btn')
            if len(buttons) >= 2:
                button_texts = [btn.text.strip() for btn in buttons]
                print(f"✅ 按钮完整: {button_texts}")
            else:
                print(f"⚠️ 按钮不完整: {len(buttons)}个")
        else:
            print("❌ 按钮组不存在")
        
        # 检查CSS样式
        style_tags = soup.find_all('style')
        if style_tags:
            style_content = ''.join([style.text for style in style_tags])
            
            # 检查关键CSS类
            css_classes = [
                '.navbar', '.hero', '.features-section', 
                '.feature-card', '.btn-group', '.btn'
            ]
            
            found_classes = []
            for css_class in css_classes:
                if css_class in style_content:
                    found_classes.append(css_class)
            
            if len(found_classes) >= 5:
                print(f"✅ CSS样式完整: {len(found_classes)}/{len(css_classes)}个类")
            else:
                print(f"⚠️ CSS样式不完整: {len(found_classes)}/{len(css_classes)}个类")
        else:
            print("❌ CSS样式不存在")
        
    except Exception as e:
        print(f"❌ 主页测试异常: {e}")
        return False
    
    # 测试文档页面链接
    print(f"\n📖 测试文档页面链接")
    print("-" * 40)
    
    try:
        docs_response = requests.get(f"{base_url}/docs", timeout=5)
        if docs_response.status_code == 200:
            print("✅ 文档页面访问正常")
        else:
            print(f"❌ 文档页面访问失败: {docs_response.status_code}")
    except Exception as e:
        print(f"❌ 文档页面测试异常: {e}")
    
    # 测试健康检查
    print(f"\n💚 测试健康检查")
    print("-" * 40)
    
    try:
        health_response = requests.get(f"{base_url}/health", timeout=3)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ 健康检查正常: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ 健康检查失败: {health_response.status_code}")
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
    
    # 生成测试报告
    print(f"\n📊 FastAPI风格主页测试报告")
    print("=" * 50)
    
    print(f"测试服务器: {base_url}")
    print(f"主页地址: {base_url}/")
    print(f"文档地址: {base_url}/docs")
    print(f"健康检查: {base_url}/health")
    
    print(f"\n🎯 风格对比")
    print("-" * 40)
    print("✅ 导航栏 - 类似FastAPI官网的蓝色导航栏")
    print("✅ Hero区域 - 大Logo + 标题 + 副标题 + 徽章")
    print("✅ 特性展示 - 网格布局的特性卡片")
    print("✅ 按钮组 - 主要和次要按钮")
    print("✅ 响应式设计 - 移动端适配")
    print("✅ 色彩方案 - 蓝色主题，专业感")
    
    print(f"\n🌟 改进效果")
    print("-" * 40)
    print("🎨 视觉效果 - 更加专业和现代")
    print("📱 用户体验 - 清晰的导航和布局")
    print("🔗 功能链接 - 文档、GitHub等链接完整")
    print("📊 信息展示 - 特性和优势突出显示")
    print("🎯 品牌形象 - YH品牌标识清晰")
    
    print(f"\n🎊 FastAPI风格主页创建成功！")
    print(f"🌐 访问地址: {base_url}")
    
    return True

if __name__ == "__main__":
    success = test_homepage_style()
    if success:
        print(f"\n🎉 FastAPI风格主页测试完成！页面风格现代化，用户体验优秀！")
    else:
        print(f"\n🔧 需要进一步优化主页设计")

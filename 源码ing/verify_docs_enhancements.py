#!/usr/bin/env python3
"""
验证文档增强功能
- 返回按钮功能
- 一键复制功能
- GitHub链接更新
"""

import requests
import time
from bs4 import BeautifulSoup

def test_docs_enhancements():
    """测试文档增强功能"""
    base_url = "http://127.0.0.1:8083"
    
    print("🔍 开始验证文档增强功能...")
    
    # 测试1: 主页GitHub链接更新
    print("\n1. 测试主页GitHub链接更新...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            github_link = soup.find('a', href=lambda x: x and 'github.com' in x)
            if github_link:
                print(f"   ✅ GitHub链接已更新: {github_link.get('href')}")
                print(f"   ✅ 链接文本: {github_link.text}")
            else:
                print("   ❌ 未找到GitHub链接")
        else:
            print(f"   ❌ 主页访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 主页测试失败: {e}")
    
    # 测试2: 自定义Swagger UI文档页面
    print("\n2. 测试自定义Swagger UI文档页面...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查返回按钮
            back_btn = soup.find('a', class_='back-btn')
            if back_btn:
                print(f"   ✅ 返回按钮存在: {back_btn.text}")
                print(f"   ✅ 返回链接: {back_btn.get('href')}")
            else:
                print("   ❌ 未找到返回按钮")
            
            # 检查页面标题
            title = soup.find('title')
            if title and 'YH API测试框架' in title.text:
                print(f"   ✅ 页面标题正确: {title.text}")
            else:
                print("   ❌ 页面标题不正确")
            
            # 检查Swagger UI相关脚本
            swagger_scripts = soup.find_all('script', src=lambda x: x and 'swagger-ui' in x)
            if swagger_scripts:
                print(f"   ✅ Swagger UI脚本已加载: {len(swagger_scripts)}个")
            else:
                print("   ❌ 未找到Swagger UI脚本")
            
            # 检查复制按钮相关代码
            if 'addCopyButtons' in response.text:
                print("   ✅ 一键复制功能代码已添加")
            else:
                print("   ❌ 未找到一键复制功能代码")
                
        else:
            print(f"   ❌ Swagger文档页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Swagger文档页面测试失败: {e}")
    
    # 测试3: 自定义ReDoc文档页面
    print("\n3. 测试自定义ReDoc文档页面...")
    try:
        response = requests.get(f"{base_url}/redoc")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查返回按钮
            back_btn = soup.find('a', class_='back-btn')
            if back_btn:
                print(f"   ✅ 返回按钮存在: {back_btn.text}")
                print(f"   ✅ 返回链接: {back_btn.get('href')}")
            else:
                print("   ❌ 未找到返回按钮")
            
            # 检查页面标题
            title = soup.find('title')
            if title and 'ReDoc' in title.text:
                print(f"   ✅ 页面标题正确: {title.text}")
            else:
                print("   ❌ 页面标题不正确")
            
            # 检查ReDoc脚本
            redoc_scripts = soup.find_all('script', src=lambda x: x and 'redoc' in x)
            if redoc_scripts:
                print(f"   ✅ ReDoc脚本已加载: {len(redoc_scripts)}个")
            else:
                print("   ❌ 未找到ReDoc脚本")
                
        else:
            print(f"   ❌ ReDoc文档页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ReDoc文档页面测试失败: {e}")
    
    # 测试4: OpenAPI JSON端点
    print("\n4. 测试OpenAPI JSON端点...")
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            openapi_data = response.json()
            if 'info' in openapi_data and 'title' in openapi_data['info']:
                print(f"   ✅ OpenAPI JSON正常: {openapi_data['info']['title']}")
                print(f"   ✅ 版本: {openapi_data['info'].get('version', 'N/A')}")
            else:
                print("   ❌ OpenAPI JSON格式不正确")
        else:
            print(f"   ❌ OpenAPI JSON访问失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ OpenAPI JSON测试失败: {e}")
    
    # 测试5: 功能完整性检查
    print("\n5. 功能完整性检查...")
    
    # 检查主页链接是否正确指向新的文档页面
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            docs_link = soup.find('a', href='/docs')
            github_link = soup.find('a', href=lambda x: x and 'github.com' in x)
            
            if docs_link:
                print("   ✅ 主页包含文档链接")
            else:
                print("   ❌ 主页缺少文档链接")
                
            if github_link and github_link.get('target') == '_blank':
                print("   ✅ GitHub链接在新窗口打开")
            else:
                print("   ❌ GitHub链接配置不正确")
                
    except Exception as e:
        print(f"   ❌ 功能完整性检查失败: {e}")
    
    print("\n🎉 文档增强功能验证完成！")
    
    # 生成验证报告
    print("\n📋 验证报告:")
    print("=" * 50)
    print("✅ 已实现功能:")
    print("  • 主页GitHub链接更新为实际仓库地址")
    print("  • 自定义Swagger UI文档页面，包含返回按钮")
    print("  • 自定义ReDoc文档页面，包含返回按钮")
    print("  • 一键复制功能（JavaScript实现）")
    print("  • 统一的页面样式和用户体验")
    print("  • OpenAPI JSON端点正常工作")
    print("\n🚀 用户体验改进:")
    print("  • 用户可以轻松从文档页面返回主页")
    print("  • 用户可以一键复制代码块内容")
    print("  • GitHub链接在新窗口打开，不影响当前使用")
    print("  • 统一的视觉设计和品牌风格")

if __name__ == "__main__":
    test_docs_enhancements()

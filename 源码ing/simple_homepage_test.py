#!/usr/bin/env python3
"""
简单的主页测试
"""

import requests

def test_homepage():
    """测试主页"""
    print("🎨 测试FastAPI风格主页")
    print("=" * 50)
    
    # 测试端口8095
    try:
        response = requests.get("http://127.0.0.1:8095/", timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"页面大小: {len(response.text)} 字符")
        
        # 检查关键内容
        content = response.text
        checks = [
            ("YH API测试框架", "标题"),
            ("导航栏", "navbar"),
            ("快速、高性能", "副标题"),
            ("关键特性", "特性区域"),
            ("查看文档", "文档按钮"),
            ("GitHub", "GitHub链接"),
            ("class=\"hero\"", "Hero区域"),
            ("class=\"features-section\"", "特性区域"),
            ("class=\"btn-group\"", "按钮组")
        ]
        
        print(f"\n✅ 内容检查:")
        for keyword, description in checks:
            if keyword in content:
                print(f"✅ {description}: 存在")
            else:
                print(f"❌ {description}: 缺失")
        
        print(f"\n🌐 访问地址:")
        print(f"主页: http://127.0.0.1:8095/")
        print(f"文档: http://127.0.0.1:8095/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_homepage()

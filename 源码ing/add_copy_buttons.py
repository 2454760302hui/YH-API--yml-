#!/usr/bin/env python3
"""
批量为代码块添加复制按钮
"""

import re

def add_copy_buttons_to_file():
    """为swagger_docs.py中的所有代码块添加复制按钮"""
    
    # 读取文件
    with open('swagger_docs.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义需要替换的模式和替换内容
    replacements = [
        # YAML配置格式
        {
            'old': '''                <div class="code-header">test_cases.yaml</div>
                <div class="code-block">
                    <pre>test_cases:''',
            'new': '''                <div class="code-header">
                    <span>test_cases.yaml</span>
                    <button class="copy-btn" onclick="copyCode(this)" data-code="test_cases:
  - name: &quot;用户登录测试&quot;
    description: &quot;测试用户登录接口&quot;
    request:
      method: POST
      url: &quot;https://api.example.com/login&quot;
      headers:
        Content-Type: &quot;application/json&quot;
      data:
        username: &quot;test_user&quot;
        password: &quot;test_password&quot;
    assertions:
      - type: &quot;status_code&quot;
        expected: 200
      - type: &quot;json_path&quot;
        path: &quot;$.success&quot;
        expected: true
      - type: &quot;response_time&quot;
        max_time: 2000
    extract:
      - name: &quot;access_token&quot;
        path: &quot;$.data.token&quot;
        
  - name: &quot;获取用户信息&quot;
    description: &quot;使用token获取用户信息&quot;
    request:
      method: GET
      url: &quot;https://api.example.com/user/profile&quot;
      headers:
        Authorization: &quot;Bearer ${{access_token}}&quot;
    assertions:
      - type: &quot;status_code&quot;
        expected: 200
      - type: &quot;json_path&quot;
        path: &quot;$.data.username&quot;
        expected: &quot;test_user&quot;">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        复制
                    </button>
                </div>
                <div class="code-block">
                    <pre>test_cases:'''
        }
    ]
    
    # 执行替换
    for replacement in replacements:
        if replacement['old'] in content:
            content = content.replace(replacement['old'], replacement['new'])
            print(f"✅ 已替换: {replacement['old'][:50]}...")
        else:
            print(f"❌ 未找到: {replacement['old'][:50]}...")
    
    # 写回文件
    with open('swagger_docs.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 批量添加复制按钮完成！")

if __name__ == "__main__":
    add_copy_buttons_to_file()

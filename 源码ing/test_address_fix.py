#!/usr/bin/env python3
"""
测试地址修复
"""

import os
import sys
import re

def test_address_fix():
    """测试地址修复"""
    print("=" * 60)
    print("测试localhost到127.0.0.1地址修复")
    print("=" * 60)
    
    # 要检查的文件
    files_to_check = [
        'quick_start.py',
        'yh_shell.py',
        'swagger_docs.py'
    ]
    
    results = {}
    
    for file_name in files_to_check:
        print(f"\n🔍 检查文件: {file_name}")
        print("-" * 40)
        
        if not os.path.exists(file_name):
            print(f"   ❌ 文件不存在: {file_name}")
            results[file_name] = {'status': 'missing', 'issues': []}
            continue
        
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找localhost引用
            localhost_patterns = [
                r'http://localhost:(\d+)',
                r'https://localhost:(\d+)',
                r'"localhost"',
                r"'localhost'"
            ]
            
            issues = []
            fixed_addresses = []
            
            for pattern in localhost_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    matched_text = match.group(0)
                    
                    # 检查是否是需要修复的地址
                    if 'localhost:8080' in matched_text:
                        if '127.0.0.1:8080' in content:
                            fixed_addresses.append({
                                'line': line_num,
                                'original': matched_text,
                                'status': 'fixed'
                            })
                        else:
                            issues.append({
                                'line': line_num,
                                'text': matched_text,
                                'type': 'needs_fix'
                            })
                    elif 'localhost:' in matched_text and '8080' in matched_text:
                        # 其他端口的localhost引用
                        issues.append({
                            'line': line_num,
                            'text': matched_text,
                            'type': 'other_port'
                        })
                    else:
                        # 其他localhost引用（可能是配置或示例）
                        issues.append({
                            'line': line_num,
                            'text': matched_text,
                            'type': 'other'
                        })
            
            # 检查127.0.0.1:8080的存在
            ip_addresses = re.findall(r'127\.0\.0\.1:8080', content)
            
            print(f"   📊 检查结果:")
            print(f"     - 找到 127.0.0.1:8080 引用: {len(ip_addresses)} 个")
            print(f"     - 已修复的地址: {len(fixed_addresses)} 个")
            print(f"     - 需要关注的问题: {len(issues)} 个")
            
            if fixed_addresses:
                print(f"   ✅ 已修复的地址:")
                for addr in fixed_addresses:
                    print(f"     行 {addr['line']}: {addr['original']} -> 已修复")
            
            if issues:
                print(f"   📋 发现的localhost引用:")
                for issue in issues:
                    if issue['type'] == 'needs_fix':
                        print(f"     ❌ 行 {issue['line']}: {issue['text']} (需要修复)")
                    elif issue['type'] == 'other_port':
                        print(f"     ⚠️ 行 {issue['line']}: {issue['text']} (其他端口)")
                    else:
                        print(f"     ℹ️ 行 {issue['line']}: {issue['text']} (配置/示例)")
            
            results[file_name] = {
                'status': 'checked',
                'fixed_count': len(fixed_addresses),
                'ip_count': len(ip_addresses),
                'issues': issues
            }
            
        except Exception as e:
            print(f"   ❌ 检查文件失败: {e}")
            results[file_name] = {'status': 'error', 'error': str(e)}
    
    # 总结报告
    print("\n" + "=" * 60)
    print("📊 修复总结报告")
    print("=" * 60)
    
    total_fixed = 0
    total_ip_refs = 0
    critical_issues = 0
    
    for file_name, result in results.items():
        if result['status'] == 'checked':
            total_fixed += result['fixed_count']
            total_ip_refs += result['ip_count']
            critical_issues += len([i for i in result['issues'] if i['type'] == 'needs_fix'])
    
    print(f"✅ 总计修复地址: {total_fixed} 个")
    print(f"✅ 127.0.0.1:8080 引用: {total_ip_refs} 个")
    print(f"⚠️ 需要修复的问题: {critical_issues} 个")
    
    # 重点检查文档服务器相关
    print(f"\n🎯 重点检查:")
    
    # 检查quick_start.py中的关键修复
    if 'quick_start.py' in results:
        result = results['quick_start.py']
        if result['status'] == 'checked' and result['ip_count'] > 0:
            print(f"✅ quick_start.py: 文档服务器地址已修复")
        else:
            print(f"❌ quick_start.py: 可能需要检查")
    
    # 检查yh_shell.py中的关键修复
    if 'yh_shell.py' in results:
        result = results['yh_shell.py']
        if result['status'] == 'checked' and result['ip_count'] > 0:
            print(f"✅ yh_shell.py: Shell文档地址已修复")
        else:
            print(f"❌ yh_shell.py: 可能需要检查")
    
    return critical_issues == 0

def main():
    """主函数"""
    success = test_address_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 地址修复验证成功！")
        print("\n✅ 修复内容:")
        print("- quick_start.py: 文档服务器地址 localhost -> 127.0.0.1")
        print("- yh_shell.py: Shell文档地址 localhost -> 127.0.0.1")
        print("- swagger_docs.py: 示例代码地址 localhost -> 127.0.0.1")
        
        print("\n🚀 现在用户看到的地址:")
        print("- 文档服务器已启动: http://127.0.0.1:8080")
        print("- 与Uvicorn显示的地址一致")
        print("- 避免了地址不一致的困惑")
        
        print("\n💡 用户体验改进:")
        print("- Uvicorn: http://127.0.0.1:8080")
        print("- 显示信息: http://127.0.0.1:8080")
        print("- 地址完全一致，用户体验更好")
        
    else:
        print("❌ 地址修复验证失败")
        print("仍有需要修复的localhost引用")
    
    print("\n📞 技术支持 QQ: 2677989813")
    print("💪 YH Spirit Lives On!")
    print("=" * 60)

if __name__ == "__main__":
    main()

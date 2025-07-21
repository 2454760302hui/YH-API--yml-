#!/usr/bin/env python3
"""
修复编码问题
"""

import os
import sys

def fix_file_encoding(filename):
    """修复文件编码问题"""
    try:
        # 尝试用不同编码读取文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                    used_encoding = encoding
                    print(f"✅ 成功使用 {encoding} 编码读取文件")
                    break
            except UnicodeDecodeError as e:
                print(f"❌ {encoding} 编码失败: {e}")
                continue
        
        if content is None:
            print("❌ 无法读取文件，尝试二进制模式")
            with open(filename, 'rb') as f:
                raw_content = f.read()
            
            # 尝试解码并替换问题字符
            try:
                content = raw_content.decode('utf-8', errors='replace')
                print("✅ 使用UTF-8编码并替换问题字符")
            except:
                content = raw_content.decode('gbk', errors='replace')
                print("✅ 使用GBK编码并替换问题字符")
        
        # 清理可能的问题字符
        content = content.replace('\x85', '')  # 移除问题字符
        content = content.replace('\ufffd', '')  # 移除替换字符
        
        # 保存为UTF-8编码
        backup_filename = filename + '.backup'
        os.rename(filename, backup_filename)
        print(f"✅ 原文件备份为: {backup_filename}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 文件已修复并保存为UTF-8编码: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def main():
    """主函数"""
    filename = "swagger_docs.py"
    
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return
    
    print(f"🔧 开始修复文件编码: {filename}")
    
    if fix_file_encoding(filename):
        print("🎉 编码修复完成！")
        
        # 验证修复结果
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            print("✅ 验证成功：文件可以正常读取")
            
            # 尝试导入模块
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("swagger_docs", filename)
                module = importlib.util.module_from_spec(spec)
                print("✅ 验证成功：模块可以正常导入")
            except Exception as e:
                print(f"⚠️  模块导入测试失败: {e}")
                
        except Exception as e:
            print(f"❌ 验证失败: {e}")
    else:
        print("❌ 编码修复失败")

if __name__ == "__main__":
    main()

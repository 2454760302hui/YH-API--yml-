#!/usr/bin/env python3
"""
修复 requirements.txt 编码问题
"""

import os

def fix_requirements_encoding():
    """修复 requirements.txt 编码问题"""
    filename = "requirements.txt"
    
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return False
    
    print(f"🔧 开始修复 {filename} 编码问题...")
    
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
        
        # 备份原文件
        backup_filename = filename + '.backup'
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        os.rename(filename, backup_filename)
        print(f"✅ 原文件备份为: {backup_filename}")
        
        # 保存为UTF-8编码
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 文件已修复并保存为UTF-8编码: {filename}")
        
        # 验证修复结果
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                test_content = f.read()
            print("✅ 验证成功：文件可以正常读取")
            return True
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

if __name__ == "__main__":
    success = fix_requirements_encoding()
    if success:
        print("\n🎉 requirements.txt 编码修复完成！")
        print("📝 现在可以正常执行: pip install -r requirements.txt")
    else:
        print("\n❌ 编码修复失败")

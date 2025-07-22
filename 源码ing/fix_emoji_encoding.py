#!/usr/bin/env python3
"""
修复emoji编码问题
"""

import re
import os

def fix_emoji_in_file(file_path):
    """修复文件中的emoji字符"""
    
    # emoji替换映射
    emoji_replacements = {
        '🚀': '[ROCKET]',
        '🔍': '[SEARCH]',
        '✅': '[CHECK]',
        '❌': '[CROSS]',
        '⚠️': '[WARNING]',
        '📊': '[CHART]',
        '🎉': '[PARTY]',
        '🌐': '[GLOBE]',
        '📋': '[CLIPBOARD]',
        '💡': '[BULB]',
        '🔧': '[WRENCH]',
        '📞': '[PHONE]',
        '💪': '[MUSCLE]',
        '🎯': '[TARGET]',
        '📖': '[BOOK]',
        '📝': '[MEMO]',
        '📦': '[PACKAGE]',
        '🏗️': '[CONSTRUCTION]',
        '⚙️': '[GEAR]',
        '📁': '[FOLDER]',
        '🧪': '[TEST_TUBE]',
        '💬': '[SPEECH]',
        '📱': '[MOBILE]',
        '🔗': '[LINK]',
        '🛡️': '[SHIELD]',
        '🔄': '[REFRESH]',
        '📈': '[TRENDING_UP]',
        '📉': '[TRENDING_DOWN]',
        '🐛': '[BUG]',
        '🎨': '[PALETTE]',
        '🏠': '[HOME]',
        '💻': '[COMPUTER]',
        '📚': '[BOOKS]',
        '🆘': '[SOS]',
        '🏃': '[RUNNER]',
        '🔥': '[FIRE]',
        '⚡': '[ZAP]',
        '💥': '[BOOM]',
        '💚': '[GREEN_HEART]',
        '🐍': '[SNAKE]',
        '🗑️': '[TRASH]',
        '📄': '[PAGE]',
        '📅': '[CALENDAR]',
        '⏱️': '[STOPWATCH]',
        '🔒': '[LOCK]',
        '🎊': '[CONFETTI]',
        '🌟': '[STAR]',
        '🚨': '[SIREN]',
        '💾': '[FLOPPY_DISK]',
        '🖥️': '[DESKTOP]',
        '🖨️': '[PRINTER]',
        '📤': '[OUTBOX]',
        '📥': '[INBOX]',
        '🤖': '[ROBOT]',
        '🔔': '[BELL]',
        '🛠️': '[HAMMER_WRENCH]',
        '🎪': '[CIRCUS]',
        '🎭': '[MASKS]',
        '🎬': '[CLAPPER]',
        '🎮': '[GAME]',
        '🎲': '[DICE]',
        '🎸': '[GUITAR]',
        '🎺': '[TRUMPET]',
        '🎻': '[VIOLIN]',
        '🥁': '[DRUM]',
        '🎤': '[MICROPHONE]',
        '🎧': '[HEADPHONES]',
        '📻': '[RADIO]',
        '📺': '[TV]',
        '📷': '[CAMERA]',
        '📹': '[VIDEO_CAMERA]',
        '💿': '[CD]',
        '💽': '[MINIDISC]',
        '💾': '[FLOPPY]',
        '💻': '[LAPTOP]',
        '🖥️': '[DESKTOP_COMPUTER]',
        '🖨️': '[PRINTER]',
        '⌨️': '[KEYBOARD]',
        '🖱️': '[MOUSE]',
        '🖲️': '[TRACKBALL]',
        '💡': '[LIGHT_BULB]',
        '🔦': '[FLASHLIGHT]',
        '🕯️': '[CANDLE]',
        '🪔': '[DIYA_LAMP]',
        '🔥': '[FIRE]',
        '💧': '[DROPLET]',
        '🌊': '[WAVE]',
    }
    
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换emoji
        original_content = content
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # 如果有修改，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 修复文件: {file_path}")
            return True
        else:
            print(f"- 无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("修复emoji编码问题")
    print("=" * 50)
    
    # 要修复的文件
    files_to_fix = [
        'swagger_docs.py'
    ]
    
    fixed_count = 0
    total_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            total_count += 1
            if fix_emoji_in_file(file_path):
                fixed_count += 1
        else:
            print(f"✗ 文件不存在: {file_path}")
    
    print("\n" + "=" * 50)
    print(f"修复完成: {fixed_count}/{total_count} 个文件")
    print("=" * 50)
    
    if fixed_count > 0:
        print("\n重新生成项目以应用修复...")
        
        # 重新生成项目
        try:
            import sys
            sys.path.append('.')
            from swagger_docs import SwaggerDocsServer
            
            docs_server = SwaggerDocsServer()
            zip_filename = docs_server.generate_project_structure()
            print(f"✓ 项目重新生成成功: {zip_filename}")
            
        except Exception as e:
            print(f"✗ 项目重新生成失败: {e}")

if __name__ == "__main__":
    main()

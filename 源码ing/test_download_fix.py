#!/usr/bin/env python3
"""
测试下载功能修复
"""

import requests
import os
import zipfile
import tempfile
import time

def test_direct_download():
    """测试直接下载功能"""
    print("🧪 测试直接下载功能...")
    
    try:
        # 测试直接下载
        print("📡 发送下载请求...")
        response = requests.get('http://localhost:8083/api/generate-project/direct', timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', '未知')}")
        print(f"Content-Length: {response.headers.get('Content-Length', '未知')}")
        
        if response.status_code == 200:
            # 保存文件
            filename = 'test-direct-download.zip'
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 文件下载成功: {filename}")
            print(f"📊 文件大小: {len(response.content)} bytes")
            
            # 测试ZIP文件
            try:
                with zipfile.ZipFile(filename, 'r') as zf:
                    file_list = zf.namelist()
                    print(f"📋 ZIP包含 {len(file_list)} 个文件:")
                    for i, file in enumerate(file_list[:5]):
                        print(f"   {i+1}. {file}")
                    if len(file_list) > 5:
                        print(f"   ... 还有 {len(file_list) - 5} 个文件")
                    
                    # 测试解压
                    temp_dir = tempfile.mkdtemp()
                    zf.extractall(temp_dir)
                    print("✅ ZIP文件解压测试成功")
                    
                    # 清理临时目录
                    import shutil
                    shutil.rmtree(temp_dir)
                    
            except Exception as e:
                print(f"❌ ZIP文件测试失败: {e}")
                return False
            
            # 清理测试文件
            os.remove(filename)
            return True
            
        else:
            print(f"❌ 下载失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_api_download():
    """测试API下载功能"""
    print("\n🧪 测试API下载功能...")
    
    try:
        # 先生成项目
        print("📡 发送生成项目请求...")
        response = requests.post('http://localhost:8083/api/generate-project/download', 
                               headers={'Content-Type': 'application/json'}, 
                               timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {data}")
            
            if data.get('success'):
                download_url = data.get('download_url')
                filename = data.get('filename')
                
                print(f"📥 下载链接: {download_url}")
                print(f"📄 文件名: {filename}")
                
                # 下载文件
                download_response = requests.get(f'http://localhost:8083{download_url}', timeout=30)
                
                if download_response.status_code == 200:
                    test_filename = f'test-api-{filename}'
                    with open(test_filename, 'wb') as f:
                        f.write(download_response.content)
                    
                    print(f"✅ API下载成功: {test_filename}")
                    print(f"📊 文件大小: {len(download_response.content)} bytes")
                    
                    # 测试ZIP文件
                    try:
                        with zipfile.ZipFile(test_filename, 'r') as zf:
                            file_list = zf.namelist()
                            print(f"📋 ZIP包含 {len(file_list)} 个文件")
                            
                            # 测试解压
                            temp_dir = tempfile.mkdtemp()
                            zf.extractall(temp_dir)
                            print("✅ ZIP文件解压测试成功")
                            
                            # 清理临时目录
                            import shutil
                            shutil.rmtree(temp_dir)
                            
                    except Exception as e:
                        print(f"❌ ZIP文件测试失败: {e}")
                        return False
                    
                    # 清理测试文件
                    os.remove(test_filename)
                    return True
                    
                else:
                    print(f"❌ 文件下载失败: {download_response.status_code}")
                    return False
            else:
                print(f"❌ 项目生成失败: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ API请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试下载功能修复...")
    print("=" * 60)
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(2)
    
    # 测试直接下载
    direct_result = test_direct_download()
    
    # 测试API下载
    api_result = test_api_download()
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print(f"   直接下载: {'✅ 通过' if direct_result else '❌ 失败'}")
    print(f"   API下载: {'✅ 通过' if api_result else '❌ 失败'}")
    
    if direct_result and api_result:
        print("\n🎉 所有测试通过！下载功能修复成功！")
        print("💡 用户现在可以正常下载和解压项目文件了。")
    else:
        print("\n❌ 部分测试失败，需要进一步修复。")
    
    print("\n📞 如有问题，请联系技术支持 QQ: 2677989813")

if __name__ == "__main__":
    main()

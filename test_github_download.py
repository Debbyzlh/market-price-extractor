#!/usr/bin/env python3
"""
测试GitHub下载功能
"""

import requests
import tempfile
import os
from pathlib import Path

def test_github_download(url, filename):
    """测试从GitHub下载文件"""
    print(f"🔍 测试下载: {filename}")
    print(f"📡 URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 检查文件大小
        file_size = len(response.content)
        print(f"✅ 下载成功! 文件大小: {file_size:,} 字节")
        
        # 保存到临时文件并验证
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        # 检查文件是否存在且可读
        if os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
            print(f"✅ 文件保存成功: {temp_file_path}")
            
            # 清理临时文件
            os.unlink(temp_file_path)
            return True
        else:
            print("❌ 文件保存失败")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False

def main():
    print("🧪 GitHub下载功能测试")
    print("=" * 50)
    
    # 测试URL (需要替换为实际的URL)
    test_urls = {
        "iPhone颜色对照表": "https://raw.githubusercontent.com/your-username/your-repo/main/color_en_cn_match.xlsx",
        "iPad颜色对照表": "https://raw.githubusercontent.com/your-username/your-repo/main/ipad_color_en_cn_match.xlsx"
    }
    
    success_count = 0
    total_count = len(test_urls)
    
    for name, url in test_urls.items():
        print(f"\n📋 测试 {name}...")
        if test_github_download(url, name):
            success_count += 1
        print("-" * 30)
    
    print(f"\n📊 测试结果: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("🎉 所有测试通过! GitHub下载功能正常工作")
    else:
        print("⚠️ 部分测试失败，请检查:")
        print("1. GitHub仓库URL是否正确")
        print("2. 仓库是否为公开仓库")
        print("3. 文件是否存在于指定路径")
        print("4. 网络连接是否正常")

if __name__ == "__main__":
    main() 
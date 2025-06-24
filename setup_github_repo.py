#!/usr/bin/env python3
"""
GitHub仓库设置脚本
用于自动创建GitHub仓库并上传颜色编码文件
"""

import os
import requests
import json
from pathlib import Path

def create_github_repo(token, repo_name, description="Market Scanner Assets"):
    """创建GitHub仓库"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": False,  # 公开仓库
        "auto_init": True  # 自动初始化README
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ 成功创建仓库: {repo_name}")
        return response.json()["clone_url"]
    else:
        print(f"❌ 创建仓库失败: {response.status_code}")
        print(response.text)
        return None

def upload_file_to_github(token, repo_owner, repo_name, file_path, file_content):
    """上传文件到GitHub"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 将文件内容编码为base64
    import base64
    content = base64.b64encode(file_content).decode('utf-8')
    
    data = {
        "message": f"Add {file_path}",
        "content": content
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [201, 200]:
        print(f"✅ 成功上传文件: {file_path}")
        return True
    else:
        print(f"❌ 上传文件失败 {file_path}: {response.status_code}")
        print(response.text)
        return False

def main():
    print("🚀 GitHub仓库设置向导")
    print("=" * 50)
    
    # 检查颜色编码文件是否存在
    color_files = ["color_en_cn_match.xlsx", "ipad_color_en_cn_match.xlsx"]
    missing_files = []
    
    for file in color_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少以下颜色编码文件: {', '.join(missing_files)}")
        print("请确保这些文件在当前目录中")
        return
    
    print("✅ 找到所有颜色编码文件")
    
    # 获取GitHub Token
    token = input("请输入你的GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ 需要GitHub Token才能继续")
        return
    
    # 获取仓库信息
    repo_name = input("请输入仓库名称 (默认: market-scanner-assets): ").strip()
    if not repo_name:
        repo_name = "market-scanner-assets"
    
    # 创建仓库
    clone_url = create_github_repo(token, repo_name)
    if not clone_url:
        return
    
    # 从clone URL中提取用户名
    repo_owner = clone_url.split('/')[-2]
    
    print(f"📁 仓库所有者: {repo_owner}")
    print(f"📁 仓库名称: {repo_name}")
    
    # 上传文件
    print("\n📤 正在上传颜色编码文件...")
    success_count = 0
    
    for file in color_files:
        with open(file, 'rb') as f:
            content = f.read()
        
        if upload_file_to_github(token, repo_owner, repo_name, file, content):
            success_count += 1
    
    if success_count == len(color_files):
        print("\n🎉 所有文件上传成功!")
        print("\n📋 请更新 streamlit_app.py 中的URL:")
        print(f"IPHONE_COLOR_URL = \"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/color_en_cn_match.xlsx\"")
        print(f"IPAD_COLOR_URL = \"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/ipad_color_en_cn_match.xlsx\"")
        
        # 自动更新streamlit_app.py
        update_app = input("\n是否自动更新 streamlit_app.py? (y/n): ").strip().lower()
        if update_app == 'y':
            update_streamlit_app(repo_owner, repo_name)
    else:
        print(f"\n⚠️ 部分文件上传失败 ({success_count}/{len(color_files)})")

def update_streamlit_app(repo_owner, repo_name):
    """自动更新streamlit_app.py中的URL"""
    try:
        with open('streamlit_app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新URL
        new_iphone_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/color_en_cn_match.xlsx"
        new_ipad_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/ipad_color_en_cn_match.xlsx"
        
        # 替换URL
        content = content.replace(
            'IPHONE_COLOR_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/color_en_cn_match.xlsx"',
            f'IPHONE_COLOR_URL = "{new_iphone_url}"'
        )
        content = content.replace(
            'IPAD_COLOR_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/ipad_color_en_cn_match.xlsx"',
            f'IPAD_COLOR_URL = "{new_ipad_url}"'
        )
        
        with open('streamlit_app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已自动更新 streamlit_app.py")
        
    except Exception as e:
        print(f"❌ 更新 streamlit_app.py 失败: {e}")
        print("请手动更新URL")

if __name__ == "__main__":
    main() 
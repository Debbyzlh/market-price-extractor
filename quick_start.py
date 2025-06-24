#!/usr/bin/env python3
"""
快速启动脚本
帮助用户快速设置和运行Market Scanner应用
"""

import os
import sys
import subprocess
import requests

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'streamlit', 'pandas', 'openpyxl', 'Pillow', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 安装缺失的依赖包...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ 依赖包安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖包安装失败")
            return False
    
    return True

def check_color_files():
    """检查颜色编码文件"""
    color_files = ["color_en_cn_match.xlsx", "ipad_color_en_cn_match.xlsx"]
    missing_files = []
    
    for file in color_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n⚠️ 缺少颜色编码文件: {', '.join(missing_files)}")
        print("建议运行 setup_github_repo.py 来设置GitHub仓库")
        return False
    
    return True

def check_github_setup():
    """检查GitHub设置"""
    print("\n🔍 检查GitHub设置...")
    
    # 读取streamlit_app.py中的URL
    try:
        with open('streamlit_app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'your-username/your-repo' in content:
            print("⚠️ 需要更新GitHub URL")
            print("请运行: python setup_github_repo.py")
            return False
        else:
            print("✅ GitHub URL已配置")
            return True
            
    except FileNotFoundError:
        print("❌ 找不到 streamlit_app.py")
        return False

def run_app():
    """运行Streamlit应用"""
    print("\n🚀 启动Market Scanner应用...")
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py'])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")

def main():
    print("🚀 Market Scanner 快速启动")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 检查依赖包
    print("\n📦 检查依赖包...")
    if not check_dependencies():
        return
    
    # 检查颜色编码文件
    print("\n📁 检查颜色编码文件...")
    check_color_files()
    
    # 检查GitHub设置
    if not check_github_setup():
        print("\n💡 提示:")
        print("1. 运行 'python setup_github_repo.py' 设置GitHub仓库")
        print("2. 或者手动更新 streamlit_app.py 中的GitHub URL")
        print("3. 然后重新运行此脚本")
        return
    
    # 询问是否启动应用
    print("\n" + "=" * 50)
    choice = input("是否现在启动应用? (y/n): ").strip().lower()
    
    if choice == 'y':
        run_app()
    else:
        print("👋 再见!")

if __name__ == "__main__":
    main() 
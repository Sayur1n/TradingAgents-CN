#!/usr/bin/env python3
"""
Pandoc安装脚本
自动安装pandoc工具，用于报告导出功能
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pandoc():
    """检查pandoc是否已安装"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ Pandoc已安装: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    print("❌ Pandoc未安装")
    return False

def install_pandoc_python():
    """使用pypandoc下载pandoc"""
    try:
        import pypandoc
        print("🔄 正在使用pypandoc下载pandoc...")
        pypandoc.download_pandoc()
        print("✅ Pandoc下载成功！")
        return True
    except ImportError:
        print("❌ pypandoc未安装，请先运行: pip install pypandoc")
        return False
    except Exception as e:
        print(f"❌ Pandoc下载失败: {e}")
        return False

def install_pandoc_system():
    """使用系统包管理器安装pandoc"""
    system = platform.system().lower()
    
    if system == "windows":
        return install_pandoc_windows()
    elif system == "darwin":  # macOS
        return install_pandoc_macos()
    elif system == "linux":
        return install_pandoc_linux()
    else:
        print(f"❌ 不支持的操作系统: {system}")
        return False

def install_pandoc_windows():
    """在Windows上安装pandoc"""
    print("🔄 尝试在Windows上安装pandoc...")
    
    # 尝试使用Chocolatey
    try:
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用Chocolatey安装pandoc...")
            result = subprocess.run(['choco', 'install', 'pandoc', '-y'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Pandoc安装成功！")
                return True
            else:
                print(f"❌ Chocolatey安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ Chocolatey未安装")
    
    # 尝试使用winget
    try:
        result = subprocess.run(['winget', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用winget安装pandoc...")
            result = subprocess.run(['winget', 'install', 'JohnMacFarlane.Pandoc'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Pandoc安装成功！")
                return True
            else:
                print(f"❌ winget安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ winget未安装")
    
    print("❌ 系统包管理器安装失败")
    return False

def install_pandoc_macos():
    """在macOS上安装pandoc"""
    print("🔄 尝试在macOS上安装pandoc...")
    
    # 尝试使用Homebrew
    try:
        result = subprocess.run(['brew', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用Homebrew安装pandoc...")
            result = subprocess.run(['brew', 'install', 'pandoc'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Pandoc安装成功！")
                return True
            else:
                print(f"❌ Homebrew安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ Homebrew未安装")
    
    print("❌ 系统包管理器安装失败")
    return False

def install_pandoc_linux():
    """在Linux上安装pandoc"""
    print("🔄 尝试在Linux上安装pandoc...")
    
    # 尝试使用apt (Ubuntu/Debian)
    try:
        result = subprocess.run(['apt', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用apt安装pandoc...")
            result = subprocess.run(['sudo', 'apt-get', 'update'], 
                                  capture_output=True, text=True, timeout=120)
            result = subprocess.run(['sudo', 'apt-get', 'install', '-y', 'pandoc'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Pandoc安装成功！")
                return True
            else:
                print(f"❌ apt安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # 尝试使用yum (CentOS/RHEL)
    try:
        result = subprocess.run(['yum', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用yum安装pandoc...")
            result = subprocess.run(['sudo', 'yum', 'install', '-y', 'pandoc'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Pandoc安装成功！")
                return True
            else:
                print(f"❌ yum安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ 系统包管理器安装失败")
    return False

def main():
    """主函数"""
    print("🔧 Pandoc安装脚本")
    print("=" * 50)
    
    # 检查是否已安装
    if check_pandoc():
        print("✅ Pandoc已可用，无需安装")
        return True
    
    print("\n🔄 开始安装pandoc...")
    
    # 方法1: 使用pypandoc下载
    print("\n📦 方法1: 使用pypandoc下载")
    if install_pandoc_python():
        if check_pandoc():
            return True
    
    # 方法2: 使用系统包管理器
    print("\n🖥️ 方法2: 使用系统包管理器")
    if install_pandoc_system():
        if check_pandoc():
            return True
    
    # 安装失败
    print("\n❌ 所有安装方法都失败了")
    print("\n📖 手动安装指南:")
    print("1. 访问 https://github.com/jgm/pandoc/releases")
    print("2. 下载适合您系统的安装包")
    print("3. 按照官方文档安装")
    print("4. 确保pandoc在系统PATH中")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

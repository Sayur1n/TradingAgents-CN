#!/usr/bin/env python3
"""
PDF工具安装脚本
自动安装PDF生成所需的工具
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_tool(command, name):
    """检查工具是否已安装"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {name}已安装: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    print(f"❌ {name}未安装")
    return False

def install_wkhtmltopdf():
    """安装wkhtmltopdf"""
    system = platform.system().lower()
    
    print(f"🔄 正在为{system}安装wkhtmltopdf...")
    
    if system == "windows":
        return install_wkhtmltopdf_windows()
    elif system == "darwin":  # macOS
        return install_wkhtmltopdf_macos()
    elif system == "linux":
        return install_wkhtmltopdf_linux()
    else:
        print(f"❌ 不支持的操作系统: {system}")
        return False

def install_wkhtmltopdf_windows():
    """在Windows上安装wkhtmltopdf"""
    # 尝试使用Chocolatey
    try:
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用Chocolatey安装wkhtmltopdf...")
            result = subprocess.run(['choco', 'install', 'wkhtmltopdf', '-y'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ wkhtmltopdf安装成功！")
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
            print("🔄 使用winget安装wkhtmltopdf...")
            result = subprocess.run(['winget', 'install', 'wkhtmltopdf.wkhtmltopdf'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ wkhtmltopdf安装成功！")
                return True
            else:
                print(f"❌ winget安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ winget未安装")
    
    print("❌ 自动安装失败，请手动下载安装")
    print("📥 下载地址: https://wkhtmltopdf.org/downloads.html")
    return False

def install_wkhtmltopdf_macos():
    """在macOS上安装wkhtmltopdf"""
    try:
        result = subprocess.run(['brew', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用Homebrew安装wkhtmltopdf...")
            result = subprocess.run(['brew', 'install', 'wkhtmltopdf'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ wkhtmltopdf安装成功！")
                return True
            else:
                print(f"❌ Homebrew安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ Homebrew未安装")
    
    print("❌ 自动安装失败，请手动安装Homebrew或下载wkhtmltopdf")
    return False

def install_wkhtmltopdf_linux():
    """在Linux上安装wkhtmltopdf"""
    # 尝试使用apt
    try:
        result = subprocess.run(['apt', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用apt安装wkhtmltopdf...")
            subprocess.run(['sudo', 'apt-get', 'update'], 
                          capture_output=True, text=True, timeout=120)
            result = subprocess.run(['sudo', 'apt-get', 'install', '-y', 'wkhtmltopdf'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ wkhtmltopdf安装成功！")
                return True
            else:
                print(f"❌ apt安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # 尝试使用yum
    try:
        result = subprocess.run(['yum', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("🔄 使用yum安装wkhtmltopdf...")
            result = subprocess.run(['sudo', 'yum', 'install', '-y', 'wkhtmltopdf'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ wkhtmltopdf安装成功！")
                return True
            else:
                print(f"❌ yum安装失败: {result.stderr}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ 自动安装失败，请手动安装")
    return False

def test_pdf_generation():
    """测试PDF生成功能"""
    print("\n🧪 测试PDF生成功能...")
    
    try:
        import pypandoc
        
        test_markdown = """# PDF测试报告

## 基本信息
- **测试时间**: 2025-01-12
- **测试目的**: 验证PDF生成功能

## 测试内容
这是一个测试文档，用于验证PDF生成是否正常工作。

### 中文支持测试
- 中文字符显示测试
- **粗体中文**
- *斜体中文*

### 表格测试
| 项目 | 数值 | 状态 |
|------|------|------|
| 测试1 | 100% | ✅ |
| 测试2 | 95% | ✅ |

---
*测试完成*
"""
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            output_file = tmp_file.name
        
        # 尝试生成PDF
        pypandoc.convert_text(
            test_markdown,
            'pdf',
            format='markdown',
            outputfile=output_file,
            extra_args=[
                '--pdf-engine=wkhtmltopdf',
                '-V', 'geometry:margin=2cm'
            ]
        )
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            file_size = os.path.getsize(output_file)
            print(f"✅ PDF生成测试成功！文件大小: {file_size} 字节")
            
            # 清理测试文件
            os.unlink(output_file)
            return True
        else:
            print("❌ PDF文件生成失败")
            return False
            
    except Exception as e:
        print(f"❌ PDF生成测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 PDF工具安装脚本")
    print("=" * 50)
    
    # 检查当前状态
    print("📋 检查当前工具状态...")
    wkhtmltopdf_installed = check_tool('wkhtmltopdf', 'wkhtmltopdf')
    
    if wkhtmltopdf_installed:
        print("\n✅ wkhtmltopdf已安装，测试PDF生成功能...")
        if test_pdf_generation():
            print("🎉 PDF功能完全正常！")
            return True
        else:
            print("⚠️ wkhtmltopdf已安装但PDF生成失败，可能需要重新安装")
    
    # 安装wkhtmltopdf
    print("\n🔄 开始安装wkhtmltopdf...")
    if install_wkhtmltopdf():
        print("\n🧪 测试安装结果...")
        if check_tool('wkhtmltopdf', 'wkhtmltopdf'):
            if test_pdf_generation():
                print("🎉 安装成功，PDF功能正常！")
                return True
            else:
                print("⚠️ 安装成功但PDF生成仍有问题")
        else:
            print("❌ 安装后仍无法找到wkhtmltopdf")
    
    # 提供手动安装指导
    print("\n📖 手动安装指导:")
    print("1. 访问 https://wkhtmltopdf.org/downloads.html")
    print("2. 下载适合您系统的安装包")
    print("3. 按照说明安装")
    print("4. 确保wkhtmltopdf在系统PATH中")
    print("5. 重新运行此脚本测试")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

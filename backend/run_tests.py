#!/usr/bin/env python3
"""
测试运行脚本
"""

import sys
import subprocess
import os
from pathlib import Path

def run_tests():
    """运行所有测试"""
    print("🧪 开始运行测试...")
    print("=" * 50)
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    tests_dir = project_root / "tests"
    
    # 检查tests目录是否存在
    if not tests_dir.exists():
        print("❌ tests目录不存在")
        return False
    
    # 运行pytest，跳过需要API的测试
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(tests_dir),
            "-v",
            "--tb=short",
            "--color=yes",
            "-m", "not api"  # 跳过需要API的测试
        ], capture_output=True, text=True, cwd=project_root)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def run_specific_test(test_name):
    """运行特定测试"""
    print(f"🧪 运行特定测试: {test_name}")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    test_file = project_root / "tests" / f"test_{test_name}.py"
    
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_file),
            "-v",
            "--tb=short",
            "--color=yes"
        ], capture_output=True, text=True, cwd=project_root)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def run_config_validation():
    """运行配置验证"""
    print("🔧 运行配置验证...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "tests/test_config.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行配置验证时出错: {e}")
        return False

def run_api_test():
    """运行API测试"""
    print("🤖 运行API测试...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "tests/test_qwen_api.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行API测试时出错: {e}")
        return False

def run_api_tests():
    """运行所有API测试（包括需要真实API密钥的测试）"""
    print("🤖 运行API测试（需要真实API密钥）...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_qwen_api.py",
            "-v",
            "--tb=short",
            "--color=yes",
            "-m", "api"  # 只运行API测试
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行API测试时出错: {e}")
        return False

def run_smart_chunking_test():
    """运行智能分片测试"""
    print("🧠 运行智能分片测试...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "tests/test_smart_chunking.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行智能分片测试时出错: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "all":
            success = run_tests()
        elif command == "config":
            success = run_config_validation()
        elif command == "api":
            success = run_api_test()
        elif command == "chunking":
            success = run_smart_chunking_test()
        elif command == "unit":
            success = run_specific_test("pdf_service") and run_specific_test("report_service")
        elif command == "api":
            success = run_api_tests()
        else:
            success = run_specific_test(command)
    else:
        # 默认运行所有测试
        success = run_tests()
    
    if success:
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print("\n❌ 测试失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
"""
测试辅助工具类
提供常用的测试工具函数
"""

import json
import yaml
import time
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class TestHelpers:
    """测试辅助工具类"""

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱地址"""
        username = TestHelpers.generate_random_string(8)
        domains = ['example.com', 'test.com', 'demo.org']
        domain = random.choice(domains)
        return f"{username}@{domain}"

    @staticmethod
    def generate_random_phone() -> str:
        """生成随机手机号"""
        prefixes = ['138', '139', '150', '151', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"

    @staticmethod
    def generate_timestamp(days_offset: int = 0) -> str:
        """生成时间戳"""
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.isoformat()

    @staticmethod
    def load_test_data(file_path: str) -> Dict[str, Any]:
        """加载测试数据文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif file_path.endswith('.json'):
                    return json.load(f)
                else:
                    raise ValueError(f"不支持的文件格式: {file_path}")
        except Exception as e:
            print(f"加载测试数据失败: {e}")
            return {}

    @staticmethod
    def validate_response_structure(response: Dict[str, Any], expected_keys: List[str]) -> bool:
        """验证响应结构"""
        for key in expected_keys:
            if key not in response:
                return False
        return True

    @staticmethod
    def extract_json_value(data: Dict[str, Any], path: str) -> Any:
        """从JSON中提取值（支持点号路径）"""
        keys = path.split('.')
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: int = 1) -> bool:
        """等待条件满足"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False

    @staticmethod
    def create_test_file(file_path: str, content: str = "测试文件内容") -> bool:
        """创建测试文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建测试文件失败: {e}")
            return False

    @staticmethod
    def cleanup_test_files(file_paths: List[str]) -> None:
        """清理测试文件"""
        import os
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"删除文件失败 {file_path}: {e}")

class DataGenerator:
    """测试数据生成器"""

    @staticmethod
    def generate_user_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成用户测试数据"""
        users = []
        for i in range(count):
            user = {
                'id': i + 1,
                'name': f"测试用户{i+1:03d}",
                'email': TestHelpers.generate_random_email(),
                'phone': TestHelpers.generate_random_phone(),
                'age': random.randint(18, 65),
                'department': random.choice(['技术部', '产品部', '运营部', '市场部']),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 365))
            }
            users.append(user)
        return users

    @staticmethod
    def generate_product_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成产品测试数据"""
        products = []
        categories = ['电子产品', '服装', '食品', '图书', '家居']

        for i in range(count):
            product = {
                'id': i + 1,
                'name': f"测试产品{i+1:03d}",
                'description': f"这是第{i+1}个测试产品的描述",
                'price': round(random.uniform(10.0, 1000.0), 2),
                'category': random.choice(categories),
                'stock': random.randint(0, 100),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 30))
            }
            products.append(product)
        return products

class AssertionHelpers:
    """断言辅助工具"""

    @staticmethod
    def assert_status_code(actual: int, expected: int) -> bool:
        """断言状态码"""
        return actual == expected

    @staticmethod
    def assert_response_time(actual: float, max_time: float) -> bool:
        """断言响应时间"""
        return actual <= max_time

    @staticmethod
    def assert_json_contains(response: Dict[str, Any], expected_data: Dict[str, Any]) -> bool:
        """断言JSON包含指定数据"""
        for key, value in expected_data.items():
            if key not in response or response[key] != value:
                return False
        return True

    @staticmethod
    def assert_array_length(array: List[Any], expected_length: int) -> bool:
        """断言数组长度"""
        return len(array) == expected_length

    @staticmethod
    def assert_string_contains(text: str, substring: str) -> bool:
        """断言字符串包含子串"""
        return substring in text

# 使用示例
if __name__ == "__main__":
    # 生成测试数据示例
    print("生成用户数据:")
    users = DataGenerator.generate_user_data(3)
    for user in users:
        print(f"  {user}")

    print("\n生成产品数据:")
    products = DataGenerator.generate_product_data(2)
    for product in products:
        print(f"  {product}")

    # 工具函数示例
    print(f"\n随机字符串: {TestHelpers.generate_random_string()}")
    print(f"随机邮箱: {TestHelpers.generate_random_email()}")
    print(f"随机手机: {TestHelpers.generate_random_phone()}")
    print(f"当前时间戳: {TestHelpers.generate_timestamp()}")

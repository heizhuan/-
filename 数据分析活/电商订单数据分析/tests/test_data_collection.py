"""数据采集服务测试

测试数据采集、清洗和验证功能。
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from app.services.data_collection import DataCollectionService

class TestDataCollectionService(unittest.TestCase):
    """测试数据采集服务类"""
    
    def setUp(self):
        """测试前准备"""
        self.config = {
            'data': {
                'input_path': 'data/raw',
                'output_path': 'data/processed'
            }
        }
        self.service = DataCollectionService(self.config)
        
        # 创建测试数据
        self.test_data = pd.DataFrame({
            'order_id': ['A001', 'A002', 'A003', 'A002'],  # A002是重复的
            'customer_id': ['C001', 'C002', None, 'C002'],  # 包含缺失值
            'product_id': ['P001', 'P002', 'P003', 'P002'],
            'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-02'],
            'quantity': [2, -1, 3, 0],  # 包含无效值
            'price': [100.0, 200.0, 300.0, 200.0]
        })
    
    def test_clean_order_data(self):
        """测试数据清洗功能"""
        # 执行清洗
        cleaned_df = self.service.clean_order_data(self.test_data)
        
        # 验证结果
        self.assertEqual(len(cleaned_df), 2)  # 应该只剩下2条有效记录
        self.assertFalse(cleaned_df['customer_id'].isnull().any())  # 不应该有缺失值
        self.assertTrue((cleaned_df['quantity'] > 0).all())  # 数量应该都大于0
        self.assertTrue((cleaned_df['price'] > 0).all())  # 价格应该都大于0
        self.assertTrue('total_amount' in cleaned_df.columns)  # 应该有总金额列
        
    def test_validate_data_quality(self):
        """测试数据质量验证功能"""
        # 先清洗数据
        cleaned_df = self.service.clean_order_data(self.test_data)
        
        # 执行验证
        report = self.service.validate_data_quality(cleaned_df)
        
        # 验证报告内容
        self.assertIn('total_records', report)
        self.assertIn('duplicate_records', report)
        self.assertIn('missing_values', report)
        self.assertIn('numerical_stats', report)
        self.assertIn('temporal_stats', report)
        
    def test_process_batch_data(self):
        """测试批量数据处理功能"""
        # 保存测试数据到临时文件
        input_path = 'data/test_input.csv'
        output_path = 'data/test_output.csv'
        self.test_data.to_csv(input_path, index=False)
        
        try:
            # 执行批处理
            self.service.process_batch_data(input_path, output_path)
            
            # 验证输出文件
            processed_df = pd.read_csv(output_path)
            self.assertGreater(len(processed_df), 0)
            self.assertTrue('total_amount' in processed_df.columns)
            
        finally:
            # 清理测试文件
            import os
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)

if __name__ == '__main__':
    unittest.main() 
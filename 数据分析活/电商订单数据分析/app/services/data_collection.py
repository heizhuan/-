"""数据采集服务

负责从各种数据源收集数据，包括：
1. CSV文件导入
2. 数据库导入
3. 实时数据采集
4. 数据清洗和转换
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataCollectionService:
    """数据采集服务类"""
    
    def __init__(self, config: Dict):
        """初始化数据采集服务
        
        Args:
            config: 配置信息字典
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def load_csv_data(self, file_path: str) -> pd.DataFrame:
        """加载CSV文件数据
        
        Args:
            file_path: CSV文件路径
            
        Returns:
            DataFrame: 加载的数据
        """
        try:
            self.logger.info(f"开始加载CSV文件: {file_path}")
            df = pd.read_csv(file_path)
            self.logger.info(f"CSV文件加载完成，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"CSV文件加载失败: {str(e)}")
            raise
    
    def clean_order_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗订单数据
        
        Args:
            df: 原始订单数据DataFrame
            
        Returns:
            DataFrame: 清洗后的数据
        """
        try:
            self.logger.info("开始清洗订单数据")
            
            # 1. 删除重复记录
            df = df.drop_duplicates()
            
            # 2. 处理缺失值
            df = df.fillna({
                'customer_id': 'unknown',
                'product_id': 'unknown',
                'quantity': 0,
                'price': 0.0
            })
            
            # 3. 数据类型转换
            df['order_date'] = pd.to_datetime(df['order_date'])
            df['quantity'] = df['quantity'].astype(int)
            df['price'] = df['price'].astype(float)
            
            # 4. 添加新特征
            df['total_amount'] = df['quantity'] * df['price']
            df['year'] = df['order_date'].dt.year
            df['month'] = df['order_date'].dt.month
            df['day'] = df['order_date'].dt.day
            df['day_of_week'] = df['order_date'].dt.dayofweek
            
            # 5. 删除异常值
            df = df[df['quantity'] > 0]
            df = df[df['price'] > 0]
            
            self.logger.info(f"数据清洗完成，剩余 {len(df)} 条记录")
            return df
            
        except Exception as e:
            self.logger.error(f"数据清洗失败: {str(e)}")
            raise
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """验证数据质量
        
        Args:
            df: 待验证的数据DataFrame
            
        Returns:
            Dict: 数据质量报告
        """
        try:
            self.logger.info("开始数据质量验证")
            
            report = {
                'total_records': len(df),
                'duplicate_records': len(df) - len(df.drop_duplicates()),
                'missing_values': df.isnull().sum().to_dict(),
                'value_counts': {
                    col: df[col].value_counts().to_dict() 
                    for col in ['customer_id', 'product_id']
                },
                'numerical_stats': {
                    'quantity': df['quantity'].describe().to_dict(),
                    'price': df['price'].describe().to_dict(),
                    'total_amount': df['total_amount'].describe().to_dict()
                },
                'temporal_stats': {
                    'date_range': {
                        'start': df['order_date'].min().strftime('%Y-%m-%d'),
                        'end': df['order_date'].max().strftime('%Y-%m-%d')
                    },
                    'orders_by_year': df.groupby('year').size().to_dict(),
                    'orders_by_month': df.groupby('month').size().to_dict(),
                    'orders_by_day_of_week': df.groupby('day_of_week').size().to_dict()
                }
            }
            
            self.logger.info("数据质量验证完成")
            return report
            
        except Exception as e:
            self.logger.error(f"数据质量验证失败: {str(e)}")
            raise
    
    def process_batch_data(self, input_path: str, output_path: str) -> None:
        """处理批量数据
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
        """
        try:
            # 1. 加载数据
            df = self.load_csv_data(input_path)
            
            # 2. 清洗数据
            df_cleaned = self.clean_order_data(df)
            
            # 3. 验证数据质量
            quality_report = self.validate_data_quality(df_cleaned)
            
            # 4. 保存处理后的数据
            df_cleaned.to_csv(output_path, index=False)
            self.logger.info(f"数据已保存到: {output_path}")
            
            # 5. 记录处理信息
            self.logger.info(f"数据处理完成，质量报告: {quality_report}")
            
        except Exception as e:
            self.logger.error(f"批量数据处理失败: {str(e)}")
            raise 
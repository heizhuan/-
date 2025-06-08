"""订单数据模型

定义订单相关的数据结构和方法。
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class Order:
    """订单数据类"""
    
    # 基本信息
    order_id: str
    customer_id: str
    order_date: datetime
    
    # 商品信息
    product_id: str
    quantity: int
    price: float
    
    # 计算字段
    total_amount: float = 0.0
    
    # 时间特征
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    day_of_week: Optional[int] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 计算总金额
        self.total_amount = self.quantity * self.price
        
        # 提取时间特征
        self.year = self.order_date.year
        self.month = self.order_date.month
        self.day = self.order_date.day
        self.day_of_week = self.order_date.weekday()
    
    @property
    def is_valid(self) -> bool:
        """验证订单是否有效"""
        return (
            self.quantity > 0 and
            self.price > 0 and
            self.total_amount > 0
        )
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'total_amount': self.total_amount,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'day_of_week': self.day_of_week
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """从字典创建订单对象"""
        return cls(
            order_id=data['order_id'],
            customer_id=data['customer_id'],
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d %H:%M:%S'),
            product_id=data['product_id'],
            quantity=int(data['quantity']),
            price=float(data['price'])
        ) 
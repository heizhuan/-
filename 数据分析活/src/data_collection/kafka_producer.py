from kafka import KafkaProducer
import json
import time
import pandas as pd
from typing import Dict, List
import sys
sys.path.append("../../")
from config.kafka_config import PRODUCER_CONFIG

class OrderDataProducer:
    def __init__(self, bootstrap_servers: str):
        """
        初始化Kafka生产者
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
    def send_order_data(self, topic: str, data: Dict):
        """
        发送订单数据到Kafka
        """
        try:
            future = self.producer.send(topic, value=data)
            future.get(timeout=10)  # 等待发送完成
            print(f"成功发送数据: {data}")
        except Exception as e:
            print(f"发送数据失败: {str(e)}")
            
    def process_csv_file(self, file_path: str, topic: str):
        """
        处理CSV文件并发送数据
        """
        try:
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                data = row.to_dict()
                self.send_order_data(topic, data)
                time.sleep(0.1)  # 控制发送速率
        except Exception as e:
            print(f"处理CSV文件失败: {str(e)}")
            
    def close(self):
        """
        关闭生产者连接
        """
        self.producer.close()

def main():
    producer = OrderDataProducer(PRODUCER_CONFIG['bootstrap_servers'])
    try:
        producer.process_csv_file(
            '../../data/raw/tmall_order_report.csv',
            'ecommerce_orders'
        )
    finally:
        producer.close()

if __name__ == "__main__":
    main() 
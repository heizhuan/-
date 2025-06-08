# Kafka配置参数
KAFKA_CONFIG = {
    'bootstrap_servers': 'localhost:9092',
    'topic_name': 'ecommerce_orders',
    'group_id': 'ecommerce_group',
    'auto_offset_reset': 'latest',
    'enable_auto_commit': True,
    'batch_size': 1000,
    'linger_ms': 10
}

# Kafka生产者配置
PRODUCER_CONFIG = {
    'bootstrap_servers': 'localhost:9092',
    'acks': 'all',
    'retries': 3,
    'batch_size': 16384,
    'linger_ms': 1,
    'buffer_memory': 33554432
}

# Kafka消费者配置
CONSUMER_CONFIG = {
    'bootstrap_servers': 'localhost:9092',
    'group_id': 'ecommerce_group',
    'auto_offset_reset': 'latest',
    'enable_auto_commit': True,
    'auto_commit_interval_ms': 1000,
    'session_timeout_ms': 30000
} 
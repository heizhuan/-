# 电商订单大数据分析系统

## 项目结构
```
ecommerce_analysis/
├── data/                      # 数据目录
│   ├── raw/                  # 原始数据
│   ├── processed/            # 处理后的数据
│   └── output/               # 输出结果
├── src/                      # 源代码
│   ├── data_collection/     # 数据采集模块
│   │   ├── kafka_producer.py
│   │   └── file_collector.py
│   ├── data_processing/     # 数据处理模块
│   │   ├── spark_processor.py
│   │   └── data_cleaner.py
│   ├── data_storage/        # 数据存储模块
│   │   ├── hdfs_operations.py
│   │   └── hive_operations.py
│   ├── analysis/           # 数据分析模块
│   │   ├── sales_analysis.py
│   │   └── user_behavior.py
│   └── visualization/      # 可视化模块
│       ├── dashboard.py
│       └── report_generator.py
├── config/                  # 配置文件
│   ├── spark_config.py
│   └── kafka_config.py
├── notebooks/              # Jupyter notebooks
│   └── analysis_notebooks/
├── tests/                  # 测试代码
└── requirements.txt        # 项目依赖
```

## 技术栈
- Apache Hadoop 3.x
- Apache Spark 3.x
- Apache Kafka
- Apache Hive
- Python 3.8+
- PySpark
- Jupyter Notebook 
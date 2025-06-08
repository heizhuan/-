from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys
sys.path.append("../../")
from config.spark_config import create_spark_session

class OrderDataProcessor:
    def __init__(self):
        """
        初始化Spark处理器
        """
        self.spark = create_spark_session()
        
    def process_streaming_data(self):
        """
        处理Kafka流数据
        """
        # 定义schema
        schema = StructType([
            StructField("订单编号", IntegerType(), True),
            StructField("总金额", DoubleType(), True),
            StructField("买家实际支付金额", DoubleType(), True),
            StructField("收货地址", StringType(), True),
            StructField("订单创建时间", StringType(), True),
            StructField("订单付款时间", StringType(), True),
            StructField("退款金额", DoubleType(), True)
        ])

        # 读取Kafka流数据
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "ecommerce_orders") \
            .load()

        # 解析JSON数据
        parsed_df = df.select(
            from_json(col("value").cast("string"), schema).alias("data")
        ).select("data.*")

        # 数据清洗和转换
        processed_df = parsed_df \
            .withColumn("订单创建时间", to_timestamp("订单创建时间")) \
            .withColumn("订单付款时间", to_timestamp("订单付款时间")) \
            .withColumn("收货地址", regexp_replace("收货地址", "自治区|维吾尔|回族|壮族|省", ""))

        # 计算实时指标
        result_df = processed_df \
            .withWatermark("订单创建时间", "1 hour") \
            .groupBy(
                window("订单创建时间", "1 hour"),
                "收货地址"
            ) \
            .agg(
                count("订单编号").alias("订单数"),
                sum("总金额").alias("总金额"),
                sum("退款金额").alias("退款金额"),
                avg("买家实际支付金额").alias("平均支付金额")
            )

        # 输出到控制台（用于测试）
        query = result_df \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .start()

        # 输出到Hive表
        query_hive = result_df \
            .writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("path", "hdfs://localhost:9000/user/hive/warehouse/order_analysis") \
            .option("checkpointLocation", "hdfs://localhost:9000/user/hive/warehouse/checkpoints") \
            .start()

        query.awaitTermination()
        query_hive.awaitTermination()

    def process_batch_data(self, input_path):
        """
        处理批量数据
        """
        # 读取CSV文件
        df = self.spark.read.csv(input_path, header=True, inferSchema=True)
        
        # 数据清洗和转换
        processed_df = df \
            .withColumn("订单创建时间", to_timestamp("订单创建时间")) \
            .withColumn("订单付款时间", to_timestamp("订单付款时间")) \
            .withColumn("收货地址", regexp_replace("收货地址", "自治区|维吾尔|回族|壮族|省", ""))

        # 注册临时视图
        processed_df.createOrReplaceTempView("orders")

        # 执行分析
        daily_stats = self.spark.sql("""
            SELECT 
                DATE(订单创建时间) as 日期,
                COUNT(*) as 订单数,
                SUM(总金额) as 总金额,
                SUM(退款金额) as 退款金额,
                AVG(买家实际支付金额) as 平均支付金额
            FROM orders 
            GROUP BY DATE(订单创建时间)
            ORDER BY 日期
        """)

        return daily_stats

def main():
    processor = OrderDataProcessor()
    # 处理流数据
    processor.process_streaming_data()
    
    # 处理批量数据
    # stats = processor.process_batch_data("../../data/raw/tmall_order_report.csv")
    # stats.show()

if __name__ == "__main__":
    main() 
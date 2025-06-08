from pyspark.sql import SparkSession

def create_spark_session():
    """
    创建SparkSession实例
    """
    return SparkSession.builder \
        .appName("E-commerce Analysis") \
        .config("spark.sql.warehouse.dir", "hdfs://localhost:9000/user/hive/warehouse") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "100") \
        .enableHiveSupport() \
        .getOrCreate()

# Spark配置参数
SPARK_CONFIGS = {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.localShuffleReader.enabled": "true"
} 
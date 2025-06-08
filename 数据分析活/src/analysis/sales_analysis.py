from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import sys
sys.path.append("../../")
from config.spark_config import create_spark_session

class SalesAnalyzer:
    def __init__(self):
        """
        初始化销售分析器
        """
        self.spark = create_spark_session()
        
    def analyze_sales_trends(self):
        """
        分析销售趋势
        """
        # 从Hive表读取数据
        df = self.spark.sql("""
            SELECT 
                window.start as 时间窗口开始,
                window.end as 时间窗口结束,
                收货地址,
                订单数,
                总金额,
                退款金额,
                平均支付金额
            FROM order_analysis
            ORDER BY 时间窗口开始
        """)
        
        return df
        
    def predict_sales(self, days_ahead=7):
        """
        预测未来销售
        """
        # 准备训练数据
        df = self.spark.sql("""
            SELECT 
                DAYOFWEEK(日期) as 星期,
                MONTH(日期) as 月份,
                订单数,
                总金额,
                平均支付金额
            FROM (
                SELECT 
                    DATE(订单创建时间) as 日期,
                    COUNT(*) as 订单数,
                    SUM(总金额) as 总金额,
                    AVG(买家实际支付金额) as 平均支付金额
                FROM orders 
                GROUP BY DATE(订单创建时间)
            )
        """)
        
        # 特征工程
        assembler = VectorAssembler(
            inputCols=["星期", "月份", "订单数", "平均支付金额"],
            outputCol="features"
        )
        
        # 准备训练数据
        data = assembler.transform(df).select("features", col("总金额").alias("label"))
        
        # 划分训练集和测试集
        train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)
        
        # 训练线性回归模型
        lr = LinearRegression(
            featuresCol="features",
            labelCol="label",
            maxIter=10,
            regParam=0.3,
            elasticNetParam=0.8
        )
        
        model = lr.fit(train_data)
        
        # 评估模型
        predictions = model.transform(test_data)
        evaluator = RegressionEvaluator(
            labelCol="label",
            predictionCol="prediction",
            metricName="rmse"
        )
        
        rmse = evaluator.evaluate(predictions)
        print(f"均方根误差: {rmse}")
        
        return model, rmse
        
    def analyze_regional_sales(self):
        """
        分析地区销售情况
        """
        df = self.spark.sql("""
            SELECT 
                收货地址,
                COUNT(*) as 订单数,
                SUM(总金额) as 总金额,
                SUM(退款金额) as 退款金额,
                AVG(买家实际支付金额) as 平均支付金额,
                COUNT(CASE WHEN 退款金额 > 0 THEN 1 END) as 退款订单数
            FROM orders 
            GROUP BY 收货地址
            ORDER BY 订单数 DESC
        """)
        
        return df

def main():
    analyzer = SalesAnalyzer()
    
    # 分析销售趋势
    trends = analyzer.analyze_sales_trends()
    trends.show()
    
    # 预测销售
    model, rmse = analyzer.predict_sales()
    print(f"销售预测模型RMSE: {rmse}")
    
    # 分析地区销售
    regional = analyzer.analyze_regional_sales()
    regional.show()

if __name__ == "__main__":
    main() 
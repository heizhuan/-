import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Map, Pie
from pyecharts.globals import ThemeType
import sys
sys.path.append("../../")
from config.spark_config import create_spark_session

class SalesDashboard:
    def __init__(self):
        """
        初始化仪表板
        """
        self.spark = create_spark_session()
        st.set_page_config(page_title="电商销售分析仪表板", layout="wide")
        
    def load_data(self):
        """
        加载数据
        """
        # 从Hive读取数据
        sales_trends = self.spark.sql("""
            SELECT * FROM order_analysis
            ORDER BY window.start DESC
            LIMIT 24
        """).toPandas()
        
        regional_sales = self.spark.sql("""
            SELECT 
                收货地址,
                COUNT(*) as 订单数,
                SUM(总金额) as 总金额
            FROM orders 
            GROUP BY 收货地址
        """).toPandas()
        
        return sales_trends, regional_sales
        
    def create_sales_trend_chart(self, data):
        """
        创建销售趋势图
        """
        line = (
            Line()
            .add_xaxis(data['时间窗口开始'].tolist())
            .add_yaxis("总金额", data['总金额'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="销售趋势"),
                xaxis_opts=opts.AxisOpts(type_="time"),
                yaxis_opts=opts.AxisOpts(type_="value"),
                datazoom_opts=[opts.DataZoomOpts()],
            )
        )
        return line
        
    def create_regional_map(self, data):
        """
        创建地区销售分布图
        """
        map_chart = (
            Map()
            .add("订单数", [list(z) for z in zip(data['收货地址'], data['订单数'])], "china")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="地区订单分布"),
                visualmap_opts=opts.VisualMapOpts(),
            )
        )
        return map_chart
        
    def run_dashboard(self):
        """
        运行仪表板
        """
        st.title("电商销售分析仪表板")
        
        # 加载数据
        sales_trends, regional_sales = self.load_data()
        
        # 显示关键指标
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总订单数", f"{sales_trends['订单数'].sum():,.0f}")
        with col2:
            st.metric("总销售额", f"¥{sales_trends['总金额'].sum():,.2f}")
        with col3:
            st.metric("平均订单金额", f"¥{sales_trends['平均支付金额'].mean():,.2f}")
        with col4:
            st.metric("退款率", f"{(sales_trends['退款金额'].sum() / sales_trends['总金额'].sum()):,.2%}")
        
        # 显示销售趋势
        st.subheader("销售趋势")
        sales_trend_chart = self.create_sales_trend_chart(sales_trends)
        st.pyecharts_chart(sales_trend_chart)
        
        # 显示地区分布
        st.subheader("地区订单分布")
        regional_map = self.create_regional_map(regional_sales)
        st.pyecharts_chart(regional_map)
        
        # 显示详细数据表格
        st.subheader("详细数据")
        st.dataframe(sales_trends)

def main():
    dashboard = SalesDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 
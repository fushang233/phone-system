import streamlit as st
import pandas as pd

df=pd.read_csv("phone.csv",encoding="gb2312")


# if st.button("🔄 重置所有筛选条件"):
#     # 刷新页面，重置所有筛选状态
#     st.rerun()
#
# brand=st.selectbox("选择品牌",df["brand"].unique())
# #价格滑动条
# max_price=st.slider("只显示低于这个价格的手机",0,15000,5000)
# #电池滑动条
# min_battary=st.slider("最小电池容量（mAh)",3000,10000,5000)
# #处理器筛选下拉框
# cpu_options=df["cpu"].unique()
# select_cpu=st.selectbox("选择处理器型号",["全部"]+list(cpu_options))
with st.sidebar:
    st.header("筛选条件")
    if st.button("🔄 重置所有筛选条件"):
        st.rerun()
    brand = st.selectbox("选择品牌", df["brand"].unique())
    max_price = st.slider("只显示低于这个价格的手机", 0, 10000, 5000)
    min_battery = st.slider("最小电池容量（mAh）", 3000, 10000, 5000)
    cpu_options = df["cpu"].unique()
    select_cpu = st.selectbox("选择处理器型号", ["全部"] + list(cpu_options))

st.title("手机参数筛选系统")
st.subheader("欢迎使用手机参数查询工具")
st.write(f"当前数据库一共有：{len(df)}台手机")
# result=df[
#     (df["brand"]==brand)&
#     (df["price"]<=max_price)&
#     (df["battery"]>=min_battary)
#     ]
condition=(df["brand"]== brand)& \
          (df["price"]<=max_price)& \
          (df["battery"]>=min_battery)

if select_cpu !="全部":
    condition=condition &(df["cpu"]==select_cpu)

result=df[condition]

# result=result.drop(columns=["brand"])

st.subheader("筛选结果")
st.write(f"符合条件的手机一共有:{len(result)}台")

st.dataframe(
    result,
    column_config={
        #"brand": "品牌",
        "model":"型号",
        "price":"价格（元）",
        "battery":"电池容量（mAh）",
        "cpu":"处理器"
    },
    column_order=["model","price","battery","cpu"],
    hide_index=True,
    width=800
)

st.subheader("价格分布")
# 只有筛选结果>0时才显示图表，避免报错
if len(result) > 0:
    st.bar_chart(
        result,
        x="model",  # x轴：手机型号
        y="price",  # y轴：价格
        color="#ff6b6b"  # 图表颜色（红色，可选）
    )

    if len(result) > 0:
        # 把DataFrame转成CSV格式的字节流
        csv_data = result.to_csv(index=False, encoding="utf-8")
        # 下载按钮
        st.download_button(
            label="📥 导出筛选结果为CSV",
            data=csv_data,
            file_name=f"手机筛选结果_{brand}.csv",
            mime="text/csv"
        )
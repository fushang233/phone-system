import plotly.express as px
import streamlit as st
import pandas as pd

df=pd.read_csv("phone.csv",encoding="gb2312")

with st.sidebar:
    st.header("📊 系统导航")
    page = st.radio(
        "选择功能页面",
        ["🔍 手机筛选", "📈 数据看板"]
    )
    st.divider()
    st.info(f"数据集：{len(df)} 款手机")


# with st.sidebar:
#     st.divider()
#     st.write(f"📁 数据统计")
#     st.write(f"• 总记录数：{len(df)} 条")
#     st.write(f"• 品牌数量：{df['brand'].nunique()} 个")
#     st.write(f"• 价格范围：{df['price'].min()} - {df['price'].max()} 元")
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

    # if page == "🔍 手机筛选与对比":
    #     st.header("🎯 筛选条件")
if page == "🔍 手机筛选":
    st.title("手机参数筛选对比系统")
    with st.sidebar:
        st.header("🎯 筛选条件")
        if st.button("🔄 重置所有筛选条件"):
            st.rerun()
        brand_options = ["全部品牌"] + list(df["brand"].unique())
        brand = st.selectbox("选择品牌", brand_options)
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
    condition = pd.Series([True] * len(df))

    # 只有当用户没有选择“全部品牌”时，才添加品牌筛选条件
    if brand != "全部品牌":
        condition = condition & (df["brand"] == brand)

    # 其他条件保持不变
    condition = condition & (df["price"] <= max_price) & (df["battery"] >= min_battery)

    if select_cpu !="全部":
        condition=condition &(df["cpu"]==select_cpu)

    result=df[condition]

# result=result.drop(columns=["brand"])

    st.subheader("筛选结果")
    st.write(f"符合条件的手机一共有:{len(result)}台")

    # ========== 添加手机对比功能 ==========
    st.subheader("🔍 手机对比功能")

    if len(result) > 1:
        # 让用户选择要对比的手机
        compare_models = st.multiselect(
            "选择要对比的机型（最多3款）",
            options=result['model'].tolist(),
            max_selections=3
        )

        if len(compare_models) >= 2:
            compare_df = result[result['model'].isin(compare_models)]

            # 显示对比表格
            st.write("**详细参数对比**")

            # 创建一个并排显示的对比
            cols = st.columns(len(compare_models))

            for idx, (_, phone) in enumerate(compare_df.iterrows()):
                with cols[idx]:
                    st.markdown(f"**{phone['model']}**")
                    st.markdown(f"品牌：{phone['brand']}")
                    st.markdown(f"价格：{phone['price']}元")
                    st.markdown(f"电池：{phone['battery']}mAh")
                    st.markdown(f"CPU：{phone['cpu']}")

                    # 如果有ram和screen_size列
                    if 'ram' in phone:
                        st.markdown(f"内存：{phone['ram']}GB")
                    if 'screen_size' in phone:
                        st.markdown(f"屏幕：{phone['screen_size']}英寸")

            # 简单的价格对比柱状图
            st.subheader("价格对比")
            price_chart = compare_df[['model', 'price']].set_index('model')
            st.subheader("💰 价格对比")

            # 创建一行卡片
            cols = st.columns(len(compare_models))

            for idx, (_, phone) in enumerate(compare_df.iterrows()):
                with cols[idx]:
                    # 价格卡片
                    st.metric(
                        label=phone['model'],
                        value=f"{phone['price']:,.0f}元",  # 格式化显示
                        # 可以计算差价作为变化值
                        delta=f"比最低价高 {phone['price'] - compare_df['price'].min():,.0f}元" if phone['price'] >
                                                                                                   compare_df[
                                                                                                       'price'].min() else "最低价"
                    )

                    # 如果有其他参数想一起展示
                    st.caption(f"电池：{phone.get('battery', 'N/A')}mAh")
                    st.caption(f"内存：{phone.get('ram', 'N/A')}GB")

            # 添加一个简单的迷你条形图作为视觉辅助
            if len(compare_models) >= 2:
                st.caption("价格比例示意")
                max_price = compare_df['price'].max()
                for _, phone in compare_df.iterrows():
                    ratio = phone['price'] / max_price
                    st.progress(ratio, text=f"{phone['model']}: {phone['price']:,.0f}元")

            # 电池容量对比
            if 'battery' in compare_df.columns:
                st.subheader("🔋 电池容量对比")
                max_battery = compare_df['battery'].max()
                for _, phone in compare_df.sort_values('battery', ascending=False).iterrows():
                    ratio = phone['battery'] / max_battery
                    st.progress(
                        float(ratio),
                        text=f"{phone['model']}: {phone['battery']}mAh"
                    )
    else:
        st.info("对比功能需要至少2款符合条件的手机。")

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



    # 价格分布与数据导出
    st.subheader("价格分布与数据导出")

    if len(result) > 0:
        # 并排显示
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(result, x="model", y="price")

        with col2:
            # 显示统计信息
            st.metric("平均价格", f"{result['price'].mean():.0f} 元")
            st.metric("平均电池容量", f"{result['battery'].mean():.0f} mAh")
            st.metric("找到机型数量", len(result))

        # 下载按钮
        csv_data = result.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📥 导出筛选结果为CSV",
            data=csv_data,
            file_name=f"手机筛选结果.csv",
            mime="text/csv"
        )

elif page == "📈 数据看板":  # 这里处理数据看板页面！
    st.title("📊 手机市场数据分析看板")
    st.markdown("基于完整数据集的宏观市场分析")

    # 显示数据基本信息
    st.info(f"当前数据集包含 **{len(df)}** 款手机，涵盖 **{df['brand'].nunique()}** 个品牌")

    # --------------------------------------------------
    # 模块1：关键指标卡片
    # --------------------------------------------------
    st.subheader("📈 关键市场指标")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_price = df['price'].mean()
        st.metric(
            "市场平均价格",
            f"¥{avg_price:,.0f}",
            f"范围：¥{df['price'].min():,.0f}-¥{df['price'].max():,.0f}"
        )

    with col2:
        avg_battery = df['battery'].mean()
        st.metric(
            "平均电池容量",
            f"{avg_battery:,.0f}mAh",
            f"范围：{df['battery'].min():,.0f}-{df['battery'].max():,.0f}mAh"
        )

    with col3:
        brand_count = df['brand'].nunique()
        st.metric(
            "品牌数量",
            f"{brand_count}个",
            "涵盖主流品牌"
        )

    with col4:
        mid_range = len(df[(df['price'] >= 2000) & (df['price'] <= 4000)])
        mid_percent = (mid_range / len(df)) * 100
        st.metric(
            "中端机型占比",
            f"{mid_percent:.1f}%",
            f"{mid_range}款（2000-4000元）"
        )

    st.divider()

    # --------------------------------------------------
    # 模块2：品牌分析
    # --------------------------------------------------
    st.subheader("🏷️ 品牌维度分析")

    tab1, tab2, tab3 = st.tabs(["📊 品牌市场份额", "📦 价格分布对比", "🔋 电池容量对比"])

    with tab1:
        brand_counts = df['brand'].value_counts().reset_index()
        brand_counts.columns = ['品牌', '机型数量']

        fig1 = px.bar(
            brand_counts,
            x='品牌',
            y='机型数量',
            color='机型数量',
            text='机型数量',
            title="各品牌手机型号数量对比",
            color_continuous_scale='Blues'
        )
        fig1.update_traces(texttemplate='%{text}', textposition='outside')
        fig1.update_layout(xaxis_title="品牌", yaxis_title="机型数量")
        st.plotly_chart(fig1, use_container_width=True)

        st.caption("📌 图表说明：柱子越高表示该品牌在售型号越多，颜色越深表示数量越多。")

    with tab2:
        fig2 = px.box(
            df,
            x='brand',
            y='price',
            points="all",
            title="各品牌价格分布与离散程度",
            labels={'brand': '品牌', 'price': '价格（元）'}
        )
        fig2.update_traces(boxmean='sd')
        fig2.update_layout(
            xaxis_title="品牌",
            yaxis_title="价格（元）",
            yaxis_tickformat=',.0f'
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.caption("📌 箱线图说明：箱子表示中间50%的数据范围，线表示中位数，点表示具体机型。")

    with tab3:
        avg_battery_by_brand = df.groupby('brand')['battery'].mean().sort_values().reset_index()

        fig3 = px.bar(
            avg_battery_by_brand,
            x='battery',
            y='brand',
            orientation='h',
            color='battery',
            text='battery',
            title="各品牌平均电池容量对比",
            labels={'battery': '平均电池容量（mAh）', 'brand': '品牌'},
            color_continuous_scale='Greens'
        )
        fig3.update_traces(
            texttemplate='%{text:.0f}mAh',
            textposition='outside'
        )
        fig3.update_layout(xaxis_title="平均电池容量（mAh）", yaxis_title="品牌")
        st.plotly_chart(fig3, use_container_width=True)

        st.caption("📌 图表说明：条形越长表示该品牌手机平均电池容量越大。")

    st.divider()

    # --------------------------------------------------
    # 模块3：价格与电池相关性分析
    # --------------------------------------------------
    st.subheader("💰 价格-电池容量相关性分析")

    col_left, col_right = st.columns(2)

    with col_left:
        fig4 = px.scatter(
            df,
            x='price',
            y='battery',
            color='brand',
            hover_name='model',
            size='price',
            title="价格与电池容量关系散点图",
            labels={'price': '价格（元）', 'battery': '电池容量（mAh）'},
            # trendline="ols"
        )
        fig4.update_layout(xaxis_tickformat=',.0f', hovermode='closest')
        st.plotly_chart(fig4, use_container_width=True)

    with col_right:
        fig5 = px.histogram(
            df,
            x='price',
            nbins=20,
            title="手机价格分布",
            labels={'price': '价格（元）', 'count': '机型数量'},
            color_discrete_sequence=['#1f77b4']
        )
        fig5.update_layout(xaxis_tickformat=',.0f', bargap=0.1)
        st.plotly_chart(fig5, use_container_width=True)

        price_stats = df['price'].describe()
        st.metric(
            "最常见价格区间",
            f"¥{int(price_stats['25%']):,}-¥{int(price_stats['75%']):,}元",
            "中间50%机型集中在此范围"
        )

    st.divider()

    # --------------------------------------------------
    # 模块4：数据详情表格
    # --------------------------------------------------
    st.subheader("📋 完整数据一览")

    search_term = st.text_input("🔍 搜索手机型号或品牌", "")

    if search_term:
        display_df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
        st.write(f"找到 {len(display_df)} 条包含 **'{search_term}'** 的记录")
    else:
        display_df = df
        st.write(f"显示全部 {len(df)} 条记录")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "model": "型号",
            "brand": "品牌",
            "price": st.column_config.NumberColumn("价格", format="¥%d"),
            "battery": st.column_config.NumberColumn("电池", format="%d mAh"),
            "cpu": "处理器"
        }
    )

    csv_data = display_df.to_csv(index=False, encoding='utf-8')
    st.download_button(
        label="📥 下载当前数据 (CSV)",
        data=csv_data,
        file_name=f"手机市场数据_{search_term if search_term else '全部'}.csv",
        mime="text/csv"
    )

# 如果还有else情况（可选）
else:
    st.warning("页面选择错误，请重新选择。")
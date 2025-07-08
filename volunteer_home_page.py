import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json

# 页面配置
st.set_page_config(
    page_title="北师大支教数据图谱",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin: 0;
    }
    .stats-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .quick-nav {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .nav-button {
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        margin: 0.25rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .nav-button:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# 主标题区域
st.markdown("""
<div class="main-header">
    <h1>🏫 北师大支教数据图谱与故事可视化门户</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        汇聚支教力量，记录青春足迹，用数据见证教育公益的温暖力量
    </p>
</div>
""", unsafe_allow_html=True)

# 数据统计区域
st.markdown("## 📊 数据概览")

# 创建四列布局显示统计数据
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">156</div>
        <div class="stats-label">支教故事</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">23</div>
        <div class="stats-label">支教队伍</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">18</div>
        <div class="stats-label">省份覆盖</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">1,200+</div>
        <div class="stats-label">志愿者人数</div>
    </div>
    """, unsafe_allow_html=True)

# 快速导航
st.markdown("## 🧭 快速导航")
st.markdown("""
<div class="quick-nav">
    <a href="#stories" class="nav-button">📖 支教故事</a>
    <a href="#analysis" class="nav-button">📈 传播分析</a>
    <a href="#recruitment" class="nav-button">🎯 支教招募</a>
    <a href="#teams" class="nav-button">👥 队伍资料</a>
</div>
""", unsafe_allow_html=True)

# 地图和词云区域
st.markdown("## 🗺️ 支教地图分布")

# 创建两列布局
map_col, wordcloud_col = st.columns([3, 2])

with map_col:
    st.markdown("### 全国支教地点分布")
    
    # 示例数据 - 实际使用时替换为真实数据
    # TODO: 替换为真实的支教地点数据
    sample_locations = [
        {"province": "云南", "city": "昆明", "lat": 25.0389, "lon": 102.7183, "teams": 3, "stories": 12},
        {"province": "贵州", "city": "贵阳", "lat": 26.6470, "lon": 106.6302, "teams": 2, "stories": 8},
        {"province": "四川", "city": "成都", "lat": 30.6667, "lon": 104.0667, "teams": 4, "stories": 15},
        {"province": "西藏", "city": "拉萨", "lat": 29.6625, "lon": 91.1146, "teams": 1, "stories": 5},
        {"province": "青海", "city": "西宁", "lat": 36.6167, "lon": 101.7667, "teams": 2, "stories": 7},
        {"province": "甘肃", "city": "兰州", "lat": 36.0611, "lon": 103.8343, "teams": 3, "stories": 10},
        {"province": "内蒙古", "city": "呼和浩特", "lat": 40.8151, "lon": 111.6621, "teams": 2, "stories": 6},
        {"province": "新疆", "city": "乌鲁木齐", "lat": 43.8256, "lon": 87.6168, "teams": 1, "stories": 4},
    ]
    
    # 创建地图
    fig_map = go.Figure()
    
    # 添加散点图
    fig_map.add_trace(go.Scattermapbox(
        lat=[loc['lat'] for loc in sample_locations],
        lon=[loc['lon'] for loc in sample_locations],
        mode='markers',
        marker=dict(
            size=[loc['teams'] * 5 + 10 for loc in sample_locations],
            color=[loc['stories'] for loc in sample_locations],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="故事数量")
        ),
        text=[f"{loc['province']} {loc['city']}<br>队伍: {loc['teams']}<br>故事: {loc['stories']}" 
              for loc in sample_locations],
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # 更新地图布局
    fig_map.update_layout(
        mapbox=dict(
            accesstoken='pk.test',  # 实际使用时需要真实的Mapbox token
            style='open-street-map',
            center=dict(lat=35, lon=105),
            zoom=4
        ),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

with wordcloud_col:
    st.markdown("### 支教关键词云")
    
    # 示例关键词数据 - 实际使用时替换为真实数据
    # TODO: 替换为真实的关键词数据
    sample_keywords = {
        "孩子": 50, "山区": 45, "陪伴": 40, "教育": 38, "温暖": 35,
        "成长": 32, "青春": 30, "梦想": 28, "希望": 26, "爱心": 24,
        "志愿": 22, "奉献": 20, "责任": 18, "感动": 16, "收获": 14,
        "坚持": 12, "支持": 10, "帮助": 8, "快乐": 6, "未来": 4
    }
    
    # 生成词云
    wordcloud = WordCloud(
        width=400, 
        height=300,
        background_color='white',
        font_path='C:/Windows/Fonts/msyh.ttc',  # 微软雅黑 # 中文字体路径，实际使用时需要确保字体文件存在
        max_words=50,
        colormap='viridis'
    ).generate_from_frequencies(sample_keywords)
    
    # 显示词云
    fig_wc, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wc, use_container_width=True)
    
    # 显示热门关键词列表
    st.markdown("#### 🔥 热门关键词")
    top_keywords = sorted(sample_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (word, count) in enumerate(top_keywords, 1):
        st.write(f"{i}. **{word}** ({count})")

# 最新动态区域
st.markdown("## 📢 最新动态")

# 创建最新动态的示例数据
latest_stories = [
    {
        "title": "云南山区支教纪实：用心点亮希望之光",
        "team": "第21届研究生支教团",
        "date": "2024-11-15",
        "summary": "在云南省昆明市东川区，支教团成员们深入山区小学，为孩子们带去知识与温暖...",
        "emotion": "正面"
    },
    {
        "title": "贵州支教日记：陪伴是最长情的告白",
        "team": "心理学院支教队",
        "date": "2024-11-10",
        "summary": "贵州省毕节市的支教生活让我们深深感受到了教育的力量和孩子们的纯真...",
        "emotion": "正面"
    },
    {
        "title": "西藏支教感悟：在高原上播种未来",
        "team": "地理学院支教队",
        "date": "2024-11-05",
        "summary": "西藏的蓝天白云见证着我们的支教之路，每一个孩子的笑容都是最美的风景...",
        "emotion": "正面"
    }
]

# 显示最新故事卡片
for story in latest_stories:
    with st.expander(f"📖 {story['title']} ({story['date']})"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**队伍：** {story['team']}")
            st.write(f"**摘要：** {story['summary']}")
        with col2:
            emotion_color = "🟢" if story['emotion'] == "正面" else "🟡" if story['emotion'] == "中性" else "🔴"
            st.write(f"**情感：** {emotion_color} {story['emotion']}")

# 页脚信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏫 北京师范大学支教数据图谱项目</p>
    <p>📧 联系我们 | 🌐 项目主页 | 📱 关注公众号</p>
    <p style="font-size: 0.9rem;">数据更新时间: 2024年11月 | 数据来源: 北师大各支教队公众号</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏（可选）
with st.sidebar:
    st.markdown("## 🔧 页面设置")
    
    # 可以添加一些过滤选项
    st.markdown("### 数据过滤")
    year_filter = st.selectbox("选择年份", ["全部", "2024", "2023", "2022"])
    region_filter = st.selectbox("选择地区", ["全部", "西南地区", "西北地区", "华北地区", "其他"])
    
    st.markdown("### 📊 数据说明")
    st.info("""
    本系统数据来源于北师大各支教队公众号，
    通过AI技术自动提取和分析支教故事，
    为支教工作提供数据支撑。
    """)
    
    # 添加更新时间
    st.markdown("### ⏰ 更新信息")
    st.write("最后更新：2024-11-15")
    st.write("数据条数：156条")
    st.write("覆盖队伍：23个")

# 数据加载提示（用于实际部署时的数据替换指导）
st.markdown("---")
st.markdown("## 🛠️ 数据接口说明（开发用）")

with st.expander("💡 数据替换指导"):
    st.markdown("""
    ### 需要替换的数据部分：
    
    1. **统计数据**（第47-70行）：
       - 支教故事数量
       - 支教队伍数量  
       - 省份覆盖数量
       - 志愿者人数
    
    2. **地图数据**（第91-100行）：
       - `sample_locations` 列表
       - 需要包含：省份、城市、经纬度、队伍数、故事数
    
    3. **关键词数据**（第139-143行）：
       - `sample_keywords` 字典
       - 格式：{"关键词": 频次}
    
    4. **最新动态**（第169-185行）：
       - `latest_stories` 列表
       - 包含：标题、队伍、日期、摘要、情感标签
    
    ### 数据格式示例：
    ```python
    # 地图数据格式
    locations = [
        {"province": "云南", "city": "昆明", "lat": 25.0389, "lon": 102.7183, "teams": 3, "stories": 12}
    ]
    
    # 关键词数据格式
    keywords = {"孩子": 50, "教育": 45, "陪伴": 40}
    
    # 故事数据格式
    stories = [
        {"title": "标题", "team": "队伍", "date": "日期", "summary": "摘要", "emotion": "情感"}
    ]
    ```
    """)

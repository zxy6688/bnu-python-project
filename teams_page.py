import streamlit as st
import pandas as pd
import json
from datetime import datetime
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="支教队资料页 - 北师大支教图谱",
    page_icon="👥",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .team-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .team-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .team-subtitle {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 15px;
    }
    .honor-badge {
        background: #ffd700;
        color: #333;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin: 3px;
    }
    .stats-container {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .comment-section {
        background: #f1f3f4;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

def load_teams_data():
    """
    加载支教队伍数据
    📝 数据填充说明：
    - 替换这里的示例数据为你的真实数据
    - 数据格式：teams_data.json 或直接在这里修改字典
    """
    # 🔴 TODO: 替换为你的真实数据文件路径
    # teams_data = json.load(open('teams_data.json', 'r', encoding='utf-8'))
    
    # 示例数据 - 请替换为你的真实数据
    teams_data = [
        {
            "id": 1,
            "team_name": "北师大历史学院支教队",
            "college": "历史学院",
            "slogan": "用知识点亮山区孩子的梦想",
            "intro": "成立于2014年，专注于贵州山区教育支持，累计服务学生超过2000人次，致力于历史文化教育传播。",
            "location": "贵州黔东南",
            "coordinates": [26.5847, 107.9772],  # 经纬度
            "established_year": 2014,
            "total_volunteers": 156,
            "service_hours": 3240,
            "served_students": 2100,
            "honors": ["2023年度优秀支教团队", "贵州省教育扶贫先进集体"],
            "contact": {
                "wechat": "BNUHISTORY_TEACH",
                "email": "history_teach@bnu.edu.cn",
                "phone": "010-58808888"
            },
            "links": {
                "baidu_baike": "https://baike.baidu.com/item/北师大历史学院支教队",
                "official_website": "https://history.bnu.edu.cn/teach",
                "wechat_account": "北师大历史学院支教队"
            },
            "representative_stories": [
                "支教路上的歌声",
                "山里的图书馆建设记",
                "那些年我们一起走过的山路"
            ],
            "team_leader": {
                "name": "张明华",
                "position": "队长",
                "quote": "每一次支教都是成长，每一个孩子都是希望。"
            }
        },
        {
            "id": 2,
            "team_name": "北师大地理学院支教队",
            "college": "地理学院",
            "slogan": "用地理看世界，用爱心暖人心",
            "intro": "成立于2016年，主要在甘肃临夏地区开展支教活动，结合地理学科特色，开展科普教育。",
            "location": "甘肃临夏",
            "coordinates": [35.5993, 103.2107],
            "established_year": 2016,
            "total_volunteers": 89,
            "service_hours": 2180,
            "served_students": 1450,
            "honors": ["2022年度创新支教模式奖"],
            "contact": {
                "wechat": "BNUGEO_TEACH",
                "email": "geo_teach@bnu.edu.cn",
                "phone": "010-58809999"
            },
            "links": {
                "baidu_baike": "https://baike.baidu.com/item/北师大地理学院支教队",
                "official_website": "https://geo.bnu.edu.cn/teach",
                "wechat_account": "北师大地理学院支教队"
            },
            "representative_stories": [
                "高原上的地理课堂",
                "黄河边的科学实验"
            ],
            "team_leader": {
                "name": "李小红",
                "position": "队长",
                "quote": "让山区孩子也能看到更广阔的世界。"
            }
        },
        {
            "id": 3,
            "team_name": "北师大文学院支教队",
            "college": "文学院",
            "slogan": "以文化人，以德育人",
            "intro": "成立于2012年，是北师大最早的支教队伍之一，专注于语文教育和文化传承。",
            "location": "云南大理",
            "coordinates": [25.6056, 100.2675],
            "established_year": 2012,
            "total_volunteers": 234,
            "service_hours": 4560,
            "served_students": 3200,
            "honors": ["2021年度全国优秀支教团队", "云南省教育贡献奖", "北师大杰出社会服务奖"],
            "contact": {
                "wechat": "BNUCHINESE_TEACH",
                "email": "chinese_teach@bnu.edu.cn",
                "phone": "010-58807777"
            },
            "links": {
                "baidu_baike": "https://baike.baidu.com/item/北师大文学院支教队",
                "official_website": "https://chinese.bnu.edu.cn/teach",
                "wechat_account": "北师大文学院支教队"
            },
            "representative_stories": [
                "苍山下的诗歌朗诵会",
                "洱海边的作文课",
                "民族文化交流节"
            ],
            "team_leader": {
                "name": "王文静",
                "position": "队长",
                "quote": "用文字的力量，点亮孩子们的心灵。"
            }
        }
    ]
    
    return teams_data

def create_team_map(teams_data):
    """创建支教队地图分布"""
    # 以北京为中心的地图
    m = folium.Map(location=[39.9042, 116.4074], zoom_start=5)
    
    for team in teams_data:
        folium.Marker(
            location=team['coordinates'],
            popup=f"""
            <b>{team['team_name']}</b><br>
            📍 {team['location']}<br>
            👥 志愿者: {team['total_volunteers']}人<br>
            🎓 服务学生: {team['served_students']}人
            """,
            tooltip=team['team_name'],
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(m)
    
    return m

def display_team_card(team_data):
    """显示单个支教队卡片"""
    st.markdown(f"""
    <div class="team-card">
        <div class="team-title">{team_data['team_name']}</div>
        <div class="team-subtitle">{team_data['college']} | {team_data['slogan']}</div>
        <p>{team_data['intro']}</p>
        <div style="margin-top: 15px;">
            <strong>🏛️ 所属学院:</strong> {team_data['college']}<br>
            <strong>📍 支教地区:</strong> {team_data['location']}<br>
            <strong>🕐 成立时间:</strong> {team_data['established_year']}年<br>
            <strong>👤 队长:</strong> {team_data['team_leader']['name']} - "{team_data['team_leader']['quote']}"
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 荣誉展示
    if team_data['honors']:
        st.markdown("**🏆 荣誉榜:**")
        honor_html = ""
        for honor in team_data['honors']:
            honor_html += f'<span class="honor-badge">{honor}</span> '
        st.markdown(honor_html, unsafe_allow_html=True)
    
    # 统计数据
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("累计志愿者", f"{team_data['total_volunteers']}人")
    with col2:
        st.metric("服务时长", f"{team_data['service_hours']}小时")
    with col3:
        st.metric("服务学生", f"{team_data['served_students']}人")
    with col4:
        st.metric("获得荣誉", f"{len(team_data['honors'])}项")

def display_team_links(team_data):
    """显示队伍相关链接"""
    st.markdown("**🔗 相关链接:**")
    
    links_col1, links_col2, links_col3 = st.columns(3)
    
    with links_col1:
        if team_data['links']['baidu_baike']:
            st.markdown(f"[📚 百度百科]({team_data['links']['baidu_baike']})")
    
    with links_col2:
        if team_data['links']['official_website']:
            st.markdown(f"[🌐 官方网站]({team_data['links']['official_website']})")
    
    with links_col3:
        if team_data['links']['wechat_account']:
            st.markdown(f"📱 微信公众号: {team_data['links']['wechat_account']}")

def display_representative_stories(team_data):
    """显示代表性故事"""
    st.markdown("**📖 代表性故事:**")
    
    # 🔴 TODO: 这里需要与Stories页面联动，实现跳转功能
    for story in team_data['representative_stories']:
        st.markdown(f"• [{story}](#) _(点击查看详情)_")

def create_honor_ranking(teams_data):
    """创建荣誉排行榜"""
    honor_stats = []
    for team in teams_data:
        honor_stats.append({
            'team_name': team['team_name'],
            'honors_count': len(team['honors']),
            'total_volunteers': team['total_volunteers'],
            'service_hours': team['service_hours'],
            'served_students': team['served_students']
        })
    
    df = pd.DataFrame(honor_stats)
    
    # 创建排行榜图表
    fig = px.bar(
        df, 
        x='team_name', 
        y='honors_count',
        title='支教队荣誉排行榜',
        labels={'honors_count': '荣誉数量', 'team_name': '支教队'},
        color='honors_count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False)
    
    return fig, df

def display_comment_section(team_id, team_name):
    """显示留言板功能"""
    st.markdown(f"""
    <div class="comment-section">
        <h3>💬 {team_name} 留言板</h3>
        <p>欢迎为支教队留言支持！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 留言表单
    with st.form(f"comment_form_{team_id}"):
        col1, col2 = st.columns(2)
        with col1:
            commenter_name = st.text_input("姓名", placeholder="请输入您的姓名")
        with col2:
            commenter_role = st.selectbox("身份", ["在校学生", "毕业校友", "社会人士", "其他"])
        
        comment_text = st.text_area("留言内容", placeholder="请输入您的留言或建议...")
        submitted = st.form_submit_button("提交留言")
        
        if submitted and commenter_name and comment_text:
            # 🔴 TODO: 这里需要实现留言保存功能
            # 可以保存到CSV文件或数据库
            st.success(f"感谢 {commenter_name} 的留言！您的支持是我们前进的动力！")
            
            # 示例：保存到CSV文件
            # comment_data = {
            #     'team_id': team_id,
            #     'team_name': team_name,
            #     'commenter_name': commenter_name,
            #     'commenter_role': commenter_role,
            #     'comment_text': comment_text,
            #     'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # }
            # df = pd.DataFrame([comment_data])
            # df.to_csv('comments.csv', mode='a', header=False, index=False)

def main():
    """主页面函数"""
    st.title("👥 北师大支教队资料页")
    st.markdown("### 🎯 认识我们的支教队伍，了解他们的故事与成就")
    
    # 加载数据
    teams_data = load_teams_data()
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["📋 队伍总览", "🏆 荣誉排行", "🗺️ 地图分布"])
    
    with tab1:
        st.markdown("#### 📋 支教队伍详细资料")
        
        # 队伍选择器
        team_names = [team['team_name'] for team in teams_data]
        selected_team = st.selectbox("选择支教队", team_names)
        
        # 获取选中的队伍数据
        selected_team_data = next(team for team in teams_data if team['team_name'] == selected_team)
        
        # 显示队伍卡片
        display_team_card(selected_team_data)
        
        # 两列布局
        col1, col2 = st.columns(2)
        
        with col1:
            display_team_links(selected_team_data)
            st.markdown("---")
            display_representative_stories(selected_team_data)
        
        with col2:
            st.markdown("**📞 联系方式:**")
            st.markdown(f"📧 邮箱: {selected_team_data['contact']['email']}")
            st.markdown(f"📱 微信: {selected_team_data['contact']['wechat']}")
            st.markdown(f"☎️ 电话: {selected_team_data['contact']['phone']}")
        
        # 留言板
        st.markdown("---")
        display_comment_section(selected_team_data['id'], selected_team_data['team_name'])
    
    with tab2:
        st.markdown("#### 🏆 支教队荣誉与成就排行")
        
        # 创建荣誉排行榜
        honor_fig, honor_df = create_honor_ranking(teams_data)
        st.plotly_chart(honor_fig, use_container_width=True)
        
        # 综合排行表
        st.markdown("#### 📊 综合数据排行")
        
        # 排序选项
        sort_option = st.selectbox(
            "排序依据", 
            ["荣誉数量", "志愿者人数", "服务时长", "服务学生数"]
        )
        
        column_mapping = {
            "荣誉数量": "honors_count",
            "志愿者人数": "total_volunteers", 
            "服务时长": "service_hours",
            "服务学生数": "served_students"
        }
        
        sorted_df = honor_df.sort_values(column_mapping[sort_option], ascending=False)
        
        # 显示排行榜
        for idx, row in sorted_df.iterrows():
            rank = list(sorted_df.index).index(idx) + 1
            st.markdown(f"""
            **#{rank} {row['team_name']}**
            - 🏆 荣誉: {row['honors_count']}项 | 👥 志愿者: {row['total_volunteers']}人 
            - ⏰ 服务时长: {row['service_hours']}小时 | 🎓 服务学生: {row['served_students']}人
            """)
    
    with tab3:
        st.markdown("#### 🗺️ 支教队地图分布")
        
        # 创建地图
        team_map = create_team_map(teams_data)
        folium_static(team_map, width=1000, height=600)
        
        # 地区统计
        st.markdown("#### 📍 支教地区分布统计")
        locations = [team['location'] for team in teams_data]
        location_counts = pd.Series(locations).value_counts()
        
        fig_pie = px.pie(
            values=location_counts.values,
            names=location_counts.index,
            title="支教地区分布"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

if __name__ == "__main__":
    main()

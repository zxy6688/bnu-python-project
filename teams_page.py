import streamlit as st
import pandas as pd
import json
from datetime import datetime
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import re

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
    .link-button {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.9rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .link-button:hover {
        background: #218838;
        text-decoration: none;
        color: white;
    }
    .story-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_teams_data():
    """加载支教队伍数据"""
    try:
        # 尝试加载data2.csv
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        df = None

        for encoding in encodings:
            try:
                df = pd.read_csv("D:/mydevelops/PycharmProjects/PythonFinalWork/data2.csv", encoding=encoding)
                break
            except UnicodeDecodeError:
                continue

        if df is None:
            st.error("无法读取data2.csv文件，请检查文件编码")
            return None

        # 数据清洗
        df = df.fillna('')

        # 统一列名
        if '序号' not in df.columns and df.columns[0]:
            df['序号'] = df.iloc[:, 0]
        if '标题' not in df.columns and len(df.columns) > 1:
            df['标题'] = df.iloc[:, 1]
        if '原始链接' not in df.columns and len(df.columns) > 2:
            df['原始链接'] = df.iloc[:, 2]
        if '真实链接' not in df.columns and len(df.columns) > 3:
            df['真实链接'] = df.iloc[:, 3]

        return df
    except Exception as e:
        st.error(f"加载数据失败: {str(e)}")
        return None


def extract_team_info_from_data(df):
    """从数据中提取支教队伍信息"""
    teams_data = []

    # 预定义一些队伍信息
    default_teams = {
        "地理学院": {
            "college": "地理学院",
            "slogan": "用地理看世界，用爱心暖人心",
            "location": "甘肃临夏",
            "coordinates": [35.5993, 103.2107],
            "established_year": 2016
        },
        "历史学院": {
            "college": "历史学院",
            "slogan": "用知识点亮山区孩子的梦想",
            "location": "贵州黔东南",
            "coordinates": [26.5847, 107.9772],
            "established_year": 2014
        },
        "文学院": {
            "college": "文学院",
            "slogan": "以文化人，以德育人",
            "location": "云南大理",
            "coordinates": [25.6056, 100.2675],
            "established_year": 2012
        },
        "心理学院": {
            "college": "心理学院",
            "slogan": "用心理学点亮心灵",
            "location": "云南昆明",
            "coordinates": [25.0389, 102.7183],
            "established_year": 2015
        },
        "数学学院": {
            "college": "数学学院",
            "slogan": "用数学逻辑启发智慧",
            "location": "贵州毕节",
            "coordinates": [27.2844, 105.2988],
            "established_year": 2013
        }
    }

    # 从数据中提取队伍相关文章
    team_patterns = [
        r'(.*?学院.*?支教)',
        r'(.*?学部.*?支教)',
        r'(北师大.*?支教)',
        r'(研支团)',
        r'(支教队)',
        r'(支教团)'
    ]

    team_articles = {}

    for idx, row in df.iterrows():
        title = str(row.get('标题', ''))
        url = str(row.get('真实链接', row.get('原始链接', '')))

        # 提取队伍信息
        for pattern in team_patterns:
            matches = re.findall(pattern, title, re.IGNORECASE)
            if matches:
                team_name = matches[0]

                # 标准化队伍名称
                for default_team in default_teams.keys():
                    if default_team in team_name:
                        team_name = f"北师大{default_team}支教队"
                        break

                if team_name not in team_articles:
                    team_articles[team_name] = []

                team_articles[team_name].append({
                    'title': title,
                    'url': url,
                    'id': idx + 1
                })
                break

    # 构建队伍详细信息
    team_id = 1
    for team_name, articles in team_articles.items():
        # 查找匹配的默认队伍信息
        college_name = None
        team_info = None

        for college, info in default_teams.items():
            if college in team_name:
                college_name = college
                team_info = info
                break

        if not team_info:
            # 如果没有匹配的默认信息，创建基本信息
            team_info = {
                "college": "其他学院",
                "slogan": "用知识传递希望",
                "location": "待定地区",
                "coordinates": [35.0, 105.0],
                "established_year": 2020
            }

        # 统计文章相关信息
        total_articles = len(articles)
        wechat_articles = len([a for a in articles if 'mp.weixin.qq.com' in a['url']])

        teams_data.append({
            "id": team_id,
            "team_name": team_name,
            "college": team_info["college"],
            "slogan": team_info["slogan"],
            "intro": f"成立于{team_info['established_year']}年，专注于{team_info['location']}地区教育支持，累计发布相关文章{total_articles}篇，致力于教育扶贫和文化传播。",
            "location": team_info["location"],
            "coordinates": team_info["coordinates"],
            "established_year": team_info["established_year"],
            "total_volunteers": 50 + total_articles * 5,  # 根据文章数量估算
            "service_hours": 1000 + total_articles * 50,
            "served_students": 800 + total_articles * 30,
            "total_articles": total_articles,
            "wechat_articles": wechat_articles,
            "honors": [
                f"{datetime.now().year - 1}年度优秀支教团队" if total_articles > 5 else f"{datetime.now().year}年度支教贡献奖",
                f"{team_info['location']}教育扶贫先进集体" if total_articles > 3 else "支教工作积极分子"
            ],
            "contact": {
                "wechat": f"BNU{college_name.upper()}_TEACH" if college_name else "BNU_TEACH",
                "email": f"{college_name.lower()}_teach@bnu.edu.cn" if college_name else "teach@bnu.edu.cn",
                "phone": "010-58808888"
            },
            "articles": articles,
            "representative_stories": [article['title'][:30] + "..." for article in articles[:3]],
            "team_leader": {
                "name": f"队长{chr(65 + team_id)}",
                "position": "队长",
                "quote": "每一次支教都是成长，每一个孩子都是希望。"
            }
        })
        team_id += 1

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
            🎓 服务学生: {team['served_students']}人<br>
            📄 相关文章: {team['total_articles']}篇
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
        st.metric("相关文章", f"{team_data['total_articles']}篇")


def display_team_articles(team_data):
    """显示队伍相关文章"""
    st.markdown("**📄 相关文章:**")

    if not team_data['articles']:
        st.info("暂无相关文章")
        return

    # 分页显示文章
    items_per_page = 5
    total_pages = (len(team_data['articles']) + items_per_page - 1) // items_per_page

    if total_pages > 1:
        page_num = st.selectbox("选择页码", range(1, total_pages + 1), key=f"articles_page_{team_data['id']}")
    else:
        page_num = 1

    start_idx = (page_num - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(team_data['articles']))

    page_articles = team_data['articles'][start_idx:end_idx]

    for article in page_articles:
        st.markdown(f"""
        <div class="story-card">
            <h5 style="color: #333; margin-bottom: 0.5rem;">{article['title']}</h5>
            <p style="color: #666; font-size: 0.9rem;">
                <strong>文章ID:</strong> {article['id']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if article['url']:
            st.markdown(f"""
            <a href="{article['url']}" target="_blank" class="link-button">
                🔗 查看原文
            </a>
            """, unsafe_allow_html=True)

        st.markdown("---")


def create_honor_ranking(teams_data):
    """创建荣誉排行榜"""
    honor_stats = []
    for team in teams_data:
        honor_stats.append({
            'team_name': team['team_name'],
            'honors_count': len(team['honors']),
            'total_volunteers': team['total_volunteers'],
            'service_hours': team['service_hours'],
            'served_students': team['served_students'],
            'total_articles': team['total_articles']
        })

    df = pd.DataFrame(honor_stats)

    # 创建排行榜图表
    fig = px.bar(
        df,
        x='team_name',
        y='total_articles',
        title='支教队文章数量排行榜',
        labels={'total_articles': '文章数量', 'team_name': '支教队'},
        color='total_articles',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)

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
            st.success(f"感谢 {commenter_name} 的留言！您的支持是我们前进的动力！")

            # 这里可以保存留言到文件或数据库
            # comment_data = {
            #     'team_id': team_id,
            #     'team_name': team_name,
            #     'commenter_name': commenter_name,
            #     'commenter_role': commenter_role,
            #     'comment_text': comment_text,
            #     'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # }


def main():
    """主页面函数"""
    st.title("👥 北师大支教队资料页")
    st.markdown("### 🎯 认识我们的支教队伍，了解他们的故事与成就")

    # 加载数据
    df = load_teams_data()
    if df is None:
        return

    # 提取队伍数据
    teams_data = extract_team_info_from_data(df)

    if not teams_data:
        st.warning("未能从数据中提取到支教队伍信息")
        return

    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📋 队伍总览", "🏆 荣誉排行", "🗺️ 地图分布", "📄 文章浏览"])

    with tab1:
        st.markdown("#### 📋 支教队伍详细资料")

        # 队伍选择器
        team_names = [team['team_name'] for team in teams_data]
        selected_team = st.selectbox("选择支教队", team_names)

        # 获取选中的队伍数据
        selected_team_data = next(team for team in teams_data if team['team_name'] == selected_team)

        # 显示队伍卡片
        display_team_card(selected_team_data)

        # 显示联系方式
        st.markdown("**📞 联系方式:**")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"📱 微信: {selected_team_data['contact']['wechat']}")
        with col2:
            st.markdown(f"📧 邮箱: {selected_team_data['contact']['email']}")
        with col3:
            st.markdown(f"☎️ 电话: {selected_team_data['contact']['phone']}")

        # 显示相关文章
        display_team_articles(selected_team_data)

        # 显示留言板
        display_comment_section(selected_team_data['id'], selected_team_data['team_name'])

    with tab2:
        st.markdown("#### 🏆 支教队伍荣誉排行榜")

        fig, df_ranking = create_honor_ranking(teams_data)
        st.plotly_chart(fig, use_container_width=True)

        # 显示详细排行表
        st.markdown("##### 📊 详细排行数据")
        df_display = df_ranking.sort_values('total_articles', ascending=False)
        df_display.index = range(1, len(df_display) + 1)
        st.dataframe(
            df_display[['team_name', 'total_articles', 'total_volunteers', 'service_hours', 'served_students']],
            use_container_width=True)

    with tab3:
        st.markdown("#### 🗺️ 支教队伍地理分布")

        # 创建地图
        team_map = create_team_map(teams_data)
        folium_static(team_map)

        # 显示地区统计
        st.markdown("##### 📍 地区分布统计")
        location_stats = {}
        for team in teams_data:
            location = team['location']
            if location not in location_stats:
                location_stats[location] = []
            location_stats[location].append(team['team_name'])

        for location, teams in location_stats.items():
            st.markdown(f"**{location}:** {', '.join(teams)}")

    with tab4:
        st.markdown("#### 📄 支教相关文章浏览")

        # 收集所有文章
        all_articles = []
        for team in teams_data:
            for article in team['articles']:
                article['team_name'] = team['team_name']
                all_articles.append(article)

        if not all_articles:
            st.info("暂无相关文章")
            return

        # 搜索和筛选
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 搜索文章标题", placeholder="输入关键词...")
        with col2:
            team_filter = st.selectbox("筛选队伍", ["全部"] + [team['team_name'] for team in teams_data])

        # 应用筛选
        filtered_articles = all_articles.copy()

        if search_term:
            filtered_articles = [a for a in filtered_articles if search_term.lower() in a['title'].lower()]

        if team_filter != "全部":
            filtered_articles = [a for a in filtered_articles if a['team_name'] == team_filter]

        st.markdown(f"**找到 {len(filtered_articles)} 篇相关文章**")

        # 分页显示
        items_per_page = 10
        total_pages = (len(filtered_articles) + items_per_page - 1) // items_per_page

        if total_pages > 0:
            page_num = st.selectbox("选择页码", range(1, total_pages + 1), key="main_articles_page")

            start_idx = (page_num - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(filtered_articles))

            page_articles = filtered_articles[start_idx:end_idx]

            for article in page_articles:
                st.markdown(f"""
                <div class="story-card">
                    <h5 style="color: #333; margin-bottom: 0.5rem;">{article['title']}</h5>
                    <p style="color: #666; font-size: 0.9rem;">
                        <strong>所属队伍:</strong> {article['team_name']} | 
                        <strong>文章ID:</strong> {article['id']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if article['url']:
                    st.markdown(f"""
                    <a href="{article['url']}" target="_blank" class="link-button">
                        🔗 查看原文
                    </a>
                    """, unsafe_allow_html=True)

                st.markdown("---")
        else:
            st.info("没有找到符合条件的文章")


if __name__ == "__main__":
    main()
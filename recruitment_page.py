import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 页面配置
st.set_page_config(page_title="支教招募 - 北师大支教数据图谱", page_icon="🎯", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    .recruitment-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .recruitment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #ff6b6b;
    }
    .urgent-tag {
        background: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .normal-tag {
        background: #3498db;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .stats-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .apply-button {
        background: #ff6b6b;
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    .apply-button:hover {
        background: #e74c3c;
        transform: translateY(-2px);
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
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
</style>
""",
            unsafe_allow_html=True)


@st.cache_data
def load_recruitment_data():
    """加载招募数据"""
    try:
        # 尝试加载data1.csv
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        df = None

        for encoding in encodings:
            try:
                df = pd.read_csv(
                    "D:/mydevelops/PycharmProjects/PythonFinalWork/data1.csv",
                    encoding=encoding)
                break
            except UnicodeDecodeError:
                continue

        if df is None:
            st.error("无法读取data1.csv文件，请检查文件编码")
            return None

        # 数据清洗
        df = df.fillna('')

        # 如果没有指定的列，使用可用的列
        if 'title' in df.columns:
            df['标题'] = df['title']
        if 'content' in df.columns:
            df['内容'] = df['content']
        if 'url' in df.columns:
            df['链接'] = df['url']
        if 'date' in df.columns:
            df['日期'] = df['date']
        if 'account' in df.columns:
            df['账号'] = df['account']
        if 'contact_info' in df.columns:
            df['联系方式'] = df['contact_info']
        if 'project_duration' in df.columns:
            df['项目时长'] = df['project_duration']
        if 'project_location' in df.columns:
            df['项目地点'] = df['project_location']

        return df
    except Exception as e:
        st.error(f"加载数据失败: {str(e)}")
        return None


def extract_recruitment_info(df):
    """从数据中提取招募信息"""
    recruitment_data = []

    for idx, row in df.iterrows():
        title = str(row.get('标题', row.get('title', '')))
        content = str(row.get('内容', row.get('content', '')))
        url = str(row.get('链接', row.get('url', '')))
        date = str(row.get('日期', row.get('date', '')))
        account = str(row.get('账号', row.get('account', '')))

        # 判断是否为招募信息
        recruitment_keywords = ['招募', '支教', '志愿', '报名', '申请']
        if any(keyword in title for keyword in recruitment_keywords):

            # 提取地点信息
            location_patterns = [
                r'(西藏|新疆|内蒙古|宁夏|青海|甘肃|云南|贵州|四川|重庆|广西|海南)',
                r'(拉萨|乌鲁木齐|呼和浩特|银川|西宁|兰州|昆明|贵阳|成都|南宁|海口)',
                r'(喀什|和田|阿克苏|库尔勒|哈密|克拉玛依)', r'(林芝|日喀则|那曲|阿里|山南|昌都)',
                r'(临夏|定西|天水|白银|平凉|庆阳|陇南|金昌|张掖|酒泉|嘉峪关)',
                r'(大理|丽江|保山|昭通|玉溪|楚雄|红河|文山|普洱|版纳|德宏|怒江|迪庆)',
                r'(毕节|六盘水|安顺|铜仁|黔西南|黔东南|黔南|遵义)'
            ]

            location = "待定"
            for pattern in location_patterns:
                matches = re.findall(pattern, title + content)
                if matches:
                    location = matches[0]
                    break

            # 提取队伍信息
            team_patterns = [
                r'(.*?学院.*?支教)', r'(.*?学部.*?支教)', r'(北师大.*?支教)', r'(研支团)',
                r'(支教队)', r'(支教团)'
            ]

            team = account if account else "北师大支教队"
            for pattern in team_patterns:
                matches = re.findall(pattern, title)
                if matches:
                    team = matches[0]
                    break

            # 判断紧急程度
            urgency = "normal"
            urgent_keywords = ['紧急', '急需', '立即', '马上', '截止']
            if any(keyword in title for keyword in urgent_keywords):
                urgency = "urgent"

            # 提取联系方式
            contact = row.get('联系方式', row.get('contact_info', ''))
            if not contact:
                # 从内容中提取可能的联系方式
                phone_pattern = r'1[3-9]\d{9}'
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

                phone_match = re.search(phone_pattern, content)
                email_match = re.search(email_pattern, content)

                if phone_match:
                    contact = phone_match.group()
                elif email_match:
                    contact = email_match.group()
                else:
                    contact = "请查看详情"

            recruitment_data.append({
                "id":
                    idx + 1,
                "team":
                    team,
                "location":
                    location,
                "title":
                    title,
                "content":
                    content[:200] + "..." if len(content) > 200 else content,
                "url":
                    url,
                "date":
                    date,
                "account":
                    account,
                "contact":
                    contact,
                "urgency":
                    urgency,
                "duration":
                    row.get('项目时长', row.get('project_duration', '待定')),
                "people_needed":
                    2,  # 默认值
                "people_applied":
                    idx % 10 + 1  # 模拟报名人数
            })

    return recruitment_data


def main():
    """主页面函数"""
    # 页面标题
    st.markdown("""
    <div class="recruitment-header">
        <h1>🎯 支教招募中心</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            加入我们，用青春点亮希望，用知识传递温暖
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    # 加载数据
    df = load_recruitment_data()
    if df is None:
        return

    # 提取招募信息
    recruitment_data = extract_recruitment_info(df)

    if not recruitment_data:
        st.warning("未找到招募相关信息")
        return

    # 招募统计
    st.markdown("## 📊 招募统计")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("招募项目", len(recruitment_data))
    with col2:
        total_applied = sum(item["people_applied"]
                            for item in recruitment_data)
        st.metric("报名人数", total_applied)
    with col3:
        unique_teams = len(set(item["team"] for item in recruitment_data))
        st.metric("招募队伍", unique_teams)
    with col4:
        urgent_count = len(
            [item for item in recruitment_data if item["urgency"] == "urgent"])
        st.metric("紧急招募", urgent_count)

    # 报名热度图
    st.markdown("## 📈 报名热度分析")
    if recruitment_data:
        recruitment_df = pd.DataFrame(recruitment_data)

        fig_applications = px.bar(recruitment_df,
                                  x='team',
                                  y=['people_needed', 'people_applied'],
                                  title='各队伍招募vs报名情况',
                                  labels={
                                      'value': '人数',
                                      'variable': '类型'
                                  },
                                  color_discrete_map={
                                      'people_needed': '#ff6b6b',
                                      'people_applied': '#3498db'
                                  })
        fig_applications.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_applications, use_container_width=True)

    # 招募信息列表
    st.markdown("## 🎯 当前招募信息")

    # 筛选选项
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        locations = list(set([r["location"] for r in recruitment_data]))
        location_filter = st.selectbox("筛选地区", ["全部"] + locations)
    with filter_col2:
        teams = list(set([r["team"] for r in recruitment_data]))
        team_filter = st.selectbox("筛选队伍", ["全部"] + teams)
    with filter_col3:
        urgency_filter = st.selectbox("筛选紧急程度", ["全部", "urgent", "normal"])

    # 筛选数据
    filtered_data = recruitment_data.copy()
    if location_filter != "全部":
        filtered_data = [
            r for r in filtered_data if r["location"] == location_filter
        ]
    if team_filter != "全部":
        filtered_data = [r for r in filtered_data if r["team"] == team_filter]
    if urgency_filter != "全部":
        filtered_data = [
            r for r in filtered_data if r["urgency"] == urgency_filter
        ]

    # 显示招募卡片
    for recruitment in filtered_data:
        with st.container():
            st.markdown(f"""
            <div class="recruitment-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">{recruitment['team']}</h3>
                    <span class="{'urgent-tag' if recruitment['urgency'] == 'urgent' else 'normal-tag'}">
                        {'🔥 紧急招募' if recruitment['urgency'] == 'urgent' else '📝 正常招募'}
                    </span>
                </div>
            </div>
            """,
                        unsafe_allow_html=True)

            # 招募详情
            detail_col1, detail_col2, detail_col3 = st.columns(3)

            with detail_col1:
                st.write(f"**📍 支教地点：** {recruitment['location']}")
                st.write(f"**📚 项目：** {recruitment['title'][:30]}...")
                st.write(f"**⏰ 时长：** {recruitment['duration']}")

            with detail_col2:
                st.write(f"**👥 需求人数：** {recruitment['people_needed']} 人")
                st.write(f"**🙋 已报名：** {recruitment['people_applied']} 人")
                st.write(f"**📅 发布日期：** {recruitment['date']}")

            with detail_col3:
                st.write(f"**📞 联系方式：** {recruitment['contact']}")
                st.write(f"**📱 发布账号：** {recruitment['account']}")

            # 描述
            st.write(f"**📝 详细描述：** {recruitment['content']}")

            # 操作按钮
            action_col1, action_col2, action_col3 = st.columns([1, 1, 2])
            with action_col1:
                if st.button(f"立即报名", key=f"apply_{recruitment['id']}"):
                    st.session_state.selected_recruitment = recruitment
                    st.rerun()
            with action_col2:
                if recruitment['url']:
                    st.markdown(f"""
                    <a href="{recruitment['url']}" target="_blank" class="link-button">
                        🔗 查看详情
                    </a>
                    """,
                                unsafe_allow_html=True)

            st.markdown("---")

    # 报名表单
    if 'selected_recruitment' in st.session_state:
        selected = st.session_state.selected_recruitment

        st.markdown("## 📝 报名表单")
        st.markdown(f"""
        <div class="form-container">
            <h3>报名：{selected['team']} - {selected['location']}</h3>
            <p><strong>项目：</strong>{selected['title'][:50]}... | <strong>时长：</strong>{selected['duration']}</p>
        </div>
        """,
                    unsafe_allow_html=True)

        with st.form("recruitment_form"):
            st.markdown("### 个人信息")

            form_col1, form_col2 = st.columns(2)
            with form_col1:
                name = st.text_input("姓名 *", placeholder="请输入您的姓名")
                student_id = st.text_input("学号 *", placeholder="请输入学号")
                college = st.selectbox("学院 *", [
                    "请选择学院", "地理学院", "心理学院", "数学学院", "文学院", "英语学院", "历史学院",
                    "化学学院", "物理学院", "生物学院", "计算机学院", "教育学院", "音乐学院", "美术学院",
                    "体育学院", "其他"
                ])

            with form_col2:
                phone = st.text_input("联系电话 *", placeholder="请输入手机号")
                email = st.text_input("邮箱 *", placeholder="请输入邮箱地址")
                grade = st.selectbox(
                    "年级 *",
                    ["请选择年级", "大一", "大二", "大三", "大四", "研一", "研二", "研三", "博士"])

            st.markdown("### 支教意向")
            intention_col1, intention_col2 = st.columns(2)
            with intention_col1:
                preferred_subject = st.multiselect("教学科目偏好", [
                    "语文", "数学", "英语", "物理", "化学", "生物", "地理", "历史", "政治",
                    "心理健康", "其他"
                ])
            with intention_col2:
                preferred_duration = st.selectbox("可支教时长",
                                                  ["一学期", "一学年", "两学期", "其他"])

            # 经验和技能
            st.markdown("### 经验与技能")
            experience = st.text_area("教学经验/志愿服务经验",
                                      placeholder="请简要描述您的教学经验、志愿服务经验等相关背景",
                                      height=100)

            skills = st.text_area("特长技能",
                                  placeholder="请描述您的特长技能，如计算机、音乐、体育、手工等",
                                  height=80)

            # 支教动机
            st.markdown("### 支教动机")
            motivation = st.text_area("为什么选择支教？",
                                      placeholder="请谈谈您选择支教的原因和期望在支教中收获什么",
                                      height=120)

            # 其他信息
            st.markdown("### 其他信息")
            other_col1, other_col2 = st.columns(2)
            with other_col1:
                health_status = st.selectbox("健康状况",
                                             ["良好", "一般", "有慢性疾病但不影响工作", "其他"])
                has_certificate = st.checkbox("是否有教师资格证")
            with other_col2:
                emergency_contact = st.text_input("紧急联系人", placeholder="姓名+电话")
                agree_terms = st.checkbox("我已阅读并同意支教相关条款 *")

            # 提交按钮
            submitted = st.form_submit_button("🎯 提交报名",
                                              use_container_width=True)

            if submitted:
                # 验证必填项
                if not all([
                    name, student_id, college != "请选择学院", phone, email,
                    grade != "请选择年级", agree_terms
                ]):
                    st.error("请填写所有必填项（标*的项目）并同意相关条款！")
                else:
                    # 显示成功信息
                    st.success(f"""
                    🎉 报名成功！

                    感谢 {name} 报名参加 {selected['team']} 的支教活动！

                    我们会在3个工作日内通过您提供的联系方式与您联系，请保持手机畅通。

                    如有疑问，请联系：{selected['contact']}
                    """)

                    # 清除选中的招募信息
                    if 'selected_recruitment' in st.session_state:
                        del st.session_state.selected_recruitment


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# 页面配置
st.set_page_config(
    page_title="支教招募 - 北师大支教数据图谱",
    page_icon="🎯",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)

# ===========================================
# 数据配置区域 - 方便替换数据
# ===========================================

# TODO: 替换为真实招募数据
RECRUITMENT_DATA = [
    {
        "id": 1,
        "team": "地理学院支教队",
        "location": "甘肃临夏",
        "task": "初中地理",
        "deadline": "2025-07-10",
        "duration": "一学期",
        "people_needed": 3,
        "people_applied": 8,
        "requirements": "地理学相关专业，普通话标准",
        "contact": "张老师 13800138000",
        "urgency": "urgent",
        "description": "在甘肃临夏州积石山县支教，主要教授初中地理课程，帮助当地学生提高地理知识水平。"
    },
    {
        "id": 2,
        "team": "心理学院支教队",
        "location": "云南昆明",
        "task": "心理健康教育",
        "deadline": "2025-06-15",
        "duration": "一学年",
        "people_needed": 2,
        "people_applied": 5,
        "requirements": "心理学专业，有心理咨询经验优先",
        "contact": "李老师 13900139000",
        "urgency": "normal",
        "description": "负责农村中学心理健康教育工作，开展心理咨询和团体辅导活动。"
    },
    {
        "id": 3,
        "team": "数学学院支教队",
        "location": "贵州毕节",
        "task": "高中数学",
        "deadline": "2025-08-01",
        "duration": "两学期",
        "people_needed": 4,
        "people_applied": 12,
        "requirements": "数学专业，师范类优先",
        "contact": "王老师 13700137000",
        "urgency": "normal",
        "description": "在贵州毕节地区高中任教数学，提升当地高中数学教学质量。"
    },
    {
        "id": 4,
        "team": "文学院支教队",
        "location": "西藏拉萨",
        "task": "中学语文",
        "deadline": "2025-07-20",
        "duration": "一学年",
        "people_needed": 2,
        "people_applied": 6,
        "requirements": "中文专业，适应高原环境",
        "contact": "赵老师 13600136000",
        "urgency": "urgent",
        "description": "在西藏拉萨地区中学支教，教授语文课程，传播中华文化。"
    },
    {
        "id": 5,
        "team": "英语学院支教队",
        "location": "新疆喀什",
        "task": "小学英语",
        "deadline": "2025-06-30",
        "duration": "一学期",
        "people_needed": 3,
        "people_applied": 9,
        "requirements": "英语专业，英语口语流利",
        "contact": "孙老师 13500135000",
        "urgency": "normal",
        "description": "在新疆喀什地区小学教授英语课程，提高当地英语教学水平。"
    }
]

# TODO: 替换为真实统计数据
RECRUITMENT_STATS = {
    "total_positions": 14,
    "total_applications": 40,
    "teams_recruiting": 5,
    "deadline_approaching": 2
}

# ===========================================
# 页面内容开始
# ===========================================

# 页面标题
st.markdown("""
<div class="recruitment-header">
    <h1>🎯 支教招募中心</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        加入我们，用青春点亮希望，用知识传递温暖
    </p>
</div>
""", unsafe_allow_html=True)

# 招募统计
st.markdown("## 📊 招募统计")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("招募岗位", RECRUITMENT_STATS["total_positions"], delta="+2")
with col2:
    st.metric("报名人数", RECRUITMENT_STATS["total_applications"], delta="+5")
with col3:
    st.metric("招募队伍", RECRUITMENT_STATS["teams_recruiting"], delta="+1")
with col4:
    st.metric("截止临近", RECRUITMENT_STATS["deadline_approaching"], delta=None)

# 报名热度图
st.markdown("## 📈 报名热度分析")
recruitment_df = pd.DataFrame(RECRUITMENT_DATA)

fig_applications = px.bar(
    recruitment_df,
    x='team',
    y=['people_needed', 'people_applied'],
    title='各队伍招募vs报名情况',
    labels={'value': '人数', 'variable': '类型'},
    color_discrete_map={'people_needed': '#ff6b6b', 'people_applied': '#3498db'}
)
fig_applications.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_applications, use_container_width=True)

# 招募信息列表
st.markdown("## 🎯 当前招募信息")

# 筛选选项
filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    location_filter = st.selectbox("筛选地区", ["全部"] + list(set([r["location"] for r in RECRUITMENT_DATA])))
with filter_col2:
    task_filter = st.selectbox("筛选学科", ["全部"] + list(set([r["task"] for r in RECRUITMENT_DATA])))
with filter_col3:
    urgency_filter = st.selectbox("筛选紧急程度", ["全部", "urgent", "normal"])

# 筛选数据
filtered_data = RECRUITMENT_DATA.copy()
if location_filter != "全部":
    filtered_data = [r for r in filtered_data if r["location"] == location_filter]
if task_filter != "全部":
    filtered_data = [r for r in filtered_data if r["task"] == task_filter]
if urgency_filter != "全部":
    filtered_data = [r for r in filtered_data if r["urgency"] == urgency_filter]

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
        """, unsafe_allow_html=True)
        
        # 招募详情
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        
        with detail_col1:
            st.write(f"**📍 支教地点：** {recruitment['location']}")
            st.write(f"**📚 任务：** {recruitment['task']}")
            st.write(f"**⏰ 时长：** {recruitment['duration']}")
            
        with detail_col2:
            st.write(f"**👥 需求人数：** {recruitment['people_needed']} 人")
            st.write(f"**🙋 已报名：** {recruitment['people_applied']} 人")
            st.write(f"**📅 截止日期：** {recruitment['deadline']}")
            
        with detail_col3:
            st.write(f"**📞 联系方式：** {recruitment['contact']}")
            st.write(f"**✅ 要求：** {recruitment['requirements']}")
            
        # 描述
        st.write(f"**📝 详细描述：** {recruitment['description']}")
        
        # 操作按钮
        action_col1, action_col2 = st.columns([1, 4])
        with action_col1:
            if st.button(f"立即报名", key=f"apply_{recruitment['id']}"):
                st.session_state.selected_recruitment = recruitment
                st.rerun()
        with action_col2:
            if st.button(f"查看队伍详情", key=f"team_{recruitment['id']}"):
                st.info(f"即将跳转到 {recruitment['team']} 详情页面")
        
        st.markdown("---")

# 报名表单
if 'selected_recruitment' in st.session_state:
    selected = st.session_state.selected_recruitment
    
    st.markdown("## 📝 报名表单")
    st.markdown(f"""
    <div class="form-container">
        <h3>报名：{selected['team']} - {selected['location']}</h3>
        <p><strong>岗位：</strong>{selected['task']} | <strong>时长：</strong>{selected['duration']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("recruitment_form"):
        st.markdown("### 个人信息")
        
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            name = st.text_input("姓名 *", placeholder="请输入您的姓名")
            student_id = st.text_input("学号 *", placeholder="请输入学号")
            college = st.selectbox("学院 *", [
                "请选择学院",
                "地理学院", "心理学院", "数学学院", "文学院", "英语学院",
                "历史学院", "化学学院", "物理学院", "生物学院", "计算机学院",
                "教育学院", "音乐学院", "美术学院", "体育学院", "其他"
            ])
            
        with form_col2:
            phone = st.text_input("联系电话 *", placeholder="请输入手机号")
            email = st.text_input("邮箱 *", placeholder="请输入邮箱地址")
            grade = st.selectbox("年级 *", ["请选择年级", "大一", "大二", "大三", "大四", "研一", "研二", "研三", "博士"])
        
        st.markdown("### 支教意向")
        intention_col1, intention_col2 = st.columns(2)
        with intention_col1:
            preferred_subject = st.multiselect("教学科目偏好", 
                ["语文", "数学", "英语", "物理", "化学", "生物", "地理", "历史", "政治", "心理健康", "其他"])
        with intention_col2:
            preferred_duration = st.selectbox("可支教时长", ["一学期", "一学年", "两学期", "其他"])
        
        # 经验和技能
        st.markdown("### 经验与技能")
        experience = st.text_area("教学经验/志愿服务经验", 
            placeholder="请简要描述您的教学经验、志愿服务经验等相关背景", height=100)
        
        skills = st.text_area("特长技能", 
            placeholder="请描述您的特长技能，如计算机、音乐、体育、手工等", height=80)
        
        # 支教动机
        st.markdown("### 支教动机")
        motivation = st.text_area("为什么选择支教？", 
            placeholder="请谈谈您选择支教的原因和期望在支教中收获什么", height=120)
        
        # 其他信息
        st.markdown("### 其他信息")
        other_col1, other_col2 = st.columns(2)
        with other_col1:
            health_status = st.selectbox("健康状况", ["良好", "一般", "有慢性疾病但不影响工作", "其他"])
            has_certificate = st.checkbox("是否有教师资格证")
        with other_col2:
            emergency_contact = st.text_input("紧急联系人", placeholder="姓名+电话")
            agree_terms = st.checkbox("我已阅读并同意支教相关条款 *")
        
        # 提交按钮
        submitted = st.form_submit_button("🎯 提交报名", use_container_width=True)
        
        if submitted:
            # 验证必填项
            if not all([name, student_id, college != "请选择学院", phone, email, grade != "请选择年级", agree_terms]):
                st.error("请填写所有必填项（标*的项目）并同意相关条款！")
            else:
                # 保存报名信息
                application_data = {
                    "recruitment_id": selected['id'],
                    "team": selected['team'],
                    "name": name,
                    "student_id": student_id,
                    "college": college,
                    "phone": phone,
                    "email": email,
                    "grade": grade,
                    "preferred_subject": preferred_subject,
                    "preferred_duration": preferred_duration,
                    "experience": experience,
                    "skills": skills,
                    "motivation": motivation,
                    "health_status": health_status,
                    "has_certificate": has_certificate,
                    "emergency_contact": emergency_contact,
                    "apply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # TODO: 这里可以保存到数据库或CSV文件
                st.success("🎉 报名成功！我们会在3个工作日内与您联系。")
                st.balloons()
                
                # 显示报名信息确认
                with st.expander("查看报名信息"):
                    st.json(application_data)
                
                # 清除选择状态
                if st.button("继续浏览其他招募信息"):
                    del st.session_state.selected_recruitment
                    st.rerun()

# 支教指南
st.markdown("## 📚 支教指南")
guide_col1, guide_col2 = st.columns(2)

with guide_col1:
    st.markdown("### 📋 报名流程")
    st.markdown("""
    1. 📝 在线填写报名表
    2. 📞 等待电话/邮件联系
    3. 💬 参加面试/笔试
    4. 📋 提交相关材料
    5. 🎓 参加培训
    6. ✈️ 出发支教
    """)

with guide_col2:
    st.markdown("### 🎒 支教准备")
    st.markdown("""
    - 📖 教学用品和教材
    - 🩺 常用药品和医疗用品
    - 👕 适合当地气候的衣物
    - 📱 通讯设备和充电器
    - 🧴 日常生活用品
    - 💝 给孩子们的小礼物
    """)

# 常见问题
st.markdown("## ❓ 常见问题")
faq_data = [
    {
        "question": "支教期间的生活条件如何？",
        "answer": "学校会提供基本的住宿条件，通常是宿舍或教师公寓。生活设施相对简单，但能满足基本需求。建议提前了解当地情况，做好心理准备。"
    },
    {
        "question": "支教期间有工资吗？",
        "answer": "根据不同项目，可能提供基本的生活补贴。主要目的是志愿服务，不以获得报酬为主要目标。"
    },
    {
        "question": "支教期间的安全如何保障？",
        "answer": "学校会与当地教育部门合作，确保志愿者的安全。同时会购买保险，并建立紧急联系机制。"
    },
    {
        "question": "支教结束后有什么证明吗？",
        "answer": "支教结束后，会颁发志愿服务证书，这对个人简历和未来发展都有积极意义。"
    }
]

for faq in faq_data:
    with st.expander(f"❓ {faq['question']}"):
        st.write(faq['answer'])

# 联系我们
st.markdown("## 📞 联系我们")
contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.markdown("""
    **📧 邮箱联系**
    - 总负责人：volunteer@bnu.edu.cn
    - 报名咨询：apply@bnu.edu.cn
    """)

with contact_col2:
    st.markdown("""
    **📱 电话咨询**
    - 工作时间：9:00-17:00
    - 咨询热线：010-58800000
    """)

with contact_col3:
    st.markdown("""
    **🌐 其他方式**
    - 微信群：扫码加入
    - QQ群：123456789
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 加入我们，用青春点亮希望！</p>
    <p style="font-size: 0.9rem;">北京师范大学支教招募中心 | 最后更新: 2024-11-15</p>
</div>
""", unsafe_allow_html=True)

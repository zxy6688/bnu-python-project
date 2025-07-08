# bnu-python-project
python小学期大作业：基于 Streamlit 构建的北京师范大学支教数据可视化平台，整合支教故事、关键词分析、地图图谱、AI摘要与智能交互，方便校内外师生，为教育公益赋能。
# 北师大支教数据图谱与故事可视化平台  
> Teaching Story Visualization Portal for BNU Rural Education Support  
> 📘 Python 课程设计 × Streamlit × 数据分析 × 教育公益 × AI 应用

---

## 🧩 项目简介 | Project Overview

本项目是一个围绕“北京师范大学支教项目”的综合性数据可视化系统。我们通过公众号内容的结构化抽取，构建了支教故事数据库，借助 Python、Streamlit 与多种数据分析工具，开发出具有图形交互、AI摘要、地图标注与动态词云等功能的数字化门户网站。

> ✅ 本项目为《Python程序设计》课程的期末综合实践作业，结合真实教育数据，体现了对支教招募效率与公益传播力的关注。

本平台集成：
- 数据收集（微信公众号支教文章解析）
- 智能处理（关键词提取、情绪分类、AI摘要生成）
- 可视化展示（地图、词云、图表、图谱）
- 交互式门户设计（Streamlit 实现）

---

## 🖼️ 项目页面结构 | Main Portal Pages

### 1. 🏠 门户首页（Home）

- 北师大支教项目简介展示
- 使用 Folium 地图标注所有支教地点（可悬停查看队伍+年份）
- 支教故事关键词词云展示（动态生成）
- 数字卡片展示“累计故事数”“参与队伍”“总志愿者”等核心数据
- 快捷入口：点击地图可跳转至具体队伍故事页

---

### 2. 📚 支教故事页（Stories）

- 筛选器支持：按年份、省份、地点、情绪标签过滤故事
- 每个故事卡片展示：标题、AI摘要、情绪分类、发布时间、全文链接
- Plotly 折线图：展示支教故事的时间趋势（按月统计）
- AI 提示说明：强调摘要由大语言模型自动生成

---

### 3. 📈 传播分析页（Analysis）

- 热度趋势图：每月故事数量与点赞趋势（模拟数据）
- 年度关键词词云：支持切换年份查看高频关键词变化
- 情绪趋势：时间-情绪分布变化图（正负面占比）
- 故事传播路径图谱：使用 NetworkX + Pyvis 构建动态网络结构（故事→媒体→读者）

---

### 4. 📬 支教招募页（Recruitment）

- 招募任务展示表格（队伍、地点、学科、时间、人数）
- 招募说明：截止时间、联系方式
- 报名表单（st.form）：用户填写基本信息后可模拟报名
- 报名人数统计图：动态更新人数变化
- 与队伍资料页跳转联动（点击报名自动跳转）

---

### 5. 👥 支教队资料页（Teams）

- 队伍卡片：队名、学院、口号、地图定位、简介
- 外部链接区：百科 / 微信公众号 / 微博跳转
- 队伍代表故事 + 人物简介，可跳转至故事页
- 支教荣誉榜：展示服务时间、获奖记录等
- 留言板模块：用户可留言评论（本地持久化）

---

### 6. 🌟 亮点功能（加分项）

- 🤖 支教画像自动生成：使用关键词聚类+情绪提取，自动生成队伍典型画像总结
- 💬 AI 问答系统（支持“哪个队服务时间最长？”等自然语言提问）
- 🗓️ 年度支教日历（streamlit_calendar 实现）：可视化活动安排
- 🎞️ 支教故事配图自动视频生成（moviepy）：支持二次传播与视频展示

---

## 💻 技术栈与依赖 | Tech Stack

| 类别 | 工具 / 库 |
|------|-----------|
| 可视化前端 | Streamlit |
| 地图组件 | folium、streamlit-folium |
| 图表绘制 | plotly、pyecharts、matplotlib |
| 文本处理 | wordcloud、jieba、re、datetime |
| 网络图谱 | networkx、pyvis |
| 数据处理 | pandas、json |
| 智能分析 | 自研规则 + AI 摘要系统 |
| 文件存储 | CSV + 本地缓存 |
| 视频生成 | moviepy（可选） |

---

## 🛠️ 环境配置与运行方式 | How to Run

### 1. ✅ 本地运行（开发者推荐）

```bash
# 克隆仓库
git clone https://github.com/zxy6688/bnu-python-project.git
cd bnu-python-project

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动 Streamlit
streamlit run app.py  # 或主入口文件 main.py
```

### 2. 🌍 在线部署至 Streamlit Cloud（分享给朋友）

1. 访问 [https://share.streamlit.io](https://share.streamlit.io)
2. 绑定你的 GitHub 账号，点击“New App”
3. 选择此仓库：`zxy6688/bnu-python-project`
4. 设置运行文件为 `app.py`
5. 点击部署，生成在线链接，即可分享给朋友或老师

---

## 📊 示例数据格式 | Example JSON Data

```json
{
  "title": "山里的图书馆",
  "date": "2023-08-12",
  "team": "历史学院支教队",
  "location": "贵州黔东南",
  "summary": "我们走进大山，为孩子们建起一座小小图书馆……",
  "emotion": "positive"
}
```

---

## 🎯 项目目标与设计思路 | Design & Goals

本项目旨在以**教育公益数字化**为目标，结合真实数据与智能分析，构建一站式信息门户，帮助：

- 教育部门与高校更好地管理与传播支教工作成果
- 志愿者与公众快速获取支教故事与报名信息
- 利用 AI 助力内容提炼与传播，扩大公益影响力

设计流程如下：

```
微信公众号数据爬取
      ↓
数据清洗与结构化（JSON / CSV）
      ↓
关键词提取 + 情绪分析 + AI摘要
      ↓
Streamlit 多页面可视化门户构建
      ↓
地图 + 图表 + 路径图谱 + 表单交互等功能集成
      ↓
本地测试 / 云端部署（Streamlit Cloud）
```

---

## 🧾 文件结构（简要）

```
bnu-python-project/
├── app.py                   # 主入口文件（Streamlit）
├── data/
│   ├── stories.json         # 支教故事结构化数据
│   ├── teams.json           # 支教队伍信息
│   └── keywords.csv         # 高频关键词统计
├── images/                  # 图片资源
├── utils/
│   └── analysis_tools.py    # 数据处理函数
├── requirements.txt         # 项目依赖列表
└── README.md                # 项目说明文档（本文件）
```

---

## 🙌 项目成员与致谢 | Acknowledgements

- 🧑‍💻 开发与设计：[@zxy6688](https://github.com/zxy6688)
- 🧑‍🏫 指导老师：北京师范大学人工智能学院教学团队
- 📖 数据来源：北师大各支教队公众号推文内容、百度网页等
- ❤️ 特别致谢：py小甜心团队成员

---

## ⚠️ 免责声明 | Disclaimer

本项目为课程作业，部分数据为模拟生成或脱敏处理，仅用于教学展示。若需实际应用或媒体传播，请联系作者授权。

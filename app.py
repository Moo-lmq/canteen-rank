import streamlit as st 
import pandas as pd 
import os 
import sqlite3
from datetime import datetime 
 
# ── 页面配置 ────────────────────────────────────────────── 
st.set_page_config( 
    page_title="🍱 食堂菜品排行榜", 
    page_icon="🍱", 
    layout="wide", 
    initial_sidebar_state="collapsed", 
) 
 
# ── 自定义 CSS ──────────────────────────────────────────── 
st.markdown(""" 
<style> 
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap'); 
 
html, body, [class*="css"] { 
    font-family: 'Noto Sans SC', sans-serif; 
} 
 
/* 背景 */ 
.stApp { 
    background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f1f8ff 100%); 
    min-height: 100vh; 
} 
 
/* 隐藏默认菜单 */ 
#MainMenu, footer, header { visibility: hidden; } 
 
/* 标题区 */ 
.hero { 
    text-align: center; 
    padding: 2.5rem 1rem 1.5rem; 
    background: linear-gradient(135deg, #1e88e5, #64b5f6); 
    border-radius: 20px; 
    margin-bottom: 2rem; 
    box-shadow: 0 8px 32px rgba(30,136,229,0.25); 
    position: relative;
    overflow: hidden;
} 
.hero h1 { 
    font-size: 2.8rem; 
    font-weight: 900; 
    color: white; 
    margin: 0; 
    text-shadow: 0 2px 8px rgba(0,0,0,0.2); 
    position: relative;
    z-index: 2;
} 
.hero p { 
    color: rgba(255,255,255,0.9); 
    font-size: 1.1rem; 
    margin: 0.5rem 0 0; 
    position: relative;
    z-index: 2;
} 

/* 背景 Logo 装饰 */
.hero-logo {
    position: absolute;
    right: -20px;
    top: -20px;
    opacity: 0.15;
    width: 150px;
    z-index: 1;
    transform: rotate(15deg);
}
 
/* 卡片 */ 
.card { 
    background: white; 
    border-radius: 16px; 
    padding: 1.5rem; 
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
    margin-bottom: 1rem; 
    border-left: 5px solid #1e88e5; 
} 
 
/* 排行榜条目 */ 
.rank-item { 
    background: white; 
    border-radius: 14px; 
    padding: 1rem 1.4rem; 
    margin-bottom: 0.8rem; 
    display: flex; 
    align-items: center; 
    gap: 1rem; 
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); 
    transition: transform 0.2s; 
} 
.rank-item:hover { transform: translateX(4px); } 
 
.rank-num { 
    font-size: 1.6rem; 
    font-weight: 900; 
    min-width: 2.5rem; 
    text-align: center; 
} 
.rank-1 { color: #FFD700; } 
.rank-2 { color: #C0C0C0; } 
.rank-3 { color: #CD7F32; } 
.rank-other { color: #ccc; } 
 
.rank-info { flex: 1; } 
.rank-name { font-size: 1.1rem; font-weight: 700; color: #333; } 
.rank-stall { font-size: 0.85rem; color: #888; margin-top: 2px; } 
 
.rank-score { 
    text-align: right; 
} 
.score-val { 
    font-size: 1.5rem; 
    font-weight: 900; 
    color: #1e88e5; 
} 
 
.score-count { 
    font-size: 0.8rem; 
    color: #aaa; 
} 
 
/* 星星 */ 
.stars { color: #FFD700; font-size: 1rem; } 
 
/* 进度条 */ 
.score-bar-bg { 
    background: #f0f0f0; 
    border-radius: 99px; 
    height: 8px; 
    margin-top: 6px; 
    overflow: hidden; 
} 
.score-bar-fill { 
    height: 100%; 
    border-radius: 99px; 
    background: linear-gradient(90deg, #1e88e5, #64b5f6); 
} 
 
/* 提交按钮 */ 
.stButton > button { 
    background: linear-gradient(135deg, #1e88e5, #42a5f5) !important; 
    color: white !important; 
    border: none !important; 
    border-radius: 12px !important; 
    font-weight: 700 !important; 
    font-size: 1rem !important; 
    padding: 0.6rem 2rem !important; 
    width: 100% !important; 
    box-shadow: 0 4px 15px rgba(30,136,229,0.4) !important; 
    transition: all 0.2s !important; 
} 
.stButton > button:hover { 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 20px rgba(30,136,229,0.5) !important; 
} 
 
/* 表单控件 */ 
.stTextInput > div > div > input, 
.stTextArea > div > div > textarea, 
.stSelectbox > div > div { 
    border-radius: 10px !important; 
    border: 2px solid #bbdefb !important; 
    font-family: 'Noto Sans SC', sans-serif !important; 
} 
.stTextInput > div > div > input:focus, 
.stTextArea > div > div > textarea:focus { 
    border-color: #1e88e5 !important; 
    box-shadow: 0 0 0 3px rgba(30,136,229,0.15) !important; 
} 
 
/* 分隔线 */ 
hr { border-color: #bbdefb; } 
 
/* 成功/警告消息 */ 
.stSuccess { border-radius: 12px !important; } 
 
/* 标签 */ 
.section-label { 
    font-size: 1.2rem; 
    font-weight: 800; 
    color: #1e88e5; 
    margin-bottom: 1rem; 
    display: flex; 
    align-items: center; 
    gap: 0.5rem; 
} 
 
.tag { 
    background: #e3f2fd; 
    color: #1e88e5; 
    border-radius: 99px; 
    padding: 2px 10px; 
    font-size: 0.8rem; 
    font-weight: 700; 
} 
</style> 
""", unsafe_allow_html=True) 
 
# ── 数据库读写函数 ────────────────────────────────────────── 
DB_FILE = "canteen_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (dish_name TEXT, stall TEXT, score INTEGER, comment TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def load_data() -> pd.DataFrame:
    init_db()
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM reviews", conn)
    conn.close()
    return df

def add_record(dish_name: str, stall: str, score: int, comment: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?)",
              (dish_name.strip(), stall.strip(), score, comment.strip(), timestamp))
    conn.commit()
    conn.close()
 
 
def get_ranking(df: pd.DataFrame) -> pd.DataFrame: 
    if df.empty: 
        return pd.DataFrame() 
    rank = ( 
        df.groupby(["dish_name", "stall"]) 
        .agg(avg_score=("score", "mean"), count=("score", "count")) 
        .reset_index() 
        .sort_values("avg_score", ascending=False) 
        .reset_index(drop=True) 
    ) 
    rank.index += 1 
    return rank 
 
 
def stars(score: float) -> str: 
    full = int(round(score)) 
    return "★" * full + "☆" * (5 - full) 
 
# ── 英雄区 ──────────────────────────────────────────────── 
if os.path.exists("logo.png"):
    st.markdown(""" 
    <div class="hero"> 
        <img src="app/static/logo.png" class="hero-logo">
        <h1>🍱 食堂菜品排行榜</h1> 
        <p>吃过留迹，好菜共享 · 让每一顿饭都值得期待</p> 
    </div> 
    """, unsafe_allow_html=True) 
else:
    st.markdown(""" 
    <div class="hero"> 
        <h1>🍱 食堂菜品排行榜</h1> 
        <p>吃过留迹，好菜共享 · 让每一顿饭都值得期待</p> 
    </div> 
    """, unsafe_allow_html=True) 
 
# ── 布局：左栏提交 | 右栏排行 ──────────────────────────── 
col_left, col_right = st.columns([1, 1.4], gap="large") 

# 侧边栏 Logo (可选)
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
    st.sidebar.markdown("---")
 
# ════════════════════════════════════════════════════════ 
# 左栏：提交表单 
# ════════════════════════════════════════════════════════ 
with col_left: 
    st.markdown('<div class="section-label">📝 提交菜品评分</div>', unsafe_allow_html=True) 
 
    with st.form("submit_form", clear_on_submit=True): 
        dish_name = st.text_input("🍜 菜品名称", placeholder="例：红烧肉、番茄炒蛋...") 
        stall = st.text_input("🏪 档口名称", placeholder="例：一档、麻辣烫窗口...") 
        score = st.select_slider( 
            "⭐ 评分", 
            options=[1, 2, 3, 4, 5], 
            value=4, 
            format_func=lambda x: f"{x} 分 {'★' * x}{'☆' * (5 - x)}", 
        ) 
        comment = st.text_area( 
            "💬 评价（选填）", 
            placeholder="分享你的用餐感受...", 
            max_chars=200, 
            height=100, 
        ) 
 
        submitted = st.form_submit_button("🚀 提交评分") 
 
        if submitted: 
            if not dish_name.strip(): 
                st.error("请填写菜品名称！") 
            elif not stall.strip(): 
                st.error("请填写档口名称！") 
            else: 
                add_record(dish_name, stall, score, comment) 
                st.success(f"✅ 已提交「{dish_name.strip()}」的 {score} 星评价！") 
                st.balloons() 
 
    # 最新评论展示 
    st.markdown("---") 
    st.markdown('<div class="section-label">💬 最新评价</div>', unsafe_allow_html=True) 
    df_all = load_data() 
    if not df_all.empty: 
        recent = df_all[df_all["comment"].str.strip().astype(bool)].tail(5).iloc[::-1] 
        if recent.empty: 
            st.caption("暂无评价，快来第一个写评价吧！") 
        for _, row in recent.iterrows(): 
            with st.container(): 
                st.markdown(f""" 
                <div class="card" style="border-left-color:#bbdefb; padding:1rem;"> 
                    <div style="display:flex;justify-content:space-between;align-items:center;"> 
                        <span style="font-weight:700;color:#333;">{row['dish_name']}</span> 
                        <span class="tag">{row['stall']}</span> 
                    </div> 
                    <div class="stars" style="margin:4px 0;">{stars(row['score'])}</div> 
                    <div style="color:#555;font-size:0.9rem;">{row['comment']}</div> 
                    <div style="color:#bbb;font-size:0.78rem;margin-top:4px;">{row['timestamp']}</div> 
                </div> 
                """, unsafe_allow_html=True) 
    else: 
        st.caption("还没有任何评价，快来第一个提交吧！") 
 
# ════════════════════════════════════════════════════════ 
# 右栏：实时排行榜 
# ════════════════════════════════════════════════════════ 
with col_right: 
    st.markdown('<div class="section-label">🏆 实时排行榜</div>', unsafe_allow_html=True) 
 
    df_all = load_data() 
    rank_df = get_ranking(df_all) 
 
    if rank_df.empty: 
        st.info("📭 排行榜空空如也，快去提交第一条评分吧！") 
    else: 
        # 总统计 
        total_dishes = len(rank_df) 
        total_reviews = int(df_all.shape[0]) 
        overall_avg = df_all["score"].mean() if not df_all.empty else 0 
 
        m1, m2, m3 = st.columns(3) 
        m1.metric("🍽️ 收录菜品", f"{total_dishes} 道") 
        m2.metric("📊 总评价数", f"{total_reviews} 条") 
        m3.metric("⭐ 整体均分", f"{overall_avg:.2f}") 
 
        st.markdown("---") 
 
        # 档口筛选 
        stalls = ["全部档口"] + sorted(rank_df["stall"].unique().tolist()) 
        selected_stall = st.selectbox("筛选档口", stalls, label_visibility="collapsed") 
 
        filtered = rank_df if selected_stall == "全部档口" else rank_df[rank_df["stall"] == selected_stall] 
        filtered = filtered.reset_index(drop=True) 
 
        for i, row in filtered.iterrows(): 
            pos = i + 1 
            if pos == 1: 
                medal = "🥇" 
                cls = "rank-1" 
            elif pos == 2: 
                medal = "🥈" 
                cls = "rank-2" 
            elif pos == 3: 
                medal = "🥉" 
                cls = "rank-3" 
            else: 
                medal = f"#{pos}" 
                cls = "rank-other" 
 
            bar_width = int(row["avg_score"] / 5 * 100) 
 
            st.markdown(f""" 
            <div class="rank-item"> 
                <div class="rank-num {cls}">{medal}</div> 
                <div class="rank-info"> 
                    <div class="rank-name">{row['dish_name']}</div> 
                    <div class="rank-stall">📍 {row['stall']}</div> 
                    <div class="stars">{stars(row['avg_score'])}</div> 
                    <div class="score-bar-bg"> 
                        <div class="score-bar-fill" style="width:{bar_width}%;"></div> 
                    </div> 
                </div> 
                <div class="rank-score"> 
                    <div class="score-val">{row['avg_score']:.1f}</div> 
                    <div class="score-count">{int(row['count'])} 次评分</div> 
                </div> 
            </div> 
            """, unsafe_allow_html=True) 
 
        # 原始数据展开 
        with st.expander("📋 查看全部原始数据"): 
            st.dataframe( 
                df_all[["dish_name", "stall", "score", "comment", "timestamp"]] 
                .rename(columns={ 
                    "dish_name": "菜品", 
                    "stall": "档口", 
                    "score": "评分", 
                    "comment": "评价", 
                    "timestamp": "时间", 
                }) 
                .sort_values("时间", ascending=False), 
                use_container_width=True, 
                hide_index=True, 
            ) 
 
# ── 底部 ────────────────────────────────────────────────── 
st.markdown("---") 
if os.path.exists("logo.png"):
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f2:
        st.image("logo.png", width=50)
st.markdown( 
    "<div style='text-align:center;color:#ccc;font-size:0.8rem;'>🍱 食堂菜品排行榜 · 数据存储于本地 canteen_data.csv</div>", 
    unsafe_allow_html=True, 
)

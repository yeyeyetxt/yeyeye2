import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------- 全局配色与界面优化 --------------------------
st.set_page_config(
    page_title="阿伦尼乌斯公式交互工具",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS配色（核心优化部分）
st.markdown("""
<style>
    /* 全局背景 */
    .stApp {
        background-color: #F8FAFC;
    }
    /* 主标题样式 */
    h1 {
        color: #165DFF;
        font-weight: 700;
    }
    /* 卡片容器 */
    .stCard {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    }
    /* 滑块样式 */
    .stSlider > div > div > div {
        background-color: #36D399 !important;
    }
    /* 按钮样式 */
    .stButton > button {
        background-color: #165DFF;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0D47A1;
    }
    /* 文本样式 */
    .stMarkdown {
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------- 标题与公式说明 --------------------------
with st.container():
    st.title("🧪 阿伦尼乌斯公式交互工具")
    st.markdown("""
    **公式：** $k = A \cdot e^{-\\frac{E_a}{RT}}$  
    - $k$：反应速率常数  
    - $A$：指前因子（碰撞频率因子）  
    - $E_a$：活化能（J/mol）  
    - $R$：气体常数，取 $8.314\ J/(mol \cdot K)$  
    - $T$：热力学温度（K）
    """)

# -------------------------- 交互参数区 --------------------------
with st.container():
    st.subheader("1. 调整反应参数")
    col1, col2 = st.columns(2)

    with col1:
        A = st.number_input("指前因子 A (s⁻¹)", value=1.00e+10, format="%e")
        Ea = st.slider("活化能 Ea (kJ/mol)", min_value=10, max_value=200, value=50, step=5)

    with col2:
        T = st.slider("温度 T (K)", min_value=273, max_value=1000, value=298, step=10)
        compare = st.checkbox("对比不同活化能的反应速率")

# -------------------------- 核心计算 --------------------------
R = 8.314
Ea_J = Ea * 1000
k = A * np.exp(-Ea_J / (R * T))

st.markdown("---")
st.subheader("2. 计算结果")
st.metric(label="反应速率常数 k (s⁻¹)", value=f"{k:.4e}")

# -------------------------- 绘图区（配色同步优化） --------------------------
st.subheader("3. 阿伦尼乌斯图")
fig, ax = plt.subplots(figsize=(10, 6))

if compare:
    Ea_list = [30, 50, 80, 100]
    colors = ["#165DFF", "#36D399", "#FF9F43", "#FF6B6B"]
    T_range = np.linspace(273, 1000, 100)
    for i, ea in enumerate(Ea_list):
        ea_j = ea * 1000
        k_range = A * np.exp(-ea_j / (R * T_range))
        ax.plot(1/T_range, np.log(k_range), label=f"Ea={ea} kJ/mol", color=colors[i], linewidth=2)
    ax.legend()
else:
    T_range = np.linspace(273, 1000, 100)
    k_range = A * np.exp(-Ea_J / (R * T_range))
    ax.plot(1/T_range, np.log(k_range), color="#165DFF", linewidth=3)
    ax.scatter(1/T, np.log(k), color="#36D399", s=60, zorder=5, label=f"当前点 (T={T}K)")
    ax.legend()

ax.set_xlabel("1/T (K⁻¹)", color="#1E293B")
ax.set_ylabel("ln(k)", color="#1E293B")
ax.set_title("阿伦尼乌斯图", color="#1E293B")
ax.grid(alpha=0.3)
fig.patch.set_facecolor("#F8FAFC")
ax.set_facecolor("#FFFFFF")

st.pyplot(fig)

# -------------------------- 结果分析 --------------------------
st.subheader("4. 结果分析")
st.info("""
💡 结论：
- 活化能越高（曲线越陡），温度对反应速率的影响越大。
- 温度升高（1/T 减小），所有反应的速率常数都会增大。
- 阿伦尼乌斯图的斜率为 $-E_a/R$，可通过直线斜率计算活化能。
""")

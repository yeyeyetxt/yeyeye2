import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# 物理常数
R = 8.314

# ------------------- 页面配置 -------------------
st.set_page_config(page_title="阿伦尼乌斯公式交互工具", layout="wide")
st.title("🌸 阿伦尼乌斯公式交互工具")

# ------------------- 公式与说明 -------------------
st.latex(r"k = A \cdot e^{-\frac{E_a}{RT}}")
st.latex(r"\ln k = -\frac{E_a}{R} \cdot \frac{1}{T} + \ln A")
st.markdown("**斜率 = $-\dfrac{E_a}{R}$**")

with st.expander("公式参数说明"):
    st.markdown("""
    - **k**: 反应速率常数
    - **A**: 指前因子（碰撞频率因子）
    - **Eₐ**: 活化能 (J/mol)
    - **R**: 气体常数，取 8.314 J/(mol·K)
    - **T**: 热力学温度 (K)
    """)

st.divider()

# ------------------- 1. 参数设置 -------------------
st.subheader("1. 调整反应参数")

# 两列布局
col1, col2 = st.columns(2)
with col1:
    A = st.number_input("指前因子 A (s⁻¹)", value=1e10, format="%e")
    Ea_kJ = st.slider("活化能 Eₐ (kJ/mol)", 10, 200, 90, 1)
with col2:
    T = st.slider("温度 T (K)", 200, 1000, 493, 1)
    compare_Ea = st.checkbox("对比不同活化能")

Ea = Ea_kJ * 1000  # 转成 J/mol

# ------------------- 2. 实时计算结果 -------------------
st.divider()
st.subheader("📊 计算结果")

k = A * math.exp(-Ea / (R * T))
lnk = math.log(k)
slope = -Ea / R  # 阿伦尼乌斯直线斜率

col_k, col_slope = st.columns(2)
with col_k:
    st.metric("速率常数 k", f"{k:.6e}")
with col_slope:
    st.metric("直线斜率", f"{slope:.2f}")

st.text("阿伦尼乌斯图")

# ------------------- 3. 动态分子碰撞模型（放在直线图上方） -------------------
st.divider()
st.subheader("🔬 微观反应模型：分子碰撞动态模拟")

np.random.seed(42)
n_particles = 60
x = np.random.uniform(0, 10, n_particles)
y = np.random.uniform(0, 6, n_particles)

# 速度随温度变化
speed = T / 280
vx = np.random.randn(n_particles) * speed
vy = np.random.randn(n_particles) * speed

# 活化能判断有效/无效碰撞
ke = 0.5 * (vx**2 + vy**2)
threshold = Ea_kJ / 4.5
is_reactive = ke > threshold

fig_anim, ax_anim = plt.subplots(figsize=(8, 4))
ax_anim.set_xlim(0, 10)
ax_anim.set_ylim(0, 6)
ax_anim.axis("off")
ax_anim.set_title(f"T = {T} K   |   有效碰撞分子：{sum(is_reactive)} 个", fontsize=12)

scatter_react = ax_anim.scatter(x[is_reactive], y[is_reactive], c="#ef4444", s=35, label="有效碰撞")
scatter_normal = ax_anim.scatter(x[~is_reactive], y[~is_reactive], c="#0ea5e9", s=35, label="无效碰撞")
ax_anim.legend(loc="upper right")

def update(frame):
    global x, y
    x += vx * 0.04
    y += vy * 0.04
    # 边界反弹
    x = np.clip(x, 0, 10, out=x)
    y = np.clip(y, 0, 6, out=y)
    vx = np.where((x == 0) | (x == 10), -vx, vx)
    vy = np.where((y == 0) | (y == 6), -vy, vy)
    # 更新位置
    scatter_react.set_offsets(np.c_[x[is_reactive], y[is_reactive]])
    scatter_normal.set_offsets(np.c_[x[~is_reactive], y[~is_reactive]])
    return scatter_react, scatter_normal

ani = FuncAnimation(fig_anim, update, frames=80, interval=50, blit=True)
st.pyplot(fig_anim)

st.caption("✅ 温度升高 → 分子动能增大 → 有效碰撞增多 → 反应速率加快")

# ------------------- 4. 阿伦尼乌斯直线图 -------------------
st.divider()
st.subheader("📉 阿伦尼乌斯图：lnk - 1/T 关系")

T_range = np.linspace(200, 1000, 80)
invT_range = 1 / T_range
lnk_range = np.log(A) - Ea / (R * T_range)

fig_line, ax_line = plt.subplots(figsize=(7, 3.5))
ax_line.plot(invT_range, lnk_range, color="#0ea5e9", linewidth=2.5)
ax_line.scatter(1/T, lnk, color="#ef4444", s=90, zorder=5)
ax_line.set_xlabel("1/T  (K⁻¹)")
ax_line.set_ylabel("ln k")
ax_line.grid(alpha=0.3)
st.pyplot(fig_line, use_container_width=True)

# ------------------- 5. 说明与结论 -------------------
st.divider()
with st.expander("💡 说明"):
    st.markdown("""
    - 阿伦尼乌斯直线斜率 $= -\dfrac{E_a}{R}$
    - 活化能 $E_a$ 越大，斜率绝对值越大
    - 由斜率可反算活化能：$E_a = -R \\times 斜率$
    """)

with st.expander("4. 结果分析"):
    st.markdown("""
    - 活化能越高（曲线越陡），温度对反应速率的影响越大。
    - 温度升高（1/T 减小），所有反应的速率常数都会增大。
    - 阿伦尼乌斯图的斜率为 $-E_a/R$，可通过直线斜率计算活化能。
    """)

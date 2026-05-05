import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

# 物理常数
R = 8.314

st.set_page_config(page_title="阿伦尼乌斯方程", layout="wide")
st.title("阿伦尼乌斯方程可视化 | Arrhenius Equation")
st.divider()

# 侧边栏参数
st.sidebar.header("参数设置")
Ea_kJ = st.sidebar.slider("活化能 Eₐ (kJ/mol)", 10, 200, 50, 1)
A_1e12 = st.sidebar.slider("指前因子 A (×10¹²)", 1.0, 50.0, 10.0, 0.5)
T = st.sidebar.slider("温度 T (K)", 200, 1000, 298, 1)

Ea = Ea_kJ * 1000
A = A_1e12 * 1e12

# 实时计算
k = A * math.exp(-Ea / (R * T))
lnk = math.log(k)

# 数据展示
col1, col2, col3, col4 = st.columns(4)
col1.metric("速率常数 k", f"{k:.2e}")
col2.metric("ln k", f"{lnk:.2f}")
col3.metric("活化能 Eₐ", f"{Ea_kJ} kJ/mol")
col4.metric("温度 T", f"{T} K")

st.divider()

# ========== 图1：lnk - 1/T 直线 ==========
st.subheader("📉 阿伦尼乌斯直线：lnk - 1/T")

T_range = np.linspace(200, 1000, 80)
invT_range = 1 / T_range
lnk_range = np.log(A * np.exp(-Ea / (R * T_range)))

fig1, ax1 = plt.subplots(figsize=(6, 3))
ax1.plot(invT_range, lnk_range, color="#38bdf8", linewidth=2)
ax1.scatter(1/T, lnk, color="#f87171", s=80, zorder=5)
ax1.set_xlabel("1/T (K⁻¹)")
ax1.set_ylabel("ln k")
ax1.grid(alpha=0.3)
st.pyplot(fig1, use_container_width=True)

st.divider()

# ========== ✅ 动态分子碰撞模型（会动！放在这里） ==========
st.subheader("⚛️ 微观反应模型：分子碰撞动态模拟")

np.random.seed(42)
n_particles = 60
x = np.random.uniform(0, 10, n_particles)
y = np.random.uniform(0, 6, n_particles)

# 速度随温度变化
speed_scale = T / 300
vx = np.random.randn(n_particles) * speed_scale
vy = np.random.randn(n_particles) * speed_scale

# 活化能判断
kinetic_energy = 0.5 * (vx**2 + vy**2)
threshold = Ea_kJ / 5
is_active = kinetic_energy > threshold

# 创建动画画布
fig2, ax2 = plt.subplots(figsize=(7, 3.5))
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 6)
ax2.axis("off")
ax2.set_title(f"T = {T} K  |  有效碰撞：{sum(is_active)} 个")

# 散点对象
scatter_active = ax2.scatter(x[is_active], y[is_active], c="#f87171", s=30)
scatter_inactive = ax2.scatter(x[~is_active], y[~is_active], c="#38bdf8", s=30)

# 动画更新函数
def update(frame):
    global x, y
    x += vx * 0.05
    y += vy * 0.05

    # 边界反弹
    x = np.where(x < 0, 10, np.where(x > 10, 0, x))
    y = np.where(y < 0, 6, np.where(y > 6, 0, y))

    # 更新点位置
    scatter_active.set_offsets(np.column_stack([x[is_active], y[is_active]]))
    scatter_inactive.set_offsets(np.column_stack([x[~is_active], y[~is_active]]))
    return scatter_active, scatter_inactive

# 播放动画
ani = animation.FuncAnimation(
    fig2, update, frames=100, interval=50, blit=True
)

# 在 Streamlit 中展示动画
st.pyplot(fig2)

st.caption("温度越高 → 分子运动越快 → 有效碰撞越多 → 反应速率越快")

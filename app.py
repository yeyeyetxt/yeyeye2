import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

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

# ========== ✅ 反应模型：分子碰撞动画 ==========
st.subheader("⚛️ 微观反应模型：分子碰撞与活化能")

np.random.seed(42)
n_particles = 60
x = np.random.uniform(0, 10, n_particles)
y = np.random.uniform(0, 6, n_particles)

# 速度随温度变化
speed_scale = T / 300
vx = np.random.randn(n_particles) * speed_scale
vy = np.random.randn(n_particles) * speed_scale

# 能量超过活化能 → 有效碰撞
kinetic_energy = 0.5 * (vx**2 + vy**2)
threshold = Ea_kJ / 5
is_active = kinetic_energy > threshold

fig2, ax2 = plt.subplots(figsize=(7, 3.5))
ax2.scatter(x[is_active], y[is_active], c="#f87171", s=30, label="有效碰撞（反应）")
ax2.scatter(x[~is_active], y[~is_active], c="#38bdf8", s=30, label="无效碰撞")

# 活化能垒
ax2.axhspan(2, 4, color="#38bdf8", alpha=0.1)
ax2.set_title(f"T = {T} K  |  有效碰撞：{sum(is_active)} 个")
ax2.legend(ncol=3, loc="upper right")
ax2.axis("off")
st.pyplot(fig2, use_container_width=True)

st.caption("温度越高 → 分子运动越快 → 有效碰撞越多 → 反应速率越快")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 页面配置
st.set_page_config(page_title="阿伦尼乌斯公式交互工具", layout="wide")

# 标题与说明
st.title("🧪 阿伦尼乌斯公式交互工具")
st.markdown(r"""
公式：
$k = A \cdot e^{-\frac{E_a}{RT}}$
- $k$：反应速率常数
- $A$：指前因子（碰撞频率因子）
- $E_a$：活化能（J/mol）
- $R$：气体常数，取 $8.314\ J/(mol·K)$
- $T$：热力学温度（K）
""")

# --------------------------
# 1. 交互参数设置区
# --------------------------
st.subheader("1. 调整反应参数")
col1, col2 = st.columns(2)

with col1:
    A = st.number_input("指前因子 A (s⁻¹)", value=1e10, format="%.2e")
    Ea = st.slider("活化能 Ea (kJ/mol)", min_value=10, max_value=200, value=50, step=5)

with col2:
    T = st.slider("温度 T (K)", min_value=273, max_value=1000, value=298, step=10)
    show_comparison = st.checkbox("对比不同活化能的反应速率")

# 单位换算：kJ/mol → J/mol
Ea_J = Ea * 1000
R = 8.314

# --------------------------
# 2. 核心计算：阿伦尼乌斯公式
# --------------------------
# 计算当前参数下的速率常数
k = A * np.exp(-Ea_J / (R * T))
lnk = np.log(k)

# 计算不同温度下的速率常数，用于绘图
T_range = np.linspace(273, 1000, 200)
k_range = A * np.exp(-Ea_J / (R * T_range))
lnk_range = np.log(k_range)
inv_T = 1 / T_range

# 对比不同活化能的曲线（如果勾选了）
if show_comparison:
    Ea_list = [30, 50, 80]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
else:
    Ea_list = [Ea]
    colors = ["#ff7f0e"]

# --------------------------
# 3. 结果展示
# --------------------------
st.subheader("2. 计算结果")
col3, col4 = st.columns(2)

with col3:
    st.metric(label="当前温度下的速率常数 k", value=f"{k:.3e} s⁻¹")
with col4:
    st.metric(label="ln(k)", value=f"{lnk:.2f}")

# --------------------------
# 4. 阿伦尼乌斯图可视化
# --------------------------
st.subheader("3. 阿伦尼乌斯图（lnk vs 1/T）")
fig, ax = plt.subplots(figsize=(8, 4))

for i, Ea_val in enumerate(Ea_list):
    Ea_J_val = Ea_val * 1000
    k_val = A * np.exp(-Ea_J_val / (R * T_range))
    lnk_val = np.log(k_val)
    ax.plot(inv_T, lnk_val, label=f"Ea={Ea_val} kJ/mol", color=colors[i], linewidth=2)

# 标记当前点
ax.scatter(1/T, lnk, color="red", s=50, zorder=5, label=f"当前点 (T={T}K)")

ax.set_xlabel("1/T (K⁻¹)")
ax.set_ylabel("ln(k)")
ax.set_title("阿伦尼乌斯图")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

# --------------------------
# 5. 补充说明与分析
# --------------------------
st.subheader("4. 结果分析")
st.info(f"""
💡 结论：
- 活化能越高（曲线越陡），温度对反应速率的影响越大。
- 温度升高（1/T 减小），所有反应的速率常数都会增大。
- 当 T={T} K 时，活化能 {Ea} kJ/mol 的反应，速率常数为 {k:.3e} s⁻¹。
""")

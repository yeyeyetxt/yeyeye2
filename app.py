import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# 物理常数
R = 8.314

# ------------------- 页面配置 -------------------
st.set_page_config(page_title="阿伦尼乌斯公式交互工具", layout="wide")

# 标题
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="display: inline-flex; align-items: center; gap: 10px;">
            <span style="color:#ec4899; font-size: 2.5rem;">🌸</span>
            阿伦尼乌斯公式交互工具
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 公式（原生渲染，不乱码）
st.latex(r"k = A \cdot e^{-\frac{E_a}{RT}}")
st.latex(r"\ln k = -\frac{E_a}{R} \cdot \frac{1}{T} + \ln A")
st.latex(r"斜率 = -\dfrac{E_a}{R}")

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

col1, col2 = st.columns(2)
with col1:
    A = st.number_input("指前因子 A (s⁻¹)", value=1e10, format="%e")
    Ea_kJ = st.slider("活化能 Eₐ (kJ/mol)", 10, 200, 90, 1)
with col2:
    T = st.slider("温度 T (K)", 200, 1000, 493, 1)
    compare_Ea = st.checkbox("对比不同活化能", value=False)

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

# ------------------- 3. 微观反应模型：JS 动画 -------------------
st.divider()
st.subheader("🔬 微观反应模型：分子碰撞动态模拟")

speed_factor = T / 300
effective_ratio = min(100, max(0, 100 - (Ea_kJ / 2))) / 100

html_code = f"""
<div style="display:flex; justify-content:center;">
<canvas id="canvas" width="800" height="350" style="border-radius:8px;"></canvas>
</div>
<p style="text-align:center; font-size:14px;">T = {T} K ｜ 活化能 Eₐ = {Ea_kJ} kJ/mol ｜ 预计有效碰撞比例 ≈ {effective_ratio*100:.0f}%</p >

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;
const N = 60;
const speedFactor = {speed_factor:.2f};
const effectiveRatio = {effective_ratio:.2f};

let molecules = [];
for (let i = 0; i < N; i++) {{
    let speed = (Math.random() * 2 + 0.5) * speedFactor;
    let angle = Math.random() * Math.PI * 2;
    let vx = Math.cos(angle) * speed;
    let vy = Math.sin(angle) * speed;
    molecules.push({{
        x: Math.random() * W,
        y: Math.random() * H,
        vx: vx,
        vy: vy,
        isReactive: Math.random() < effectiveRatio
    }});
}}

function animate() {{
    ctx.clearRect(0, 0, W, H);
    molecules.forEach(m => {{
        m.x += m.vx;
        m.y += m.vy;
        if (m.x < 0 || m.x > W) m.vx *= -1;
        if (m.y < 0 || m.y > H) m.vy *= -1;
        m.x = Math.max(0, Math.min(W, m.x));
        m.y = Math.max(0, Math.min(H, m.y));
        ctx.beginPath();
        ctx.arc(m.x, m.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = m.isReactive ? '#ef4444' : '#0ea5e9';
        ctx.fill();
    }});
    requestAnimationFrame(animate);
}}
animate();
</script>
"""

st.components.v1.html(html_code, height=420)

st.caption("✅ 温度升高 → 分子动能增大 → 有效碰撞增多 → 反应速率加快")

# ------------------- 4. 阿伦尼乌斯直线图（带对比功能） -------------------
st.divider()
st.subheader("📉 阿伦尼乌斯图：lnk - 1/T 关系")

T_range = np.linspace(200, 1000, 80)
invT_range = 1 / T_range

fig_line, ax_line = plt.subplots(figsize=(7, 3.5))

# 主活化能曲线
lnk_range = np.log(A) - Ea / (R * T_range)
ax_line.plot(invT_range, lnk_range, color="#0ea5e9", linewidth=2.5, label=f"Eₐ = {Ea_kJ} kJ/mol")
ax_line.scatter(1/T, lnk, color="#ef4444", s=90, zorder=5)

# 对比不同活化能的曲线
if compare_Ea:
    # 定义几个不同的活化能
    compare_Ea_list = [30, 60, 120, 150]
    colors = ["#22c55e", "#f59e0b", "#8b5cf6", "#ec4899"]
    for idx, ea in enumerate(compare_Ea_list):
        ea_J = ea * 1000
        lnk_compare = np.log(A) - ea_J / (R * T_range)
        ax_line.plot(invT_range, lnk_compare, color=colors[idx], linestyle="--", linewidth=1.5, label=f"Eₐ = {ea} kJ/mol")

ax_line.set_xlabel("1/T  (K⁻¹)")
ax_line.set_ylabel("ln k")
ax_line.grid(alpha=0.3)
ax_line.legend()
st.pyplot(fig_line, use_container_width=True)

# ------------------- 5. 说明与结论 -------------------
st.divider()
with st.expander("💡 说明"):
    st.markdown("""
    - 阿伦尼乌斯直线斜率 $= -\dfrac{E_a}{R}$
    - 活化能 $E_a$ 越大，斜率绝对值越大，直线越陡
    - 由斜率可反算活化能：$E_a = -R \\times 斜率$
    """)

with st.expander("4. 结果分析"):
    st.markdown("""
    - 活化能越高（曲线越陡），温度对反应速率的影响越大。
    - 温度升高（1/T 减小），所有反应的速率常数都会增大。
    - 阿伦尼乌斯图的斜率为 $-E_a/R$，可通过直线斜率计算活化能。
    """)

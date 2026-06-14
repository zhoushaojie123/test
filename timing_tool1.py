import matplotlib.pyplot as plt
import numpy as np

# 中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ================== 1. 数据定义 ==================
# GLOBAL_DELAY的延时长度
LASER_FIRE_TIME=41007
GLOBAL_AD=3000
GLOBAL_LF=0
TRIG_PP=9900
PP_MISS=2000
MP_LOCK_PP=1310
RP_LOCK_MP=1310
PP2MP=2600
RP2MP=3810
LF_CD=4000
SCAM2PP=0
SCAM_LOCK_PP=5000
SCAM_CD=LF_CD+SCAM_LOCK_PP
PP=TRIG_PP+PP_MISS
RP_CD=RP_LOCK_MP+PP2MP-RP2MP
global_delay = [LASER_FIRE_TIME, GLOBAL_AD, GLOBAL_LF]
# 七个延伸段长度（七个变量）
extensions = [PP, 1.2, RP_CD, 0.5, 2.8, 1.7, 2.3]

# 总段数：1个公共 + 7个延伸
num_ext = len(extensions)

# ================== 2. 公共部分总长 ==================
base_total = sum(global_delay)

# ================== 3. 绘图 ==================
fig, ax = plt.subplots(figsize=(12, 6))
bar_height = 0.6

# ------ 3.1 绘制公共横条（最上方，y=0） ------
base_y = 0
left = 0.0
colors_base = ['#4C72B0', '#55A868', '#C44E52']

for i, seg in enumerate(global_delay):
    ax.barh(
        y=base_y,
        width=seg,
        height=bar_height,
        left=left,
        color=colors_base[i],
        edgecolor='white',
        linewidth=0.8,
        label=f'公共小段{i+1}'
    )
    left += seg

# ------ 3.2 绘制七个延伸横条（y=1 到 y=7） ------
ext_colors = plt.cm.Set2(np.linspace(0, 1, num_ext))
segment_names = [f"第{i+1}段" for i in range(num_ext)]

for i, ext in enumerate(extensions):
    y = i + 1               # 第1段在y=1，第7段在y=7
    ax.barh(
        y=y,
        width=ext,
        height=bar_height,
        left=base_total,    # 从公共右边界开始
        color=ext_colors[i],
        edgecolor='white',
        linewidth=0.8,
        label=f'{segment_names[i]}特有' if i == 0 else ""
    )
    # 总延时标注
    total = base_total + ext
    ax.text(total + 0.1, y, f'{total:.1f}s', va='center', fontsize=9)

# ------ 3.3 添加垂直虚线，连接公共部分右端与延伸部分起点 ------
ax.plot([base_total, base_total],
        [base_y + bar_height/2, num_ext + bar_height/2],
        color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

# ================== 4. 坐标轴设置 ==================
# y轴刻度：0为公共基础，1~7为七个延伸段
ax.set_yticks(range(num_ext + 1))
ax.set_yticklabels(['公共基础'] + segment_names)
ax.set_xlabel('延时长度（秒）')
ax.set_title('7段延时：共同三小段（最上） + 七段特有延伸')

ax.set_ylim(-0.5, num_ext + 0.5)   # 让图形紧凑

# ================== 5. 图例 ==================
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.02, 1), loc='upper left')

plt.tight_layout()
plt.show()
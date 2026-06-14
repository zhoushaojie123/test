import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体，避免图表标题、标签乱码（可根据系统调整）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 1. 定义数据：7段延时，每段由若干小段组成 ----------
# 每段是一个列表，列表中的数值代表该小段的延时长度（单位可自定义，例如秒）
delay_segments = [
    [2.1, 1.5, 0.8],          # 第1段：3个小段
    [3.0, 0.9, 1.2, 0.5],     # 第2段：4个小段
    [1.2, 2.2, 0.7],          # 第3段：3个小段
    [0.6, 0.9, 1.5, 1.0],     # 第4段：4个小段
    [2.0, 1.1, 1.3, 0.4, 0.6],# 第5段：5个小段
    [0.8, 2.5, 0.5],          # 第6段：3个小段
    [3.2, 0.7, 0.9]           # 第7段：3个小段
]

# 每段的名称，用于纵轴标签
segment_names = [f"第{i+1}段" for i in range(7)]

# 为了堆叠图，我们需要知道每个小段在横条中的起始位置（左边界）
# 可以使用 numpy 的 cumsum 计算累计长度
num_segments = len(delay_segments)               # 7
max_subs = max(len(seg) for seg in delay_segments)  # 最多的小段数量（用于统一颜色映射）

# 生成一组颜色，每个小段一种颜色（同一列的小段使用相同颜色）
colors = plt.cm.tab10(np.linspace(0, 1, max_subs))

# ---------- 2. 绘制水平堆叠条形图 ----------
fig, ax = plt.subplots(figsize=(12, 6))

# 记录每个主段的起始位置（初始为0）
left_positions = np.zeros(num_segments)

for i, seg in enumerate(delay_segments):
    cum_length = 0.0
    for j, sub_delay in enumerate(seg):
        # 绘制第 i 段中的第 j 个小段
        bar = ax.barh(
            y=i,                     # 纵坐标：第 i 行
            width=sub_delay,         # 小段的长度
            height=0.6,              # 横条的高度
            left=cum_length,         # 左边起点
            color=colors[j % max_subs],  # 颜色按列循环
            edgecolor='white',
            linewidth=0.5,
            label=f'小段类型 {j+1}' if i == 0 else ""   # 只创建一次图例项
        )
        cum_length += sub_delay       # 下一个子段从当前累计长度开始
    # 记录该段总延时，用于后面标注
    left_positions[i] = cum_length   # 这里其实用于其他目的，我们暂时不用

# 设置纵轴标签
ax.set_yticks(range(num_segments))
ax.set_yticklabels(segment_names)

# 设置横轴标签和标题
ax.set_xlabel('延时长度（单位：秒）')
ax.set_title('7段延时组成（横条中不同颜色代表不同小段）')

# 在图表的右侧添加总延时标注
for i, seg in enumerate(delay_segments):
    total = sum(seg)
    ax.text(total + 0.1, i, f'{total:.1f}s', va='center', fontsize=9, color='black')

# 添加图例（去重并放在图外，避免遮挡）
handles, labels = ax.get_legend_handles_labels()
# 只保留唯一的图例句柄
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

# 调整布局，使图例完整显示
plt.tight_layout()
plt.show()
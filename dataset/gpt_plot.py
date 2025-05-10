import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import numpy as np
import json
import matplotlib
from adjustText import adjust_text

# ======================= 辅助函数 ===========================
def interpolate_colors(color_a, color_b, t):
    """
    颜色插值函数: 计算两个颜色之间的中间值。
    - color_a, color_b: RGB颜色元组
    - t: 插值因子 (0.0 - 1.0)
    """
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

def lightening_colors(color_a, number_of_colors):
    if len(color_a) == 4:  # RGBA
        alphas = np.linspace(0.0, 1.0, num=number_of_colors + 2).tolist()[1:-1]
        rgb = color_a[:3]
        return [rgb + (a,) for a in alphas][::-1]

    color_b = (1, 1, 1)
    colors = [interpolate_colors(color_a, color_b, t / number_of_colors) for t in range(number_of_colors + 2)]
    return colors[1:-1]

def filter_data(superclass_counts, subclass_counts, threshold_super=1000, threshold_sub=1500):
    """
    数据筛选:
    - 筛选superclass和subclass，合并数量较小的类为'Other'。
    """
    filtered_superclass = defaultdict(int)
    filtered_subclass = defaultdict(int)
    minor_superclasses = set()

    # 筛选superclass
    for superclass, count in superclass_counts.items():
        if superclass == "null":  # 跳过null值
            continue
        if count > threshold_super:
            filtered_superclass[superclass] += count
        else:
            filtered_superclass['Others'] += count
            minor_superclasses.add(superclass)

    # 筛选subclass
    for (superclass, subclass), count in subclass_counts.items():
        if superclass == "null" or subclass == "null":
            continue
        if superclass not in minor_superclasses:
            if count > threshold_sub:
                filtered_subclass[(superclass, subclass)] = count
            else:
                filtered_subclass[(superclass, 'Others')] += count
        else:
            filtered_subclass[('Others', 'Others')] += count

    return filtered_superclass, filtered_subclass

# ======================= 绘图函数 ===========================
def plot_pie_chart(superclass_counts, subclass_counts):
    """
    绘制分层饼图:
    - 内圈: superclass 数据
    - 外圈: subclass 数据，并包含连接线。
    """
    inner_width = 0.75  # 内圈宽度比例
    start_angle = 45    # 饼图起始角度

    # 筛选数据
    filtered_superclass, filtered_subclass = filter_data(superclass_counts, subclass_counts)

    # 内圈数据
    super_labels = list(filtered_superclass.keys())
    super_sizes = list(filtered_superclass.values())
    rotation_labels = [super_labels[i] for i in range(len(super_labels)) if super_sizes[i] <= 0.25*sum(super_sizes)]

    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制内圈
    wedges, texts= ax.pie(
        super_sizes, labels=super_labels, startangle=start_angle,
        radius=inner_width, wedgeprops=dict(width=inner_width),
        labeldistance=0.4, rotatelabels=True, textprops={'fontsize': 7}
    )

    for i, (wedge, text) in enumerate(zip(wedges, texts)):
        label = super_labels[i]

        # 获取扇形的中间角度
        theta1, theta2 = wedge.theta1, wedge.theta2  # 扇形起始和结束角度
        angle = (theta1 + theta2) / 2  # 计算扇形的中间角度

        # 只旋转特定标签
        if label in rotation_labels:
            # 调整文本角度：根据角度位置，确保文本直立（顶部朝上）
            rotation_angle = angle
            text.set_rotation(rotation_angle)  # 设置文本旋转角度
        else:
            text.set_rotation(0)  # 不旋转

    # 内圈颜色
    inner_colors = [w.get_facecolor() for w in wedges]

    # 外圈数据
    sub_labels, sub_sizes, sub_colors = [], [], []
    for idx, superclass in enumerate(super_labels):
        subclass_data = [(k[1], v) for k, v in filtered_subclass.items() if k[0] == superclass]
        subclass_data = sorted(subclass_data, key=lambda x: x[1], reverse=True)
        sub_labels.extend([label for label, _ in subclass_data])
        sub_sizes.extend([size for _, size in subclass_data])
        sub_colors.extend(lightening_colors(inner_colors[idx], len(subclass_data)))

    # 绘制外圈
    wedges2, texts = ax.pie(
        sub_sizes, labels=sub_labels, startangle=start_angle,
        radius=1, colors=sub_colors, wedgeprops=dict(width=1 - inner_width),
        labeldistance=1.1, textprops={'fontsize': 6}
    )

    # 添加连接线
    for i, wedge in enumerate(wedges2):
        # 计算角度和坐标
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x, y = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
        # 确定标签对齐方向
        horizontal_alignment = 'left' if x > 0 else 'right'
        connectionstyle = f"angle,angleA=0,angleB={angle}"

        # 绘制连接线和标签
        ax.annotate(
            sub_labels[i], xy=(x, y), xytext=(1.2 * x, 1.2 * y),
            horizontalalignment=horizontal_alignment, fontsize=6,
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, connectionstyle=connectionstyle)
        )
        texts[i].set_visible(False)  # 隐藏默认标签

    # 保存和显示图表
    plt.title("Metabolite Categories Distribution", fontsize=10)
    plt.tight_layout()
    plt.savefig("metabolite_distribution.png", dpi=400)
    # plt.show()

# ======================= 主程序 ===========================
if __name__ == "__main__":
    # 读取JSON数据文件
    with open('metabolites_class.json', encoding="utf-8") as file:
        data = json.load(file)

    # 统计superclass和subclass数量
    superclass_counter = Counter(sample["superclass"] for sample in data)
    subclass_counter = Counter((sample["superclass"], sample["subclass"] or sample["class"] or "null") for sample in data)

    # 设置字体
    matplotlib.rcParams.update({
        'font.size': 7, 'font.family': 'sans-serif', 'font.sans-serif': 'Arial'
    })

    # 绘图
    plot_pie_chart(superclass_counter, subclass_counter)

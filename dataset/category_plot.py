import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import numpy as np
import json
import matplotlib
from adjustText import adjust_text


def interpolate(color_a, color_b, t):
    # 'color_a' and 'color_b' are RGB tuples
    # 't' is a value between 0.0 and 1.0
    # this is a naive interpolation
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

def lightening_colors(color_a, number_of_colors):
    if len(color_a) == 4:  # RGBA
        alphas = np.linspace(0.0, 1.0, num=number_of_colors + 2).tolist()[1:-1]
        rgb = color_a[:3]
        return [rgb + (a,) for a in alphas][::-1]

    color_b = (1, 1, 1)
    colors = [interpolate(color_a, color_b, t / number_of_colors) for t in range(number_of_colors + 2)]
    return colors[1:-1]

# Threshold
def filter_names(n=1000, m=1000, max_=np.Inf):
    # Prepare data for filtering
    filtered_superclass_counts = defaultdict(int)
    filtered_subclass_counts = defaultdict(int)

    minors = set()
    for superclass, count in superclass_counts.items():
        if superclass == "null":
            continue
        if count > n:
            filtered_superclass_counts[superclass] += count
        else:
            filtered_superclass_counts['Others'] += count
            minors.add(superclass)

    for (superclass, subclass), count in subclass_counts.items():
        if superclass == "null":
            continue
        if not subclass:
            raise ValueError(f"{superclass} {subclass}")
        if superclass not in minors:
            if max_ >= count > m:
                filtered_subclass_counts[(superclass, subclass)] = count
            else:
                filtered_subclass_counts[(superclass, 'Others')] += count
        else:
            filtered_subclass_counts[('Others', 'Others')] += count

    lb_sz = [(lb, sz) for lb, sz in filtered_superclass_counts.items()]
    lb_sz = sorted(lb_sz, key=lambda x: x[1], reverse=True)
    superclasses = [lb for lb, sz in lb_sz]
    superclass_sizes = [sz for lb, sz in lb_sz]

    sub_labels = {key: [] for key in superclasses}
    sub_sizes = {key: [] for key in superclasses}

    for (superclass, subclass), count in filtered_subclass_counts.items():
        sub_labels[superclass].append(subclass)
        sub_sizes[superclass].append(count)

    return superclasses, superclass_sizes, sub_labels, sub_sizes


# Plot
def plot_main():
    inner_width = 0.75
    startangle = 45
    fig, ax = plt.subplots(figsize=(9, 7))

    superclasses, superclass_sizes, sub_labels, sub_sizes = filter_names()
    rotation_labels = [superclasses[i] for i in range(len(superclasses)) if superclass_sizes[i] <= 0.25 * sum(superclass_sizes)]

    # Draw the inner pie for superclasses
    wedges, texts = ax.pie(
        superclass_sizes, labels=superclasses, startangle=startangle,
        radius=inner_width, wedgeprops=dict(width=inner_width),
        rotatelabels=True, labeldistance=0.4, textprops={'fontsize': 5})

    # only rotate small fraction labels
    for i, (wedge, text) in enumerate(zip(wedges, texts)):
        label = superclasses[i]
        theta1, theta2 = wedge.theta1, wedge.theta2
        angle = (theta1 + theta2) / 2
        if label in rotation_labels:
            rotation_angle = angle
            text.set_rotation(rotation_angle)
        else:
            text.set_rotation(0)

    colors_rgba = [wedge.get_facecolor() for wedge in wedges]

    # Draw the outer pie for subclasses
    sub_lb = []
    sub_sz = []
    sub_colors = []
    for ii, superclass in enumerate(superclasses):
        lb_sz = [(lb, sz) for lb, sz in zip(sub_labels[superclass], sub_sizes[superclass])]
        lb_sz = sorted(lb_sz, key=lambda x: x[1], reverse=True)
        sub_lb.extend(lb for lb, sz in lb_sz)
        sub_sz.extend(sz for lb, sz in lb_sz)
        sub_colors.extend(lightening_colors(colors_rgba[ii], len(lb_sz)))

    wedges2, texts = ax.pie(
        sub_sz, labels=sub_lb, startangle=startangle,
        colors=sub_colors,
        radius=1, wedgeprops=dict(width=1-inner_width),
        # rotatelabels=True,
        labeldistance=1 + 0.02)

    # Adjust text positions to avoid overlap

    # adjust_text(texts,
    #             only_move={"text": "xy", "static": "xy", "explode": "xy", "pull": "xy"},
    #             arrowprops=dict(arrowstyle='-', color='grey', lw=0.5, shrinkA=2),
    #             min_arrow_len=3,
    #             # expand_points=(1.2, 1.4),
    #             # expand_text=(1.2, 1.4),
    #             force_text=(1.1, 1.2),
    #             # force_static=(0.3, 1.0),
    #             iter_lim=1000,
    #             # avoid_text=True
    #             )

    bbox_props = dict(boxstyle="square", fc="w", ec="w", lw=0)
    kw = dict(arrowprops=dict(arrowstyle='-', color='grey', lw=0.5),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges2):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(texts[i].get_text(), xy=(x, y), xytext=(1.2*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, fontsize=4, **kw)

        texts[i].set_visible(False)

    # plt.tight_layout()
    plt.savefig("metabolites_categories_chart.png", dpi=400)
    plt.savefig("metabolites_categories_chart.svg")


def plot_superclass(superclass):
    inner_width = 0
    startangle = 45
    fig, ax = plt.subplots(figsize=(9, 7))

    superclasses, superclass_sizes, sub_labels, sub_sizes = filter_names(n=0, m=20, max_=50)

    # Draw the pie for subclasses
    sub_lb = []
    sub_sz = []
    lb_sz = [(lb, sz) for lb, sz in zip(sub_labels[superclass], sub_sizes[superclass])]
    lb_sz = sorted(lb_sz, key=lambda x: x[1], reverse=True)
    sub_lb.extend(lb for lb, sz in lb_sz)
    sub_sz.extend(sz for lb, sz in lb_sz)

    # for lb in sub_lb:
    #     print(lb)
    # return

    wedges2, texts = ax.pie(
        sub_sz, labels=sub_lb, startangle=startangle,
        # colors=sub_colors,
        radius=1, wedgeprops=dict(width=1-inner_width),
        # rotatelabels=True,
        labeldistance=1 + 0.02)

    bbox_props = dict(boxstyle="square", fc="w", ec="w", lw=0)
    kw = dict(arrowprops=dict(arrowstyle='-', color='grey', lw=0.5),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges2):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(texts[i].get_text(), xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

        texts[i].set_visible(False)

    plt.savefig(f"drug_categories_{superclass}.png", dpi=400)
    plt.savefig(f"drug_categories_{superclass}.svg")


with open('metabolites_class.json', encoding="utf-8") as f:
    data_samples = json.load(f)
superclass_counts = Counter(sample["superclass"] for sample in data_samples)
subclass_counts = Counter((sample["superclass"], sample["subclass"] or sample["class"] or "Null") for sample in data_samples)

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
plt.rcParams.update({'font.size': 7, 'font.family': 'sans-serif', 'font.sans-serif': 'Arial'})

plot_main()
# plot_superclass('Organoheterocyclic compounds')
# plot_superclass('Benzenoids')
# plot_superclass('Organic acids and derivatives')
# plot_superclass('Lipids and lipid-like molecules')
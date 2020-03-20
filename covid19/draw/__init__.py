from matplotlib import pyplot as plt


def plot(x=None, y=None, legend=None, title=None, x_label=None, y_label=None, figsize=(15, 10), grid=True,
         ticks=(None, None), fontsize=14, t_fontsize=18, linewidth=4):
    if figsize is not None:
        plt.figure(figsize=figsize)
    assert y is not None
    if x is None:
        plt.plot(y, linewidth=linewidth)
    if x is not None:
        plt.plot(x, y, linewidth=linewidth)
    if grid:
        plt.grid(grid)
    plt.yticks(fontsize=fontsize)
    if ticks[0] is not None:
        plt.yticks(y[::ticks[0]], fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    if x is None and ticks[1] is not None:
        plt.xticks(fontsize=fontsize)
    if x is not None and ticks[1] is not None:
        plt.xticks(x[::ticks[1]], fontsize=fontsize)
    if title is not None:
        plt.title(title, fontsize=t_fontsize)
    if x_label is not None:
        plt.xlabel(x_label, fontsize=fontsize)
    if y_label is not None:
        plt.ylabel(y_label, fontsize=fontsize)
    if legend is not None:
        plt.legend(legend, fontsize=fontsize)

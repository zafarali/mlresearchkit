import matplotlib
matplotlib.use('Agg') # for use on servers
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

REASONABLE_DEFAULTS={
    'font_scale':1.5,
    'fill_betwee_alpha':0.3,
    'plot_linewidth': 1.5,
    'palette': 'colorblind',
    'style': 'whitegrid',
    'context': 'paper'
}

def set_seaborn_defaults(palette=REASONABLE_DEFAULTS['palette'],
                         style=REASONABLE_DEFAULTS['style'],
                         context=REASONABLE_DEFAULTS['context'],
                         font_scale=REASONABLE_DEFAULTS['font_scale']):
    sns.set_color_codes(palette)
    sns.set_style(style)
    sns.set_context(context, font_scale=font_scale)



def plot_curve(ax, data, label, color, scale_x=1):
    """
    Plots a single experiment on an axis.
    :param ax:
    :param data:
    :param label:
    :param color:
    :param scale_x:
    :return:
    """
    if type(data) is tuple:
        mean, std = data
    else:
        mean, std = data, None

    x_data = np.arange(len(mean)) * scale_x

    ax.plot(x_data, mean, linewidth=1.5, color=color, label=label)
    if std is not None:
        ax.fill_between(x_data, mean + std, mean - std, alpha=0.3,
                        edgecolor=color, facecolor=color)

    return ax

def plot_experiments(list_of_data,
                     palette='colorblind',
                     labels=None,
                     figsize=(12, 8),
                     title='Results',
                     x_label='Iterations',
                     y_label='',
                     legend_location='best',
                     scale_x=1,
                     logx=False,
                     logy=False):
    """
    :param list_of_data: Data must contain a single list/np.array of data with what will be plotted
                        or tuples with the first element as the mean of the data and the 2nd as the std deviation
    :return:
    """
    colors = sns.color_palette(palette, n_colors=len(list_of_data))
    if labels is None:
        labels_to_print = [''] * len(list_of_data)
    else:
        labels_to_print = labels

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    for color, label, data in zip(colors, labels_to_print, list_of_data):
        ax = plot_curve(ax, data, label, color, scale_x=scale_x)

    if logx:
        ax.semilogx()
    if logy:
        ax.semilogy()

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)


    if labels is not None:
        fig.legend(loc=legend_location)

    return fig
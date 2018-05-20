import argparse
from ..plotting.loaders import load_data_for_experiments
from ..plotting.plot import plot_experiments

def create_argparse():
    parser = argparse.ArgumentParser('plot subroutine',
                                     description='Plots data')

    parser.add_argument("--paths", help="Glob paths to the folder with data. "
                                        "For example, if you have experiments under"
                                        "'experiment/method1/$seed/data.csv' and "
                                        "'experiment/method2/$seed/data.csv'. pass them as:"
                                        "`--paths 'experiment/method1/*/data.csv' "
                                        "'experiment/method2/*/data.csv'`",
                        nargs='+',
                        required=True)
    parser.add_argument('--labels', default=None, nargs='+',
                        help='Labels for the plot')
    parser.add_argument('--column', default=None, type=int,
                        help='The axes of the data to return.')
    parser.add_argument('--title', default='Results')
    parser.add_argument('--xlabel', default='Iterations')
    parser.add_argument('--ylabel', default='')
    parser.add_argument('--logx', default=False, action='store_true')
    parser.add_argument('--logy', default=False, action='store_true')
    parser.add_argument('--palette', default='colorblind')
    parser.add_argument('--legend_location', default='best')
    parser.add_argument('--save-type', default='auto')
    parser.add_argument('--truncate-to-min', default=False, action='store_true')
    parser.add_argument('--smoothing-window', default=0, type=int)
    parser.add_argument('--scale-x', default=1, type=int,
                        help='How to scale the x axis')
    parser.add_argument('--figsize', default=(12, 8), nargs='+', type=int)
    parser.add_argument('--save-name', default=None)
    parser.add_argument('--to-pdf', default=False, action='store_true')
    parser.add_argument('--to-png', default=False, action='store_true')
    parser.add_argument('--silent', default=False, action='store_true')

    return parser


def load_and_plot_data(args):
    data = load_data_for_experiments(args.paths,
                                     save_type=args.save_type,
                                     truncate_to_min=args.truncate_to_min,
                                     smoothing_window=args.smoothing_window,
                                     column=args.column,
                                     verbose=not args.silent)

    if args.save_name is None:
        args.save_name = args.title.replace(' ', '')
    fig = plot_experiments(data,
                           palette=args.palette,
                           labels=args.labels,
                           figsize=args.figsize,
                           title=args.title,
                           x_label=args.xlabel,
                           y_label=args.ylabel,
                           legend_location=args.legend_location,
                           scale_x=args.scale_x,
                           logx=args.logx,
                           logy=args.logy)

    if args.to_pdf:
        fig.savefig(args.save_name + '.pdf')
    if args.to_png:
        fig.savefig(args.save_name + '.png')



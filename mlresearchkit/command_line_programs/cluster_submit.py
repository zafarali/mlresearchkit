import argparse
from ..computecanada.parsers import create_cc_arguments, parse_cc_argument, load_all_modules

def create_argparse():
    parser = argparse.ArgumentParser('cluster-submit subroutine',
                                     description='This will default to SLURM (i.e. CEDAR)')

    parser.add_argument('program',
                        metavar='PATH_TO_PYTHON_FILE',
                        help='The python file to run')

    parser.add_argument_group('Program arguments')
    parser.add_argument('-submit', '--submit', default=False,
                        action='store_true',
                        help='By default, cluster-submit will do nothing.'
                             'You MUST provide -submit to force a submit.')

    parser.add_argument('-virtualenv', '--virtualenv', default='',
                        metavar='PATH_TO_VENV',
                        help='The virtual environment to run this script in.')

    parser.add_argument('-programargs', '--programargs', default='',
                        metavar='ARGUMENTS FOR THE PROGRAM',
                        help='The arguments to run this program with')

    parser.add_argument_group('Cluster specific arguments')
    create_cc_arguments(parser)
    return parser


def create_submission_file(args):
    header, modules = parse_cc_argument(args)

    header += '\n'+load_all_modules(modules)
    if args.virtualenv != '':
        header += '\n source {}'.format(args.virtualenv)
    header += '\npython {} {}'.format(args.program, args.programargs)
    return header, modules


import time
import argparse
from mlresearchkit.computecanada import clusters
from mlresearchkit.computecanada.slurm.parsers import create_slurm_header
from mlresearchkit.computecanada.moab.parsers import create_moab_header
from mlresearchkit.computecanada.moab import modules as moab_modules
from mlresearchkit.computecanada.slurm import modules as slurm_modules

_TIME_HELP_STRING="""Time for the job to run:
FOR SLURM: Acceptable time formats include "minutes", "minutes:seconds", \
"hours:minutes:seconds", "days-hours", "days-hours:minutes" \
and "days-hours:minutes:seconds".
FOR PBS: "hours:minutes:seconds"""

def create_cc_arguments(parser):
    """
    Create command line arguments for compute canada clusters
    :param parser: the Argparse instance
    :return:
    """
    parser.add_argument('--cc_account', required=True)
    parser.add_argument('--cc_job_name',
                        help='Name of the job to run', type=str,
                        default='JOB{}'.format(time.time()))
    parser.add_argument('--cc_gpus', type=int, default=0,
                        help='Number of GPUs to request')
    parser.add_argument('--cc_log', type=str, default='./',
                        help='Log directory')
    parser.add_argument('--cc_time', type=str,
                        help=_TIME_HELP_STRING,
                        default='00:15:00')
    parser.add_argument('--cc_cpus', type=int, default=1,
                        help='CPUs to request per task.')
    parser.add_argument('--cc_tasks', type=int, default=1,
                        help='Number of tasks.')
    parser.add_argument('--cc_mem', default=8192, type=int,
                        help='The amount of memory in MB for the job.')
    parser.add_argument('--cc_queue', default='debug', type=str,
                        help='The queue to run on.')
    parser.add_argument('--cc_other', '--cc-other', default='',
                        help='Other arguments to append to the run')
    parser.add_argument('--cc_mail', metavar='YOU@MAIL.COM', default=False, type=str,
                        help='Sends a mail to you when done')
    parser.add_argument('--cc_cluster', default=clusters.CEDAR, type=str,
                        help=('Cluster to format headers for. '
                              'One from {}'.format(clusters.AVAILABLE_CLUSTERS)))
    return parser

def parse_cc_argument(parsed_args):
    """
    Parses the arguments for the compute canada runner
    :param parsed_args:
    :return:
    """
    if parsed_args.cc_cluster in clusters.SLURM_CLUSTERS:
        return create_slurm_header(parsed_args), slurm_modules
    elif parsed_args.cc_cluster in clusters.MOAB_CLUSTERS:
        return create_moab_header(parsed_args), moab_modules
    else:
        raise ValueError(
            'Unknown cluster {}. Must select one of {}'.format(
                parsed_args.cc_cluster, clusters.AVAILABLE_CLUSTERS))

def load_all_modules(modules):
    tmpstr = ''
    tmpstr += modules.CURRENT_DIRECTORY+'\n'
    tmpstr += '\n'
    tmpstr += modules.REQUIREMENTS+'\n'

    for module in modules.MODULES_LIST:
        tmpstr += module+'\n'

    return tmpstr
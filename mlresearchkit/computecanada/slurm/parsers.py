import argparse
import time

TEMPLATE = """#!/bin/bash
#SBATCH --account={JOBACCOUNT}
#SBATCH --time={JOBTIME}
#SBATCH --job-name={JOBNAME}
#SBATCH --ntasks={N_CPUS}
#SBATCH -o {LOGDIR}/{OUTFILE}.out
#SBATCH -e {LOGDIR}/{ERRORFILE}.err
#SBATCH --mem={JOBMEM}M"""

def create_slurm_header(args):
    """
    Give a parsed argparse object, create a header for the slurm job
    :param args:
    :return:
    """
    tmpstr = TEMPLATE.format(JOBACCOUNT=args.cc_account,
                             JOBTIME=args.cc_time,
                             N_CPUS=args.cc_cpus,
                             JOBNAME=args.cc_job_name,
                             OUTFILE=args.cc_job_name,
                             ERRORFILE=args.cc_job_name,
                             JOBMEM=args.cc_mem,
                             LOGDIR=args.cc_log)

    if args.cc_gpus > 0: tmpstr += parse_gpu_arguments(args)
    if args.cc_mail is not False: tmpstr += parse_mail_arguments(args)

    return tmpstr

def parse_gpu_arguments(args):
   tmpstr = '\n#SBATCH --gres=gpu:{}'.format(args.cc_gpus)
   # tmpstr += '\n#SBATCH --cpus-per-task={}'.format(6 if args.cc_cluster_name=='cedar' else 16)
   return tmpstr

def parse_mail_arguments(args):
    tmpstr = """\n#SBATCH --mail-type=ALL
#SBATCH --mail-user={}"""
    return tmpstr.format(args.cc_mail)

def create_slurm_arguments(parser):
    """
    Create command line arguments for SLURM
    :param parser:
    :return:
    """
    parser.add_argument('-cc-job-name', '--cc-job-name',
                        help='Name of the job to run', type=str,
                        default='SLURM{}'.format(time.time()))

    parser.add_argument('--cc-gpus', '--cc-gpus', type=int, default=0,
                        help='Number of GPUs to request')
    parser.add_argument('--cc-log', '--cc-log', type=str, default='./',
                        help='Log directory')
    parser.add_argument('--cc-time', '--cc-time', type=str,
                        help="""Time for the job to run: Acceptable time formats include "minutes",
                        "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes"
                        and "days-hours:minutes:seconds".""",
                        default='0-00:15:00')
    parser.add_argument('-cc-cpus', '--cc-cpus', type=int, default=1,
                        help='CPUs to request')
    parser.add_argument('-cc-mem', '--cc-mem', default=8192, type=int)
    parser.add_argument('-cc-account', '--cc-account', required=True)
    parser.add_argument('-cc-other', '--cc-other', default='',
                        help='Other arguments to append to the run')
    parser.add_argument('-cc-mail', '--cc-mail', metavar='YOU@MAIL.COM', default=False, type=str,
                        help='Sends a mail to you when done')
    return parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Test Compute Canada runner')
    create_slurm_arguments(parser)
    args = parser.parse_args()
    print(create_slurm_header(args))

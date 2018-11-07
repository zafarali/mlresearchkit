import argparse

TEMPLATE = """#!/bin/bash
#SBATCH --account={JOBACCOUNT}
#SBATCH --time={JOBTIME}
#SBATCH --job-name={JOBNAME}
#SBATCH --ntasks={N_TASKS}
#SBATCH --cpus-per-task={N_CPUS}
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
                             N_TASKS=args.cc_tasks,
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

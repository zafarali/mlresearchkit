TEMPLATE = """#!/bin/bash
#PBS -l nodes=1:ppn={N_CPUS}
#PBS -l walltime={JOBTIME}
#PBS -A {JOBACCOUNT}
#PBS -N {JOBNAME}
#PBS -o {LOGDIR}/{OUTFILE}.txt
#PBS -e {LOGDIR}/{ERRORFILE}.txt
#PBS -q {QUEUE}
#PBS -l mem={JOBMEM}MB"""

def create_moab_header(args):
    """
    Give a parsed argparse object, create a header for the moab job
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
                             LOGDIR=args.cc_log,
                             QUEUE=args.cc_queue)

    if args.cc_gpus > 0: tmpstr += parse_gpu_arguments(args)
    if args.cc_mail is not False: tmpstr += parse_mail_arguments(args)

    return tmpstr

def parse_gpu_arguments(args):
   tmpstr = '\n#PBS -l gpus={}:exclusive_process'.format(args.cc_gpus)
   return tmpstr

def parse_mail_arguments(args):
    tmpstr = """\n#PBS -m abe
#PBS -M {}"""
    return tmpstr.format(args.cc_mail)

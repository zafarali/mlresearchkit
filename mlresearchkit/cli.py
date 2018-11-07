import sys
from . import __version__, __author__
HELP = """mlresearchkit is a set of meta-tools to do research.
Really what we are trying to do is automate the pain of getting a new 
research environment for machine learning setup. Here are some of the things 
you can do with this tool via the command line:
# Run a python script on a cluster (for example on Compute Canada)
use `mlresearchkit cluster-submit` to run things!
# Set up a new research environment
use `mlresearchkit new-env` to set up a template directory for a new research environment.
# Plot data easily
use `mlresearchkit plot`
"""
WELCOME = '# mlresearchkit {} created by {}'.format(__version__, __author__)
def main():
    if len(sys.argv) < 2:
        print(WELCOME)
        print(HELP)
        sys.exit(0)

    if sys.argv[1] == 'cluster-submit':
        # quickly submit to clusters!
        from .command_line_programs import cluster_submit
        parser = cluster_submit.create_argparse()
        args = parser.parse_args(sys.argv[2:])
        prepared_file, modules = cluster_submit.create_submission_file(args)
        if not args.submit:
            # dry run, just print to output
            print(prepared_file)
        else:
            job_name = '{}_submission.sh'.format(args.cc_job_name)
            # this is serious, submit it to a cluster!
            print('Prepared submission file in {}'.format(job_name))
            open(job_name, 'w').write(prepared_file) # save the submission file
            print('Now submitting...')
            import subprocess
            subprocess.Popen('{} {}'.format(modules.JOB_SCHEDULER, job_name))
        sys.exit(0)

    elif sys.argv[1] == 'new-env':
        print(WELCOME)
        print('New research environment')
        sys.exit(0)
    elif sys.argv[1] == 'plot':
        from .command_line_programs import plot
        parser = plot.create_argparse()
        args = parser.parse_args(sys.argv[2:])
        plot.load_and_plot_data(args)
    else:
        print('Unknown command was given!')
        sys.exit(1)
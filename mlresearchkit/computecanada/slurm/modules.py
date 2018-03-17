"""
Modules to quickly build scripts to run on slurm
"""

# move to current directory
CURRENT_DIRECTORY = "cd $SLURM_SUBMIT_DIR"

# defaults to run
REQUIREMENTS = ""

# note these are using the new installed modules described from REQUIREMENTS
PYTHON35 = "module load python/3.5.2"
SCIPY = "module scipy-stack/2017b"
CUDA8 = "module load cuda/8.0.44"
CUDNN7 = "module load cudnn/7.0"
QT5 = "module load qt"

JOB_SCHEDULER = "sbatch"

MODULES_LIST = (PYTHON35, SCIPY, CUDA8, CUDNN7, QT5)

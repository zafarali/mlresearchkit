"""
Modules to quickly build scripts to run on moab
"""

# move to current directory
CURRENT_DIRECTORY = "cd $PBS_O_WORKDIR"

# defaults to run
REQUIREMENTS = "source /software/soft.computecanada.ca.sh"

# note these are using the new installed modules described from REQUIREMENTS
PYTHON35 = "module load python/3.5.2"
SCIPY = "module scipy-stack/2017b"
CUDA8 = "module load cuda/8.0.44"
CUDNN7 = "module load cudnn/7.0"
QT5 = "module load qt"

MODULES_LIST = (PYTHON35, SCIPY, CUDA8, CUDNN7, QT5)

JOB_SCHEDULER = "qsub"

# these are the old and soon to be deprecated modules
OLD_FOSS = "module load foss/2015b"
OLD_PYTHON35 = "module load Python/3.5.2"
OLD_CUDA75 = "module load CUDA_Toolkit/7.5"
OLD_CUDNN5 = "module load cuDNN/5.0-ga"
OLD_TENSORFLOW = "module load Tensorflow/1.0.0-Python-3.5.2"
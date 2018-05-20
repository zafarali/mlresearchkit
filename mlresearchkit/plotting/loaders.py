import glob
import numpy as np
import torch
import pandas as pd
import logging
def find_file_paths(glob_path):
    """
    Files file paths matching a glob_path
    Example Input: "/experiments/experiment_name/*/results.csv"
    where * catches the fact that folders hold different replicates
    :param glob_path:
    :return:
    """
    file_paths = glob.glob(glob_path)
    if len(file_paths) == 0:
        raise ValueError('glob_path is malformed, no paths found.: {}'.format(glob_path))

    return file_paths

# load data from different types of files
def load_csv(file_path):
    return pd.read_csv(file_path).values

def load_npy(file_path):
    return np.load(file_path)

def load_torch(file_path):
    return torch.load(file_path).numpy()

def detect_save_type(path):
    if '.csv' in path:
        save_type = 'csv'
    elif '.npy' in path:
        save_type = 'npy'
    elif '.pyt' in path:
        save_type = 'pytorch'
    else:
        raise AttributeError('Unable to detect save_type.')

    return save_type

def load_experiment(glob_path,
                    save_type='auto',
                    truncate_to_min=False,
                    column=None,
                    verbose=False):
    """

    :param glob_path:
    :param save_type:
    :param truncate_to_min:
    :return:
    """
    if save_type == 'auto':
        save_type = detect_save_type(glob_path)

    paths = find_file_paths(glob_path)

    if verbose: print('{} replicates for {}'.format(len(paths), glob_path))

    if save_type == 'csv':
        loader = load_csv
    elif save_type == 'npy':
        loader = load_npy
    elif save_type == 'torch':
        loader = load_torch
    else:
        raise ValueError('Unknown save_type.')

    min = np.Inf
    data = []
    for path in paths:
        loaded_data = loader(path)
        if truncate_to_min and len(loaded_data) < min:
            min = len(loaded_data)
        if column is not None:
            loaded_data = loaded_data[:, column]
        data.append(loaded_data)

    # truncate all the data to be of the same length
    if truncate_to_min:
        data_to_return = []
        for loaded_data in data:
            data_to_return.append(loaded_data[:min])
    else:
        data_to_return = data

    # print(data_to_return)
    data_to_return = np.stack(data_to_return, axis=1).astype(np.float_)

    return data_to_return

def calculate_mean_and_std(data, smoothing_window=0):
    """

    :param data:
    :param smoothing_window:
    :return:
    """
    if smoothing_window > 0:
        #TODO: verify this
        data = pd.DataFrame(data).rolling(smoothing_window).mean()

    data_mean = data.mean(axis=1)
    try:
        data_std = data.std(axis=1)
    except AttributeError:
        data_std = None
        logging.warning('Could not compute standard deviation.')
    return data_mean, data_std


def load_data_for_experiments(glob_path_to_experiments,
                              save_type='auto',
                              truncate_to_min=False,
                              smoothing_window=0,
                              column=None,
                              verbose=False):
    """

    :param glob_path_to_experiments:
    :param save_type:
    :param truncate_to_min:
    :return:
    """
    data_to_plot = []
    if verbose: print('Total Number of Paths: {}'.format(len(glob_path_to_experiments)))
    for glob_path in glob_path_to_experiments:
        data_to_plot.append(calculate_mean_and_std(
                                load_experiment(glob_path,
                                                save_type=save_type,
                                                truncate_to_min=truncate_to_min,
                                                column=column,
                                                verbose=verbose),
                                smoothing_window=smoothing_window))

    return data_to_plot

from random import sample
from typing import Tuple, Union, List

import numpy as np
import torch
from sklearn.base import BaseEstimator


def preprocess_waldo_estimation(
    parameters: Union[np.ndarray, torch.Tensor], 
    samples: Union[np.ndarray, torch.Tensor], 
    method: str,
    estimator: object
) -> Tuple[Union[np.ndarray, torch.Tensor], ...]:
    if method == 'prediction':
        # make sure types are correct for:
        if isinstance(estimator, torch.nn.Module):
            # PyTorch models
            if isinstance(parameters, np.ndarray):
                parameters = torch.from_numpy(parameters)
            if isinstance(samples, np.ndarray):
                samples = torch.from_numpy(samples)
        if isinstance(estimator, BaseEstimator):
            # Scikit-Learn models
            if isinstance(parameters, torch.Tensor):
                parameters = parameters.numpy()
            if isinstance(samples, torch.Tensor):
                samples = samples.numpy()
    else:
        # for posterior estimation we currently support `SBI` from mackelab, which uses PyTorch
        if isinstance(parameters, np.ndarray):
            parameters = torch.from_numpy(parameters)
        if isinstance(samples, np.ndarray):
            samples = torch.from_numpy(samples)
    return parameters, samples


def preprocess_waldo_evaluation(
    parameters: Union[np.ndarray, torch.Tensor], 
    samples: Union[np.ndarray, torch.Tensor], 
    method: str,
    estimator: object
) -> Tuple[Union[np.ndarray, torch.Tensor], ...]:
    return preprocess_waldo_estimation(parameters, samples, method, estimator)


def preprocess_waldo_computation(
    parameters: np.ndarray,
    conditional_mean: Union[np.ndarray, List],
    conditional_var: Union[np.ndarray, List],
    param_dim: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if param_dim == 1:
        parameters = parameters.reshape(-1, param_dim)
        if isinstance(conditional_mean, List):
            # method == posterior
            conditional_mean = np.vstack(conditional_mean)
            conditional_var = np.vstack(conditional_var)
        else:
            # method == prediction
            conditional_mean = conditional_mean.reshape(-1, param_dim)
            conditional_var = conditional_var.reshape(-1, param_dim)
    else:
        # so that when sliced it is still 2-dimensional
        parameters = parameters.reshape(-1, 1, param_dim)
        if isinstance(conditional_mean, np.ndarray):
            # method == prediction; this should be rarely used
            conditional_mean = conditional_mean.reshape(-1, 1, param_dim)
            conditional_var = conditional_var.reshape(-1, param_dim, param_dim)
    
    return parameters, conditional_mean, conditional_var
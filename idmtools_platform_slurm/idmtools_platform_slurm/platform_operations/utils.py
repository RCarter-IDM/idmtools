"""
This is SlurmPlatform operations utils.

Copyright 2021, Bill & Melinda Gates Foundation. All rights reserved.
"""
import os
import subprocess
from typing import Dict
from idmtools.core import ItemType
from idmtools.entities import Suite
from idmtools.entities.experiment import Experiment
from logging import getLogger

logger = getLogger(__name__)


class SlurmItem:
    """
    Represent Slurm Object
    """

    def __init__(self, metas: Dict):
        for key, value in metas.items():
            setattr(self, key, value)

    def get_platform_object(self):
        return self


class SlurmSuite(SlurmItem):
    """
    Represent Slurm Suite
    """

    def __init__(self, metas: Dict):
        super().__init__(metas)
        self.item_type = ItemType.SUITE


class SlurmExperiment(SlurmItem):
    """
    Represent Slurm Experiment
    """

    def __init__(self, metas: Dict):
        super().__init__(metas)
        self.item_type = ItemType.EXPERIMENT


class SlurmSimulation(SlurmItem):
    """
    Represent Slurm Simulation
    """

    def __init__(self, metas: Dict):
        super().__init__(metas)
        self.item_type = ItemType.SIMULATION


def clean_experiment_name(experiment_name: str) -> str:
    """
    Handle some special characters in experiment names.
    Args:
        experiment_name: name of the experiment
    Returns:the experiment name allowed for use
    """
    import re
    chars_to_replace = ['/', '\\', ':', "'", '"', '?', '<', '>', '*', '|', "\0", "(", ")", "[", "]", '`', ',', '!', '$',
                        '&', '"', ' ']
    clean_names_expr = re.compile(f'[{re.escape("".join(chars_to_replace))}]')

    experiment_name = clean_names_expr.sub("_", experiment_name)
    return experiment_name.encode("ascii", "ignore").decode('utf8').strip()


def add_dummy_suite(experiment: Experiment, suite_name: str = None, tags: Dict = None) -> Suite:
    """
    Create Suite parent for given experiment
    Args:
        experiment: idmtools Experiment
        suite_name: new Suite name
        tags: new Suite tags
    Returns:
        Suite
    """
    if suite_name is None:
        suite_name = 'Suite'
    suite = Suite(name=suite_name)

    if not tags:
        suite.tags = tags

    # add experiment
    suite.add_experiment(experiment)

    return suite


def get_max_array_size():
    """
    Get Slurm MaxArraySize from configuration.
    Returns:
        Slurm system MaxArraySize
    """
    try:
        output = subprocess.check_output(['scontrol', 'show', 'config'])
        for line in output.decode().splitlines():
            if line.startswith("MaxArraySize"):
                max_array_size = int(line.split("=")[1])
                return max_array_size - 1
    except (subprocess.CalledProcessError, IndexError, ValueError):
        pass

    return None


def check_home(directory: str) -> bool:
    """
    Check if a directory is under HOME.
    Args:
        directory: a directory

    Returns:
        True/False
    """
    home = os.path.expanduser("~").replace('\\', '/')
    directory = directory.replace('\\', '/')
    if directory.startswith(home):
        return True
    else:
        return False

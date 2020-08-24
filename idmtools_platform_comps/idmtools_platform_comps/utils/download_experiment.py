import os
import stat
import sys
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from tqdm import tqdm

from idmtools.core.context import get_current_platform
from idmtools.entities.experiment import Experiment
from idmtools.entities.simulation import Simulation


def get_script_extension():
    if sys.platform in ["linux", "darwin"]:
        return "sh"
    else:
        return "bat"


def download_asset(asset, path):
    os.makedirs(path, exist_ok=True)
    asset.download_to_path(path)


def write_script(simulation: Simulation, path):
    """
    Writes a shell script to execute simulation
    Args:
        simulation:
        path:

    Returns:

    """
    command = str(simulation.task.command)
    sp = os.path.join(path, f"idmtools_run.{get_script_extension()}")
    with open(sp, "w") as sfile:
        sfile.write(command)
    if sys.platform in ["linux", "darwin"]:
        st = os.stat(sp)
        os.chmod(sp, st.st_mode | stat.S_IEXEC)


def write_experiment_script(experiment: Experiment, path: str):
    """
    Write an experiment script
    Args:
        experiment:
        path:

    Returns:

    """
    sp = os.path.join(path, f"idmtools_run.{get_script_extension()}")

    with open(sp, 'w') as sout:
        for sim in experiment.simulations:
            sout.write(f".{os.path.sep}{sim.id}{os.path.sep}idmtools_run.{get_script_extension()}")
    if sys.platform == "linux":
        st = os.stat(sp)
        os.chmod(sp, st.st_mode | stat.S_IEXEC)


def download_experiment(experiment: Experiment, destination: str):
    """
    Downloads experiment to local directory. Usefule for troubleshooting experiments

    Args:
        experiment: Experiment to download
        destination: Destionation Directory

    Returns:

    """
    asset_dir = os.path.join(destination, "Assets")
    os.makedirs(asset_dir, exist_ok=True)
    pool = ThreadPoolExecutor()
    futures = []
    for asset in experiment.assets:
        futures.append(pool.submit(download_asset, asset, asset_dir))

    for sim in experiment.simulations:
        sim_path = os.path.join(destination, sim.id)
        try:
            os.makedirs(sim_path, exist_ok=True)
        except FileExistsError:
            pass

        for output in get_current_platform()._simulations.all_files(sim):
            futures.append(pool.submit(download_asset, output, sim_path))

        write_script(sim, sim_path)
        if sys.platform == "linux" and not os.path.exists(os.path.join(sim_path, "Assets")):
            os.symlink("../Assets", os.path.join(sim_path, "Assets"))

    write_experiment_script(experiment, destination)
    for future in tqdm(as_completed(futures), total=len(futures)):
        pass
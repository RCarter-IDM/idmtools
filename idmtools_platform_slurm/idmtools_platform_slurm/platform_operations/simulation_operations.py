import os
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from os import cpu_count
from typing import List, Dict, Any, Tuple, Type
from uuid import UUID, uuid4
from idmtools.entities import ISimulation
from idmtools.entities.iplatform_metadata import IPlatformSimulationOperations


@dataclass
class SlurmPLatformSimulationOperations(IPlatformSimulationOperations):
    platform: 'SlurmPlatform'
    platform_type: Type = ISimulation

    def get(self, simulation_id: UUID, **kwargs) -> Any:
        raise NotImplementedError("Fetching experiments has not been implemented on the Slurm Platform")

    def create(self, simulation: ISimulation, common_asset_dir = None) -> Tuple[Any, UUID]:
        if common_asset_dir is None:
            common_asset_dir = os.path.join(self.platform.job_directory, simulation.experiment.uid, 'Assets')
        simulation.uid = str(uuid4())
        sim_dir = os.path.join(self.platform.job_directory, simulation.experiment.uid, simulation.uid)
        self.platform._op_client.mk_directory(sim_dir)
        # store sim info in folder
        self.platform._op_client.dump_metadata(simulation, os.path.join(sim_dir, 'simulation.json'))
        self.platform._op_client.link_dir(common_asset_dir, os.path.join(sim_dir, 'Assets'))
        self.send_assets(simulation)
        self.platform._op_client.create_simulation_batch_file(simulation, sim_dir, mail_type=self.platform.mail_type,
                                                     mail_user=self.platform.mail_user)

        return simulation, simulation.uid

    def get_parent(self, simulation: Any, **kwargs) -> Any:
        raise NotImplementedError("Listing assets is not supported on Slurm Yet")

    def batch_create(self, sims: List[ISimulation], **kwargs) -> List[Tuple[Any, UUID]]:
        created = []
        common_asset_dir = os.path.join(self.platform.job_directory, sims[0].experiment.uid, 'Assets')

        for simulation in sims:
            created.append(self.create(simulation))
        return created

    def run_item(self, simulation: ISimulation):
        sim_dir = os.path.join(self.platform.job_directory, simulation.experiment.uid, simulation.uid)
        self.platform._op_client.submit_job(os.path.join(sim_dir, 'submit-simulation.sh'), sim_dir)

    def send_assets(self, simulation: ISimulation):
        for asset in simulation.assets:
            sim_dir = os.path.join(self.platform.job_directory, simulation.experiment.uid, simulation.uid)
            self.platform._op_client.copy_asset(asset, sim_dir)

    def refresh_status(self, simulation: ISimulation):
        raise NotImplementedError("Fetching experiments has not been implemented on the Slurm Platform")

    def get_assets(self, simulation: ISimulation, files: List[str], **kwargs) -> Dict[str, bytearray]:
        ret = dict()
        futures = {}
        base_path = os.path.join(self.platform.job_directory, simulation.experiment.uid, simulation.uid)
        with ThreadPoolExecutor(max_workers=cpu_count()) as pool:
            for file in files:
                futures[pool.submit(self.platform._op_client.download_asset, os.path.join(file, base_path))] = file

            for future in as_completed(futures):
                ret[futures[future]] = future.result()
        return ret

    def list_assets(self, simulation: ISimulation) -> List[str]:
        raise NotImplementedError("Listing assets is not supported on Slurm Yet")
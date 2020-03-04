from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Any, List, Dict, NoReturn
from uuid import UUID

from idmtools.core.cache_enabled import CacheEnabled
from idmtools.entities.iplatform_ops.utils import batch_create_items
from idmtools.entities.simulation import Simulation


@dataclass
class IPlatformSimulationOperations(CacheEnabled, ABC):
    platform: 'IPlatform'
    platform_type: Type

    @abstractmethod
    def get(self, simulation_id: UUID, **kwargs) -> Any:
        """
        Returns the platform representation of an Simulation

        Args:
            simulation_id: Item id of Simulations
            **kwargs:

        Returns:
            Platform Representation of an simulation
        """
        pass

    def pre_create(self, simulation: Simulation, **kwargs) -> NoReturn:
        """
        Run the platform/simulation post creation events

        Args:
            simulation: simulation to run post-creation events
            **kwargs: Optional arguments mainly for extensibility

        Returns:
            NoReturn
        """
        simulation.pre_creation()

    def post_create(self, simulation: Simulation, **kwargs) -> NoReturn:
        """
        Run the platform/simulation post creation events

        Args:
            simulation: simulation to run post-creation events
            **kwargs: Optional arguments mainly for extensibility

        Returns:
            NoReturn
        """
        simulation.post_creation()

    def create(self, simulation: Simulation, do_pre: bool = True, do_post: bool = True, **kwargs) -> Any:
        """
        Creates an simulation from an IDMTools simulation object. Also performs pre-creation and post-creation
        locally and on platform

        Args:
            simulation: Simulation to create
            do_pre: Perform Pre creation events for item
            do_post: Perform Post creation events for item
            **kwargs: Optional arguments mainly for extensibility

        Returns:
            Created platform item and the UUID of said item
        """
        if simulation.status is not None:
            return simulation
        if do_pre:
            self.pre_create(simulation, **kwargs)
        ret = self.platform_create(simulation, **kwargs)
        if do_post:
            self.post_create(simulation, **kwargs)
        return ret

    @abstractmethod
    def platform_create(self, simulation: Simulation, **kwargs) -> Any:
        """
        Creates an simulation on Platform from an IDMTools Simulation Object

        Args:
            simulation: Simulation to create
            **kwargs: Optional arguments mainly for extensibility

        Returns:
            Created platform item and the UUID of said item
        """
        pass

    def batch_create(self, sims: List[Simulation], display_progress: bool = True, **kwargs) -> List[Simulation]:
        """
        Provides a method to batch create simulations

        Args:
            sims: List of simulations to create
            display_progress: Show progress bar
            **kwargs:

        Returns:
            List of tuples containing the create object and id of item that was created
        """
        return batch_create_items(sims, create_func=self.create, display_progress=display_progress,
                                  progress_description="Commissioning Simulations",
                                  **kwargs)

    @abstractmethod
    def get_parent(self, simulation: Any, **kwargs) -> Any:
        """
        Returns the parent of item. If the platform doesn't support parents, you should throw a TopLevelItem error

        Args:
            simulation:
            **kwargs:

        Returns:

        Raise:
            TopLevelItem
        """
        pass

    def to_entity(self, simulation: Any, **kwargs) -> Simulation:
        """
        Converts the platform representation of simulation to idmtools representation

        Args:
            simulation:Platform simulation object

        Returns:
            IDMTools simulation object
        """
        return simulation

    def pre_run_item(self, simulation: Simulation, **kwargs):
        """
        Trigger right before commissioning experiment on platform. This ensures that the item is created. It also
            ensures that the children(simulations) have also been created

        Args:
            simulation: Experiment to commission

        Returns:

        """
        # ensure the item is created before running
        # TODO what status are valid here? Create only?
        if simulation.status is None:
            self.create(simulation, **kwargs)

    def post_run_item(self, simulation: Simulation, **kwargs):
        """
        Trigger right after commissioning experiment on platform.

        Args:
            simulation: Experiment just commissioned

        Returns:

        """
        pass

    def run_item(self, simulation: Simulation, **kwargs):
        """
        Called during commissioning of an item. This should create the remote resource

        Args:
            simulation:

        Returns:

        """
        self.pre_run_item(simulation, **kwargs)
        self.platform_run_item(simulation, **kwargs)
        self.post_run_item(simulation, **kwargs)

    @abstractmethod
    def platform_run_item(self, simulation: Simulation, **kwargs):
        """
        Called during commissioning of an item. This should create the remote resource but not upload assets

        Args:
            simulation: Simulation to run

        Returns:

        """
        pass

    @abstractmethod
    def send_assets(self, simulation: Any, **kwargs):
        pass

    @abstractmethod
    def refresh_status(self, simulation: Simulation, **kwargs):
        """
        Refresh status for simulation object

        Args:
            simulation: Experiment to get status for

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_assets(self, simulation: Simulation, files: List[str], **kwargs) -> Dict[str, bytearray]:
        """
        Get files from simulation

        Args:
            simulation: Simulation to fetch files from
            files: Files to get
            **kwargs:

        Returns:
            Dictionary containting filename and content
        """
        pass

    @abstractmethod
    def list_assets(self, simulation: Simulation, **kwargs) -> List[str]:
        """
        List available files for a simulation

        Args:
            simulation: Simulation to list files for

        Returns:
            List of filenames
        """
        pass
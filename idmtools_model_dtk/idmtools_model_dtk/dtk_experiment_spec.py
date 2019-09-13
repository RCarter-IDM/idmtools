from typing import Type
from idmtools.registry.model_specification import ModelSpecification, get_model_impl, get_model_type_impl
from idmtools.registry.plugin_specification import get_description_impl


class DTKExperimentSpec(ModelSpecification):

    @get_description_impl
    def get_description(self) -> str:
        return "Provides access to the Local Platform to IDM Tools"

    @get_model_impl
    def get(self, configuration: dict) -> 'DTKExperiment':
        """
        Build our local platform from the passed in configuration object

        We do our import of platform here to avoid any weir
        Args:
            configuration:

        Returns:

        """
        from idmtools_model_dtk.dtk_experiment import DTKExperiment
        return DTKExperiment(**configuration)

    @get_model_type_impl
    def get_type(self) -> Type['LocalPlatform']:
        from idmtools_model_dtk.dtk_experiment import DTKExperiment
        return DTKExperiment
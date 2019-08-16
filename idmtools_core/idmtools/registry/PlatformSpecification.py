# Define our platform specific specifications
import typing
from abc import ABC
from logging import getLogger

import pluggy

from idmtools.entities import IPlatform
from idmtools.registry import PluginSpecification
from idmtools.registry.PluginSpecification import PLUGIN_REFERENCE_NAME
from idmtools.registry.utils import load_plugin_map

example_configuration_spec = pluggy.HookspecMarker(PLUGIN_REFERENCE_NAME)
get_platform_spec = pluggy.HookspecMarker(PLUGIN_REFERENCE_NAME)
get_platform_type_spec = pluggy.HookspecMarker(PLUGIN_REFERENCE_NAME)
example_configuration_impl = pluggy.HookimplMarker(PLUGIN_REFERENCE_NAME)
get_platform_impl = pluggy.HookimplMarker(PLUGIN_REFERENCE_NAME)
get_platform_type_impl = pluggy.HookimplMarker(PLUGIN_REFERENCE_NAME)
logger = getLogger(__name__)


class PlatformSpecification(PluginSpecification, ABC):

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.replace('PlatformSpecification', '')

    @example_configuration_spec
    def example_configuration(self):
        """
        Example configuration for platform. This is useful in help or error messages
        Returns:

        """
        raise NotImplementedError("Plugin did not implement example_configuration")

    @get_platform_spec
    def get(self, configuration: dict) -> IPlatform:
        """
        Factor that should return a new platform using the passed in configuration
        Args:
            configuration:

        Returns:

        """
        raise NotImplementedError("Plugin did not implement get")

    @get_platform_type_spec
    def get_type(self) -> typing.Type[IPlatform]:
        pass


class PlatformPlugins:
    def __init__(self) -> None:
        self._plugins = typing.cast(typing.Dict[str, PlatformSpecification],
                                    load_plugin_map('idmtools_platform', PlatformSpecification))

    def get_plugins(self) -> typing.Set[PlatformSpecification]:
        return set(self._plugins.values())

    def get_plugin_map(self) -> typing.Dict[str, PlatformSpecification]:
        return self._plugins
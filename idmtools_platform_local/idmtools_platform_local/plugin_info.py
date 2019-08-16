from typing import Type

from idmtools.registry.PlatformSpecification import example_configuration_impl, get_platform_impl, \
    get_platform_type_impl, PlatformSpecification
from idmtools.registry.PluginSpecification import get_description_impl


from idmtools.entities import IPlatform


LOCAL_PLATFORM_EXAMPLE_CONFIG = """
[LOCAL]
# Timeout of tasks submissions to local platform
default_timeout: int = 30
# Items related to internals of the local platform. Most likely you want to use the defaults
#
# Which work image to use
workers_image: str = 'idm-docker-staging.packages.idmod.org:latest'
# Port to display UI (ie the portion after colon in default URL http://localhost:5000)
workers_ui_port int = 5000
# Docker runtime. On GPU Machines you may want to use nvidia instead of the default
runtime = 'runc'
# Name of idmtools local network
network = 'idmtools'
# redis config
redis_image= 'redis:5.0.4-alpine'
redis_port = 6379
redis_mem_limit = '128m'
redis_mem_reservation: str = '64m'
# Postgres settings
postgres_image = 'postgres:11.4'
postgres_mem_limit = '64m'
postgres_mem_reservation = '32m'
postgres_port = 5432
# Only set this in environments where you need to run as another user. For example, in linux systems
# where you must sudo to run as root you would want to do use this setting to run the container as
# you by getting your user id and group id id -u, id -g and replacing 1000 in the below with the values
# run_as = "1000:1000"
"""


class LocalPlatformSpecification(PlatformSpecification):

    @get_description_impl
    def get_description(self) -> str:
        return "Provides access to the Local Platform to IDM Tools"

    @get_platform_impl
    def get(self, configuration: dict) -> IPlatform:
        """
        Build our local platform from the passed in configuration object

        We do our import of platform here to avoid any weir
        Args:
            configuration:

        Returns:

        """
        from idmtools_platform_local.local_platform import LocalPlatform
        return LocalPlatform()

    @example_configuration_impl
    def example_configuration(self):
        return LOCAL_PLATFORM_EXAMPLE_CONFIG

    @get_platform_type_impl
    def get_type(self) -> Type['LocalPlatform']:
        from idmtools_platform_local.local_platform import LocalPlatform
        return LocalPlatform
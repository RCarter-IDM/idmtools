import os
import json
import collections
from dataclasses import dataclass, field
from typing import Optional, Any

from idmtools.assets import Asset
from idmtools.entities import ISimulation
from idmtools_model_dtk.interventions import DTKEmptyCampaign
# from idmtools_model_dtk.idmtools_model_dtk.interventions import DTKEmptyCampaign


@dataclass(repr=False)
class DTKSimulation(ISimulation):
    config: dict = field(default_factory=lambda: {})
    campaign: dict = field(default_factory=lambda: DTKEmptyCampaign.campaign())
    demographics: collections.OrderedDict = field(default_factory=lambda: collections.OrderedDict())

    def set_parameter(self, name: str, value: any) -> dict:
        self.config[name] = value
        return {name: value}

    def get_parameter(self, name: str, default: Optional[Any] = None):
        """
        Get a parameter in the simulation
        Args:
            name: Name of the parameter
            default: Optional default value for parameter
        Returns: the Value of the parameter
        """
        return self.config.get(name, default)

    def update_parameters(self, params):
        """
        Bulk update config
        Args:
            params: dict with new values
        Returns: None
        """
        self.config.update(params)

    def gather_assets(self):

        config = {"parameters": self.config}

        # Add config and campaign to assets
        self.assets.add_asset(Asset(filename="config.json", content=json.dumps(config)), fail_on_duplicate=False)
        self.assets.add_asset(Asset(filename="campaign.json", content=json.dumps(self.campaign)),
                              fail_on_duplicate=False)

        # Add demographics files to assets
        for filename, content in self.demographics.items():
            self.assets.add_asset(Asset(filename=filename, content=json.dumps(content)), fail_on_duplicate=False)

    def load_files(self, config_path=None, campaign_path=None, demographics_paths=None, force=False):
        """
        Provide a way to load custom files
        Args:
            config_path: custom config file
            campaign_path: custom campaign file
            demographics_paths: custom demographics files (single file or a list)
            force: always return if True, else throw exception is something wrong
        Returns: None
        """

        def load_file(file_path):
            try:
                with open(file_path, 'rb') as f:
                    return json.load(f)
            except IOError:
                if not force:
                    raise Exception(f"Encounter issue when loading file: {file_path}")
                else:
                    return None

        if config_path:
            jn = load_file(config_path)
            if jn:
                if 'parameters' in jn and len(jn) == 1:
                    self.config = jn['parameters']
                else:
                    self.config = jn

                # Refresh demographics file names for new config file
                self.update_config_demographics_filenames(self.demographics.keys())

        if campaign_path:
            jn = load_file(campaign_path)
            if jn:
                self.campaign = jn

        if demographics_paths:
            if isinstance(demographics_paths, collections.Iterable) \
                    and not isinstance(demographics_paths, str):
                demographics_paths = demographics_paths
            else:
                demographics_paths = [demographics_paths]

            for demographics_path in demographics_paths:
                jn = load_file(demographics_path)
                if jn:
                    self.demographics.update({os.path.basename(demographics_path): jn})
                    self.update_config_demographics_filenames(os.path.basename(demographics_path))

    def update_config_demographics_filenames(self, demographics_files):
        """
        Update demographics filenames parameter
        Args:
            demographics_files: single file or a list
        Returns: None
        """
        if isinstance(demographics_files, collections.Iterable) and not isinstance(demographics_files, str):
            demographics_files = demographics_files
        else:
            demographics_files = [demographics_files]

        demo_files = self.config.get("Demographics_Filenames", [])

        # Update config from simulation demographics files
        for filename in demographics_files:
            if filename not in demo_files:
                demo_files.append(filename)
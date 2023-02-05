import logging
from pathlib import Path
from typing import Dict

from nymbus.config.envspec import EnvSpec
from nymbus.config.reader import read_yml
from nymbus.config.step import Step

logger = logging.getLogger(__name__)


class Component(EnvSpec):

    def __init__(self, name: str, yml: dict):
        super().__init__(yml)
        self.name = name

        # Pop the config entries
        config = yml.copy()
        self.steps: Dict[str, Step] = {
            step: Step(step, step_config)
            for step, step_config in config.pop("steps", {}).items()
        }

        # If there are still configs, they are unknown. Print a warning (for retro-compatibility)
        if config:
            logger.warning(f"Unknown configuration in file \"{self.name}\": {config}")

    @classmethod
    def from_file(cls, location: Path):
        return cls(location.parent.name, read_yml(location))


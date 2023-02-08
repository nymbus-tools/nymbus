import logging
from pathlib import Path
from typing import Dict

from nymbus.config.environment import DEFAULT_NYMBUS_EXTENSION
from nymbus.config.envspec import EnvSpec
from nymbus.config.readers.reader import read_yml
from nymbus.config.components.step import Step

logger = logging.getLogger(__name__)


class Component(EnvSpec):

    def __init__(self, name: str, environment: str, yml: dict):
        super().__init__(yml)
        self.name = name
        self.environment = environment

        # Pop the config entries
        config = yml.copy()
        self.context = config.pop("context", None)
        self.steps: Dict[str, Step] = {
            step: Step(step, environment, step_config)
            for step, step_config in config.pop("steps", {}).items()
        }

        # If there are still configs, they are unknown. Print a warning (for retro-compatibility)
        config.pop("env", {})
        if config:
            logger.warning(f"Unknown configuration in component \"{self.name}\", "
                           f"file {self.environment}{DEFAULT_NYMBUS_EXTENSION}: {config}")

    @classmethod
    def from_file(cls, location: Path):
        return cls(location.parent.name, read_yml(location))

import logging

from nymbus.config.envspec import EnvSpec

logger = logging.getLogger(__name__)


class Step(EnvSpec):

    def __init__(self, name: str, yml: dict):
        super().__init__(yml)
        self.name = name

        # Pop the config entries
        config = yml.copy()
        self.command = config.pop("command", "")
        self.image = config.pop("image", None)

        # If there are still configs, they are unknown. Print a warning (for retro-compatibility)
        config.pop("env")
        if config:
            logger.warning(f"Unknown configuration in file \"{self.name}\": {config}")

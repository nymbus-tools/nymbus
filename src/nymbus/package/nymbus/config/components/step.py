import logging

from nymbus.config.environment import DEFAULT_NYMBUS_EXTENSION
from nymbus.config.envspec import EnvSpec
from nymbus.config.images.image import Image
from nymbus.config.template import Template

logger = logging.getLogger(__name__)


class Step(EnvSpec):

    def __init__(self, name: str, environment: str, yml: dict):
        super().__init__(yml)
        self.name = name
        self.environment = environment

        # Pop the config entries
        config = yml.copy()
        self.command = config.pop("command", None)
        image = config.pop("image", None)
        self.image = Image(image) if image else None
        if not self.command and not self.image:
            raise RuntimeError("One of 'command' or 'image' must be not null")
        template = config.pop("template", None)
        self.template = Template(template) if template else None

        # If there are still configs, they are unknown. Print a warning (for retro-compatibility)
        config.pop("env", {})
        if config:
            logger.warning(f"Unknown configuration in component \"{self.name}\", "
                           f"file {self.environment}{DEFAULT_NYMBUS_EXTENSION}: {config}")

import logging
import os
from pathlib import Path

from nymbus.config.component import Component
from nymbus.config.environment import DEFAULT_ENVIRONMENT
from nymbus.config.reader import read_yml, merge_dictionaries
from nymbus.tools.shell import Shell

logger = logging.getLogger(__name__)


class Runner:

    def run(self, context: str = os.getcwd(), environment: str = DEFAULT_ENVIRONMENT, step: str = None) -> None:

        # Read the default
        default_location = Path(context)/f"{DEFAULT_ENVIRONMENT}.yml"
        default = read_yml(default_location)

        # Read the component from the location
        location = Path(context)/f"{environment}.yml"
        specific = read_yml(location)

        # Merge the dictionaries
        result = merge_dictionaries(default, specific)
        component = Component(environment, result)

        # Check step existence
        if step and step not in component.steps:
            raise Exception(f"Step {step} is not {context}")

        # Run it (or them, if step is not specified)
        steps = [step] if step else component.steps
        for target_step in steps:
            target = component.steps[target_step]
            Shell().run(
                target.command,
                env=merge_dictionaries(component.env, target.env)
            )


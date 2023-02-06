import logging
import os
from pathlib import Path

from nymbus.cli.console.output import log_title
from nymbus.config.environment import DEFAULT_ENVIRONMENT
from nymbus.config.readers.combiner import read_component, merge_envs
from nymbus.tools.shell import Shell

logger = logging.getLogger(__name__)


class Runner:

    def run(self, context: str = os.getcwd(), environment: str = DEFAULT_ENVIRONMENT, step: str = None) -> None:

        # Read component
        location = Path(context)
        component = read_component(location, environment)

        # Check step existence
        if step and step not in component.steps:
            raise Exception(f"Step {step} is not in {location}")

        # Run it (or them, if step is not specified)
        steps = [step] if step else component.steps
        for target_step in steps:

            # Get the target step
            target = component.steps[target_step]
            log_title(logger, target.name)

            # Merge envs
            env_spec = merge_envs(location, component, target, environment)
            env_spec.expand()

            # Run it
            Shell().run(
                target.command,
                env=env_spec.env
            )

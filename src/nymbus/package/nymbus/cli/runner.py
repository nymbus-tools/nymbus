import logging
import os
from pathlib import Path

from nymbus.cli.console.output import log_title
from nymbus.config.environment import DEFAULT_ENVIRONMENT
from nymbus.config.readers.combiner import read_component, merge_envs, find_env_spec_locations
from nymbus.tools import system

logger = logging.getLogger(__name__)


class Runner:

    def run(self, component_path: str, environment: str = DEFAULT_ENVIRONMENT, step_name: str = None, context: str = None) -> None:

        # Read component
        location = component_path if Path(component_path).is_absolute() else Path(os.getcwd())/component_path
        component = read_component(location, environment)

        # Check step existence
        if step_name and step_name not in component.steps:
            raise Exception(f"Step {step_name} is not in {location}")

        # Run it (or them, if step is not specified)
        steps = [step_name] if step_name else component.steps
        for target_step_name in steps:

            # Get the target step
            target_step = component.steps[target_step_name]
            log_title(logger, target_step.name)

            # Merge envs
            env_spec = merge_envs(location, component, target_step, environment)
            env_spec.expand()

            # Run the step
            context = context or component.context or location
            system.run(target_step, env_spec, location, context)

import functools
from pathlib import Path
from typing import List

from nymbus.config.components.component import Component
from nymbus.config.environment import DEFAULT_ENVIRONMENT, DEFAULT_ENVIRONMENT_FILE, DEFAULT_NYMBUS_EXTENSION
from nymbus.config.envspec import EnvSpec
from nymbus.config.readers.reader import merge_dictionaries, read_yml
from nymbus.config.components.step import Step


def read_dicts_merging(context: Path, environment: str = DEFAULT_ENVIRONMENT, optional_env: bool = True) -> dict:
    # Read the default
    default_location = Path(context) / DEFAULT_ENVIRONMENT_FILE
    default = read_yml(default_location)

    # Read the component from the location
    location = Path(context) / f"{environment}{DEFAULT_NYMBUS_EXTENSION}"
    if location.exists() or not optional_env:
        specific = read_yml(location)

        # Merge the dictionaries
        result = merge_dictionaries(default, specific)
    else:
        result = default

    return result


def read_component(context: Path, environment: str = DEFAULT_ENVIRONMENT):
    result = read_dicts_merging(context, environment, optional_env=False)
    return Component(context.name, environment, result)


def _has_env_spec(location: Path) -> bool:
    return (location/DEFAULT_ENVIRONMENT_FILE).exists()


def find_env_spec_locations(location: Path, include_current: bool = False) -> List[Path]:

    # Go up the uppermost env file
    env_specs = []
    while _has_env_spec(location):
        env_specs.insert(0, location)
        location = location.parent

    # Keep the current (i.e. the last one)?
    return env_specs[:-1 if not include_current else len(env_specs)]


def read_upper_env_specs_merging(location: Path, environment: str = DEFAULT_ENVIRONMENT, optional_env: bool = True) -> EnvSpec:

    # Find all upper EnvSpec paths
    env_spec_paths = find_env_spec_locations(location)

    # Read them all
    env_specs = [
        read_dicts_merging(location, environment, optional_env=optional_env)
        for location in env_spec_paths
    ]

    # Merge EnvSpecs
    result = functools.reduce(merge_dictionaries, env_specs)
    return EnvSpec(result)


def merge_envs(location: Path, component: Component, target_step: Step = None, environment: str = DEFAULT_ENVIRONMENT) -> EnvSpec:

    # Read the upper envs, merging them
    env_spec = read_upper_env_specs_merging(location, environment)

    # Reduce them with component and step
    return EnvSpec.from_env(functools.reduce(
        merge_dictionaries,
        [env_spec.env, component.env] + ([target_step.env] if target_step else [])
    ))

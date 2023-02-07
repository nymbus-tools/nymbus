import os
from pathlib import Path

from nymbus.config.readers.combiner import merge_envs, read_component


def test_combiner(data_location: Path):

    # Set an env variable
    redacted = "<redacted>"
    os.environ["DEV_SECRET"] = redacted

    # Read component
    name = "backend"
    component_path = data_location/name
    component = read_component(component_path, "dev")

    # Merge envs
    env_spec = merge_envs(component_path, component, component.steps["deploy"])
    env_spec.expand()
    assert env_spec.env["SECRET"] == redacted
    assert env_spec.env["PROJECT"] == "project-dev"
    assert env_spec.env["STANDARD"] == "low"

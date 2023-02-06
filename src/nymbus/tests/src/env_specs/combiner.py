import os
from pathlib import Path

from nymbus.config.readers.combiner import merge_envs, read_component


def combine(data_location: Path):

    # Set an env variable
    redacted = "<redacted>"
    os.environ["DEV_SECRET"] = redacted

    # Read component and merge envs
    component = read_component(data_location/"backend", "dev")
    env = merge_envs(data_location, component, component.steps["deploy"])

    assert env["SECRET"] == redacted
    assert env["PROJECT"] == "project-dev"
    assert env["STANDARD"] == "high"

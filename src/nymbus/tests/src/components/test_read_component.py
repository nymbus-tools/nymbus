from pathlib import Path

from nymbus.config.readers.combiner import read_component


def test_read_component(data_location: Path):

    # Read component
    name = "backend"
    component = read_component(data_location/name, "dev")
    assert component.name == name

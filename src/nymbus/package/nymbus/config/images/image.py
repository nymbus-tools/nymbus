from nymbus.config.images.bind import Bind


class Image:

    def __init__(self, yml: dict):
        # Pop the config entries
        config = yml.copy()
        self.name = config.pop("name")
        self.volumes = {
            path: Bind(bind)
            for path, bind in config.pop("volumes", {}).items()
        }


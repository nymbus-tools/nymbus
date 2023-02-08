
class Bind:

    def __init__(self, yml: dict):
        # Pop the config entries
        config = yml.copy()
        self.bind = config.pop("bind")
        self.mode = config.pop("mode", "ro")

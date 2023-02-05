from nymbus.config.environment import expand_variable


class EnvSpec:

    def __init__(self, yml: dict):
        # Pop the config entries
        config = yml.copy()
        self.env = {
            name: expand_variable(value)
            for name, value in config.pop("env", {}).items()
        }

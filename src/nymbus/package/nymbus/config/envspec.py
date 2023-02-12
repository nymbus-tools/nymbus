from nymbus.config.environment import expand_variable


class EnvSpec:

    def __init__(self, yml: dict):
        # Pop the config entries
        self.env = yml.get("env", {})

    def expand(self):
        self.env = {name: expand_variable(value) for name, value in self.env.items()}

    @classmethod
    def from_env(cls, env: dict):
        return cls({"env": env})

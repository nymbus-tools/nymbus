class Template:

    def __init__(self, yml: dict):
        # Pop the config entries
        config = yml.copy()
        self.repository = config.pop("repository")
        self.tag = config.pop("tag", "master")

class PluginInterface:
    def perform_action(self, data):
        raise NotImplementedError("Plugins must implement this method")

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        # Dynamically import and instantiate plugins
        # Example: self.plugins.append(SamplePlugin())
        pass

    def run_plugins(self, data):
        for plugin in self.plugins:
            plugin.perform_action(data)

class SamplePlugin(PluginInterface):
    def perform_action(self, data):
        print(f"Plugin action performed on {data}")
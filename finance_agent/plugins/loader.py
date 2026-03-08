import importlib
import pkgutil
import finance_agent.plugins as plugins_pkg


def load_plugins():
    loaded = []
    for module in pkgutil.iter_modules(plugins_pkg.__path__, plugins_pkg.__name__ + "."):
        importlib.import_module(module.name)
        loaded.append(module.name)
    return loaded

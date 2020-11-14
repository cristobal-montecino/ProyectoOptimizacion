import importlib

import src.render as renderModule
import src.Fabrik as fabrikModule
import src.skeletal as skeletalModule

def reload_modules():
    importlib.reload(renderModule)
    importlib.reload(fabrikModule)
    importlib.reload(skeletalModule)
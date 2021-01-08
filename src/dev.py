import importlib

import src.render as renderModule
import src.Fabrik as fabrikModule
import src.skeletal as skeletalModule
import src.direk as direkModule
import src.pinkind as pinkindModule

def reload_modules():
    importlib.reload(renderModule)
    importlib.reload(fabrikModule)
    importlib.reload(skeletalModule)
    importlib.reload(direkModule)
    importlib.reload(pinkindModule)
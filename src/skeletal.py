import copy

import src.render as render
import src.Fabrik as fabrik

class Skeletal:
    def __init__(self):
        self.points = []
        
    def render(self, viewport, **config):
        render.render(viewport, self.points, **config)
        
    def clone(self):
        return copy.deepcopy(self)
    
    def fabrik(self, target, tolerance=10**-14):
        result_skeletal = self.clone()
        result_skeletal.points = fabrik.fabrik(result_skeletal.points, target, tolerance)
        
        return result_skeletal
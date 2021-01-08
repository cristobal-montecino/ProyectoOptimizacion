import copy

import src.render as render
import src.Fabrik as fabrik
import src.direk as direk
import src.pinkind as pinkind

DEFAULT_TOLERANCE = 10**-11

class Skeletal:
    def __init__(self):
        self.points = []
        self.lengths = []
        
    def render(self, viewport, **config):
        render.render(viewport, self.points, **config)
        
    def clone(self):
        return copy.deepcopy(self)
    
    def fabrik(self, target, tolerance=DEFAULT_TOLERANCE):
        result_skeletal = self.clone()
        result_skeletal.points = fabrik.fabrik(result_skeletal.points, target, result_skeletal.lengths, tolerance)
        
        return result_skeletal
    
    def direk(self, target, tolerance=DEFAULT_TOLERANCE, **options):
        result_skeletal = self.clone()
        result_skeletal.points = direk.direk(result_skeletal.points, target, result_skeletal.lengths,
                                             scalar_epsilon=tolerance,
                                             vector3_epsilon=tolerance,
                                             **options)
        
        return result_skeletal
    
    def pinkind(self, target, tolerance=DEFAULT_TOLERANCE):
        result_skeletal = self.clone()
        result_skeletal.points = pinkind.pinkind(result_skeletal.lengths, result_skeletal.points[0], target)
         
        return result_skeletal
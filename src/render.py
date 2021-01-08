import numpy as np
import matplotlib.pyplot as plt

class Viewport(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center = np.array([0.0, 0.0])

DEFAULT_RENDER_CONFIG = {
    'point_size': 0.1,
    'target_color': 'red',
    'point_color': 'blue',
    'figsize': (10, 10),
    'on_click': None,
    'fig,ax': None,
}

def render(viewport, points, target=None, **_config):
    config = dict()
    config.update(DEFAULT_RENDER_CONFIG)
    config.update(_config)
       
    fig_ax = config['fig,ax']
    if fig_ax is None:
        figsize = config['figsize']
        fig, ax = plt.subplots(figsize=figsize)
        is_new = True
    else:
        fig, ax = fig_ax
        ax.cla()
        is_new = False
        
    ax.set(
        xlim = (viewport.center[0] - viewport.width * 0.5, viewport.center[0] + viewport.width * 0.5),
        ylim = (viewport.center[1] - viewport.height * 0.5, viewport.center[1] + viewport.height * 0.5),
        aspect = 1.0
    )
    
    point_size = config['point_size']
    
    point_color = config['point_color']
    point_circles = [plt.Circle(point, point_size, color=point_color) for point in points]

    for circle in point_circles:
        ax.add_artist(circle)

    for i, _ in enumerate(points[1:], 1):
        line = plt.Line2D([points[i-1][0], points[i][0]], [points[i-1][1], points[i][1]])
        ax.add_artist(line)
        
    if target is not None:
        target_color = config['target_color']
        target_circle = plt.Circle(target, point_size, color=target_color)
        ax.add_artist(target_circle)
    
    if is_new:
        on_click = config['on_click']            
        if on_click is not None:
            args = {'fig,ax': (fig, ax), 'viewport': viewport}
            args.update(_config)
            fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, args))
    
        plt.ion()
        plt.show()
'''
To be added:
    Widgets will be implemented with:
        fig.canvas.mpl_connect(event, callback)
'''
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from numpy.typing import NDArray

#TODO: Fufil this bit

class NodeMovement:
    def __init__(self, fig: Figure, positions: NDArray) -> None:
        self.fig = fig
        self.positions = positions
        self.hold = False
        
        self._event_dict = {
            'button_press_event': self._button_press
        }
        
        self.cids = {}
        
    def start(self) -> None:
        for key, func in self._event_dict.items():
            self.cids[key] = self.fig.canvas.mpl_connect(key, func)
            
    def stop(self) -> None:
        for key in self._event_dict:
            self.fig.canvas.mpl_disconnect(self.cids[key])

    def _button_press(self, event) -> None:
        self.hold = True
        
    def _locate_node(self, x, y) -> None:
        pass
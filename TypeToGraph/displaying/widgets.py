'''
To be added:
    Widgets will be implemented with:
        fig.canvas.mpl_connect(event, callback)
'''
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from time import sleep
from typing import Tuple, Optional

#TODO: Fufil this bit

class NodeMovement:
    def __init__(self, fig: Figure, positions: list[Tuple[float, float]]) -> None:
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
        print(f"Button pressed at: ({event.xdata}, {event.ydata})")

        while self.hold:
            if event.xdata is None or event.ydata is None:
                continue
            
            node = self._locate_node(event.xdata, event.ydata)
            if node is not None:

                print(f"Node found at position: {node}")
            
            # Redraw the figure to reflect changes
            self.fig.canvas.draw()
            sleep(0.1)


    def _locate_node(self, x, y) -> Optional[Tuple[float, float]]:
        for node in self.positions:
            # use euclidean distance to find the closest node
            distance = ((node[0] - x) ** 2 + (node[1] - y) ** 2) ** 0.5
            if distance < 6:
                return node
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from typing import Optional, Dict

from .layouts import LayoutEngine, SpringLayoutEngine
from .adapter import BinaryTreeAdapter, DateBasedTreeAdapter, TreeAdapter


'''
I was initally questioning if this needed to be a class but here is an analysis

States:
    current_nodes
    current_positions
    figure
    ax
    _current_anim
    layout_engine (Dependency Injection) <- Biggest argument for a class
    
Encapsulates all of the logic with private methods

Reusability
- Multiple instances of it with a different layout engine

Readability and Maintainability
- Defines actions performed on the object
'''

class GraphDisplayer:
    '''Main displayer class.
    Default Engine: Spring Engine
    '''

    def __init__(self, layout_engine: Optional[LayoutEngine] = None):
        self.layout_engine = layout_engine or SpringLayoutEngine()
        self.adapters: Dict[str, TreeAdapter] = {
            'BinaryTree': BinaryTreeAdapter(),
            'DateBasedNodeTree': DateBasedTreeAdapter(), 
        }

        self.current_nodes = []
        self.current_positions = {}
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
        self._current_animation: Optional[animation.FuncAnimation] = None

    def display(self, tree, tree_type: str | None = None, animate: bool = True):
        '''Display any tree using appropriate adapter'''

        if tree_type is None:
            tree_type = tree.__class__.__name__

        if tree_type not in self.adapters:
            raise ValueError(f"No adapter available for {tree_type}. Available: {list(self.adapters.keys())}")

        adapter = self.adapters[tree_type]
        self.current_nodes = adapter.to_display_nodes(tree)
        
        if not self.current_nodes:
            raise ValueError("No Nodes to display")

        final_positions = self.layout_engine.calculate_positions(self.current_nodes)
        self.current_positions = final_positions

        if animate:
            self._animate_to_layout()
        else:
            self._static_display()

    def _static_display(self):
        """Display without animation"""
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # draw nodes
        x_coords = [self.current_positions[node.id][0] for node in self.current_nodes]
        y_coords = [self.current_positions[node.id][1] for node in self.current_nodes]
        
        self.ax.scatter(x_coords, y_coords, s=300, c='lightblue',
                    edgecolors='black', zorder=3)

        # draw edges
        for node in self.current_nodes:
            if node.parent_id and node.parent_id in self.current_positions:
                x1, y1 = self.current_positions[node.parent_id]
                x2, y2 = self.current_positions[node.id]
                self.ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.6, zorder=1)

        # draw labels
        for node in self.current_nodes:
            x, y = self.current_positions[node.id]
            self.ax.text(x, y, node.label, ha='center', va='center', fontsize=10, zorder=4)

        self._setup_axes()
        plt.show()

    def _animate_to_layout(self):
        '''Animate nodes to final positions'''
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        initial_pos = {node.id: (node.x, node.y) for node in self.current_nodes}
        total_frames = 50

        def animate(frame):
            if self.ax is None:
                raise RuntimeError("Axes object is None during animation")

            self.ax.clear()
            t = frame / (total_frames - 1) if total_frames > 1 else 1
            t_smooth = 3 * t**2 - 2 * t**3  # smooth step

            current_pos = {}
            for node in self.current_nodes:
                start = np.array(initial_pos[node.id])
                end = np.array(self.current_positions[node.id])
                current_pos[node.id] = start + t_smooth * (end - start)

            # nodes
            x_coords = [pos[0] for pos in current_pos.values()]
            y_coords = [pos[1] for pos in current_pos.values()]
            scatter = self.ax.scatter(x_coords, y_coords, s=300, c='lightblue',
                                    edgecolors='black', zorder=3)

            # edges
            lines = []
            for node in self.current_nodes:
                if node.parent_id and node.parent_id in current_pos:
                    x1, y1 = current_pos[node.parent_id]
                    x2, y2 = current_pos[node.id]
                    line, = self.ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.6, zorder=1)
                    lines.append(line)

            # draw labels
            texts = []
            for node in self.current_nodes:
                x, y = current_pos[node.id]
                text = self.ax.text(x, y, node.label, ha='center', va='center', 
                                fontsize=10, zorder=4)
                texts.append(text)

            self._setup_axes()
            self.ax.set_title(f'Animation Frame {frame+1}/{total_frames}')

            return [scatter] + lines + texts

        self._current_animation = animation.FuncAnimation(
            self.fig, animate, frames=total_frames, interval=100, repeat=False, blit=False
        )

        plt.show()

    def _setup_axes(self):
        """Configure axes settings"""
        if isinstance(self.ax, Axes):
            self.ax.set_xlim(0, 1280)
            self.ax.set_ylim(720, 0)
            self.ax.set_aspect('equal')
            self.ax.axis('off')

    def save_animation(self, filename: str, writer: str = 'pillow'):
        """Save the current animation to file"""
        if self._current_animation:
            self._current_animation.save(filename, writer=writer)
        else:
            print("No animation to save")
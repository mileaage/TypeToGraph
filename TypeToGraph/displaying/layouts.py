import networkx as nx
from typing import List, Dict, Tuple, Optional
from abc import abstractmethod, ABC
import math

from models.display import DisplayNode
from constants import *


class LayoutEngine(ABC):
    """Abstract base for layout algorithms"""
    
    @abstractmethod
    def calculate_positions(self, nodes: List[DisplayNode]) -> Dict[str, Tuple[float, float]]:
        """Calculate final positions for nodes"""
        pass


class SpringLayoutEngine(LayoutEngine):
    """NetworkX spring layout implementation with bounds checking"""
    
    def __init__(self, k: float = 1, iterations: int = 50, seed: Optional[int] = None):
        self.k = k
        self.iterations = iterations
        self.seed = seed
    
    def calculate_positions(self, nodes: List[DisplayNode]) -> Dict[str, Tuple[float, float]]:
        if not nodes:
            return {}
            
        # Create NetworkX graph
        G = nx.Graph()
        initial_pos = {}
        
        for node in nodes:
            G.add_node(node.id)
            
            # Normalize initial positions to [-1, 1] range for spring layout
            initial_pos[node.id] = (
                (node.x / SCREEN_X) * 2 - 1,
                (node.y / SCREEN_Y) * 2 - 1
            )
            
            # ^ initially tried [0, SCREEN_X] but it proved to be a little off
            
            # did some more research: the algorithm uses a default scale of 1 (0,0 being the middle so it's -1, 1)
            
            if node.parent_id:
                G.add_edge(node.parent_id, node.id)
        
        # Handle single node case
        if len(nodes) == 1:
            return {nodes[0].id: (SCREEN_X / 2, SCREEN_Y / 2)}
        
        # apply spring layout
        try:
            spring_pos = nx.spring_layout(
                G, pos=initial_pos, k=self.k, 
                iterations=self.iterations, seed=self.seed
            )
        except Exception as e:
            print(f"Spring layout failed: {e}. Using hierarchical fallback.")
            return HierarchicalLayoutEngine().calculate_positions(nodes)
        
        # Scale to screen coordinates with bounds checking
        final_pos = {}
        for node_id, (x, y) in spring_pos.items():
            scaled_x = max(50, min(SCREEN_X - 50, (x + 1) * SCREEN_X / 2))
            scaled_y = max(50, min(SCREEN_Y - 50, (y + 1) * SCREEN_Y / 2))
            final_pos[node_id] = (scaled_x, scaled_y)
        
        return final_pos


class HierarchicalLayoutEngine(LayoutEngine):
    """Simple hierarchical layout that maintains tree structure"""
    
    def calculate_positions(self, nodes: List[DisplayNode]) -> Dict[str, Tuple[float, float]]:
        return {node.id: (node.x, node.y) for node in nodes}


class CircularLayoutEngine(LayoutEngine):
    """Circular layout for better visualization of small trees"""
    
    def __init__(self, radius: float = 200):
        self.radius = radius
    
    def calculate_positions(self, nodes: List[DisplayNode]) -> Dict[str, Tuple[float, float]]:
        if not nodes:
            return {}
        
        if len(nodes) == 1:
            return {nodes[0].id: (SCREEN_X / 2, SCREEN_Y / 2)}
        
        center_x, center_y = SCREEN_X / 2, SCREEN_Y / 2
        final_pos = {}
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = center_x + self.radius * math.cos(angle)
            y = center_y + self.radius * math.sin(angle)
            final_pos[node.id] = (x, y)
        
        return final_pos


class ForceDirectedLayoutEngine(LayoutEngine):
    """Custom force-directed layout with configurable parameters"""
    
    def __init__(self, attraction: float = 0.01, repulsion: float = 1000, 
                damping: float = 0.9, iterations: int = 100):
        self.attraction = attraction
        self.repulsion = repulsion
        self.damping = damping
        self.iterations = iterations
    
    def calculate_positions(self, nodes: List[DisplayNode]) -> Dict[str, Tuple[float, float]]:
        if not nodes:
            return {}
        
        if len(nodes) == 1:
            return {nodes[0].id: (SCREEN_X / 2, SCREEN_Y / 2)}
        
        # Initialize positions and velocities
        positions = {node.id: [float(node.x), float(node.y)] for node in nodes}
        velocities = {node.id: [0.0, 0.0] for node in nodes}
        
        # Build adjacency list
        edges = []
        for node in nodes:
            if node.parent_id:
                edges.append((node.parent_id, node.id))
        
        for _ in range(self.iterations):
            forces = {node.id: [0.0, 0.0] for node in nodes}
            
            # Repulsive forces between all nodes
            for i, node1 in enumerate(nodes):
                for node2 in nodes[i+1:]:
                    dx = positions[node2.id][0] - positions[node1.id][0]
                    dy = positions[node2.id][1] - positions[node1.id][1]
                    distance = math.sqrt(dx*dx + dy*dy) + 0.1  # Avoid division by zero
                    
                    force = self.repulsion / (distance * distance)
                    fx = force * dx / distance
                    fy = force * dy / distance
                    
                    forces[node1.id][0] -= fx
                    forces[node1.id][1] -= fy
                    forces[node2.id][0] += fx
                    forces[node2.id][1] += fy
            
            # Attractive forces along edges
            for parent_id, child_id in edges:
                if parent_id in positions and child_id in positions:
                    dx = positions[child_id][0] - positions[parent_id][0]
                    dy = positions[child_id][1] - positions[parent_id][1]
                    
                    forces[parent_id][0] += self.attraction * dx
                    forces[parent_id][1] += self.attraction * dy
                    forces[child_id][0] -= self.attraction * dx
                    forces[child_id][1] -= self.attraction * dy
            
            # Update positions
            for node in nodes:
                velocities[node.id][0] = self.damping * velocities[node.id][0] + forces[node.id][0]
                velocities[node.id][1] = self.damping * velocities[node.id][1] + forces[node.id][1]
                
                positions[node.id][0] += velocities[node.id][0]
                positions[node.id][1] += velocities[node.id][1]
                
                # Keep within bounds
                positions[node.id][0] = max(50, min(SCREEN_X - 50, positions[node.id][0]))
                positions[node.id][1] = max(50, min(SCREEN_Y - 50, positions[node.id][1]))
        
        return {node_id: (float(pos[0]), float(pos[1])) for node_id, pos in positions.items()}
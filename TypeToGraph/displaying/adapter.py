from typing import Any, List, Dict, Optional, Protocol, runtime_checkable
from models.display import DisplayNode
from constants import *

'''
    Adapter pattern
    
    Use Case: Since we need to modify the structure of the trees to provide a simple interface to work with
    we use adapters to solve this
'''

@runtime_checkable
class TreeAdapter(Protocol):
    """Protocol for converting tree structures to display format"""
    
    def to_display_nodes(self, tree: Any) -> List[DisplayNode]:
        """Tree -> List[DisplayNode]"""
        ...


# Probably won't be used a lot
class BinaryTreeAdapter:
    """Adapter for binary trees with improved parent tracking"""
    
    def to_display_nodes(self, tree) -> List[DisplayNode]:
        nodes = []
        
        try:
            levels = tree.get_display_values()
        except AttributeError:
            raise ValueError("Tree must implement get_display_values() method")
        
        if not levels:
            return nodes
        
        y_positions = self._calculate_y_positions(len(levels))
        node_id_map = {}
        
        for level_idx, level in enumerate(levels):
            if not level:
                continue
                
            x_positions = self._calculate_x_positions(len(level))
            
            for i, node in enumerate(level):
                if node is not None:
                    node_id = f"level_{level_idx}_pos_{i}"
                    parent_id = self._find_parent_id(node, levels, level_idx, node_id_map)
                    
                    display_node = DisplayNode(
                        id=node_id,
                        x=x_positions[i],
                        y=y_positions[level_idx],
                        label=str(getattr(node, 'value', node)),
                        data=node,
                        parent_id=parent_id
                    )
                    
                    nodes.append(display_node)
                    node_id_map[node] = node_id
        
        return nodes
    
    def _calculate_y_positions(self, num_levels: int) -> List[float]:
        if num_levels <= 0:
            return []
        if num_levels == 1:
            return [START_Y + AVAILABLE_SPACE / 2]
        return [START_Y + (i / (num_levels - 1)) * AVAILABLE_SPACE for i in range(num_levels)]
    
    def _calculate_x_positions(self, num_nodes: int) -> List[float]:
        if num_nodes <= 0:
            return []
        return [(i + 0.5) * (SCREEN_X / num_nodes) for i in range(num_nodes)]
    
    def _find_parent_id(self, node, levels, level_idx, node_id_map):
        if level_idx == 0:
            return None
        
        # serach previous level
        for prev_node in levels[level_idx - 1]:
            if prev_node is not None:
                if (hasattr(prev_node, 'left') and prev_node.left == node) or \
                    (hasattr(prev_node, 'right') and prev_node.right == node):
                    return node_id_map.get(prev_node)
        return None


class DateBasedTreeAdapter:
    """Adapter for date-based note trees with improved parent tracking"""
    
    def __init__(self):
        self.node_id_map = {}  # track node ids
    
    def to_display_nodes(self, tree) -> List[DisplayNode]:
        nodes = []
        self.node_id_map = {} # reset our nodes
        
        try:
            levels = tree.get_display_values()
        except AttributeError:
            raise ValueError("Tree must implement get_display_values() method")
        
        if not levels:
            return nodes
        
        y_positions = self._calculate_y_positions(len(levels))
        
        for level_idx, level in enumerate(levels):
            if not level:
                continue
                
            x_positions = self._calculate_x_positions(len(level))
            
            for i, item_dict in enumerate(level):
                if self._has_content(item_dict):
                    node_id = f"date_level_{level_idx}_pos_{i}"
                    parent_id = self._find_parent_id(item_dict, level_idx)
                    
                    display_node = DisplayNode(
                        id=node_id,
                        x=x_positions[i],
                        y=y_positions[level_idx],
                        label=self._extract_label(item_dict),
                        data=item_dict,
                        parent_id=parent_id
                    )
                    
                    nodes.append(display_node)
                    # Store mapping for parent lookup
                    self.node_id_map[id(item_dict)] = node_id
        
        return nodes
    
    def _has_content(self, item_dict: Dict) -> bool:
        if not isinstance(item_dict, dict):
            return False
        return item_dict.get('value') is not None or item_dict.get('note') is not None
    
    def _extract_label(self, item_dict: Dict) -> str:
        return str(item_dict.get('value') or item_dict.get('note', 'Empty'))
    
    def _find_parent_id(self, item_dict: Dict, level_idx: int) -> Optional[str]:
        if level_idx == 0:
            return None
        parent = item_dict.get('parent')
        if parent:
            return self.node_id_map.get(id(parent))
        return None
    
    def _calculate_y_positions(self, num_levels: int) -> List[float]:
        if num_levels <= 0:
            return []
        if num_levels == 1:
            return [START_Y + AVAILABLE_SPACE / 2]
        return [START_Y + (i / (num_levels - 1)) * AVAILABLE_SPACE for i in range(num_levels)]
    
    def _calculate_x_positions(self, num_nodes: int) -> List[float]:
        if num_nodes <= 0:
            return []
        return [(i + 0.5) * (SCREEN_X / num_nodes) for i in range(num_nodes)]
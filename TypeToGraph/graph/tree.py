from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Union, TypeAlias, Optional, List, Set, Dict
from datetime import datetime
from enum import Enum
import uuid


NodeValue: TypeAlias = Union[int, float, str]

@dataclass
class TreeNode:
    value: Any

@dataclass()
class BSTNode(TreeNode):
    left: Optional['BSTNode'] = None
    right: Optional['BSTNode'] = None

@dataclass
class NNode:
    value: Any
    children: List[Optional['NNode']] = field(default_factory=list)

class BaseTree(ABC):
    @abstractmethod
    def get_display_values(self) -> List[List[TreeNode]]:
        pass
    
class NoteType(Enum):
    TEXT = "text"
    TASK = "task" 
    IDEA = "idea"
    REFERENCE = "reference"

@dataclass
class Note:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    note_type: NoteType = NoteType.TEXT
    tags: Set[str] = field(default_factory=set)
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.title and self.content:
            # auto gen name
            self.title = self.content.split('\n')[0][:50]

    def add_note_as_child(self, note: 'Note'):
        self.children_ids.append(note.id)
        note.parent_id = self.id


class DateBasedNoteTree(BaseTree):
    """
    Organized by date
    """
    
    def __init__(self):
        self.notes: Dict[str, Note] = {}
        self.date_hierarchy: Dict[str, Dict[str, List[str]]] = {}
        # Structure: {year: {month: [note_ids]}}
    
    def add_note(self, title: str, content: str = "") -> Note:
        note = Note(title=title, content=content)
        self.notes[note.id] = note
        
        # Organize by date
        year = str(note.created_at.year)
        month = f"{note.created_at.month:02d}"
        
        if year not in self.date_hierarchy:
            self.date_hierarchy[year] = {}
        if month not in self.date_hierarchy[year]:
            self.date_hierarchy[year][month] = []
        
        self.date_hierarchy[year][month].append(note.id)
        return note
    
    def get_display_values(self) -> List[List[Any]]:
        """Convert to tree levels: Years -> Months -> Notes"""
        if not self.date_hierarchy:
            return []
        
        levels = []
        
        # Level 1: Years
        years = sorted(self.date_hierarchy.keys())
        year_nodes = [{"type": "year", "value": year} for year in years]
        levels.append(year_nodes)
        
        # Create lookup for year nodes by value
        year_lookup = {year: year_nodes[i] for i, year in enumerate(years)}
        
        # Level 2: Months
        month_nodes = []
        month_lookup = {}
        for year in years:
            months = sorted(self.date_hierarchy[year].keys())
            for month in months:
                month_node = {
                    "type": "month", 
                    "value": f"{year}-{month}",
                    "parent": year_lookup[year]  # refer to year dict
                }
                month_nodes.append(month_node)
                month_lookup[f"{year}-{month}"] = month_node
        levels.append(month_nodes)
        
        # Level 3: Notes
        note_nodes = []
        for year in years:
            for month in sorted(self.date_hierarchy[year].keys()):
                month_key = f"{year}-{month}"
                for note_id in self.date_hierarchy[year][month]:
                    note = self.notes[note_id]
                    note_nodes.append({
                        "type": "note",
                        "value": note.title or note.content[:20],
                        "note": note,
                        "parent": month_lookup[month_key]  # Reference to actual month dict
                    })
        levels.append(note_nodes)
        
        return levels


class BinaryTree(BaseTree):
    def __init__(self, value: NodeValue):
        """Initialize a binary tree with a root node."""
        if not isinstance(value, NodeValue):
            raise ValueError("Value must be an int, float, or str.")
        
        self.root = BSTNode(value)
        
    
    def insert(self, value: Any) -> None:
        '''Public Insert Method'''
        self.root = self._insert_recursive(self.root, value)
    
    def get_display_values(self) -> List[List[TreeNode]]:
        """
        Level order traversal that maintains positional structure with None placeholders.
        This is crucial for proper binary tree visualization.
        """
        if self.root is None:
            return []
        
        result = []
        current_level = [self.root]
        
        while current_level and any(node is not None for node in current_level):
            result.append(current_level[:])  # add current level
            next_level = []
            
            for node in current_level:
                if node is not None:
                    next_level.append(node.left)   # Add left child (or None)
                    next_level.append(node.right)  # Add right child (or None)
                else:
                    next_level.append(None)  # Add two None placeholders for missing node
                    next_level.append(None)
            
            current_level = next_level
        
        return result
    
    def _insert_recursive(self, root: Optional[BSTNode], value: Any):
        """Insert a value into the binary tree following binary search tree rules."""
        if root is None:
            return BSTNode(value)
        
        if root.value == value:
            return root
        
        if root.value < value:
            root.right = self._insert_recursive(root.right, value)
        else:
            root.left = self._insert_recursive(root.left, value)
        
        return root
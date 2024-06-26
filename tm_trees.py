"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring. DONE
        # 2. Set this tree as the parent for each of its subtrees. DONE
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False
        # task 1 initialization 
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if self._name is None:
            self._subtrees = []
            self._parent_tree = None
            self.data_size = 0
        elif not subtrees:
            self.data_size = data_size
        else:
            self.data_size = sum(subtree.data_size for subtree in self._subtrees)
        for subtreei in range(len(self._subtrees)):
            self._subtrees[subtreei]._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        x, y, wd, h = rect
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif wd <= h:
            self.rect = rect
            to_use = y
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_h = math.floor(percent * h)
                else:
                    new_h = h + y - to_use
                self._subtrees[i].update_rectangles((
                    x, to_use, wd, new_h))
                to_use += new_h
        else:
            self.rect = rect
            to_use = x
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_wd = math.floor(percent * wd)
                else:
                    new_wd = wd + x - to_use
                self._subtrees[i].update_rectangles((
                    to_use, y, new_wd, h))
                to_use += new_wd

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        rects = []
        if self.data_size == 0 or self.is_empty():
            return []
        elif not self._expanded or self._subtrees == []:
            return [(self.rect, self._colour)]
        else:
            for x in self._subtrees:
                rects = rects + TMTree.get_rectangles(x)
            return rects

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        to_check = self._subtrees
        if not self.is_inside_rec(self.rect, pos):
            return None
        elif self._subtrees and self._expanded:  # change made here to check if the desired rectanges are shown or the file is just being shown
            for subtree in to_check:
                if subtree.get_tree_at_position(pos):
                    return subtree.get_tree_at_position(pos)
        return self

    def is_inside_rec(self, rect: Tuple, pos: Tuple[int, int]) -> bool:
        """
        given a rectange rect in a coordinate base and an (x,y) format coordinate
        pos, return True if the pos is located with on on the edge of the rectangle.
        """
        if pos[0] >= rect[0] and pos[1] >= rect[1]:
            if (rect[0] + rect[2]) >= pos[0] and (rect[1] + rect[3]) >= pos[1]:
                return True
        return False

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if not self._subtrees:
            return self.data_size
        else:
            size = sum(subtree.data_size for subtree in self._subtrees)
            self.data_size = size
            if self._parent_tree:
                self._parent_tree.update_data_sizes
            return size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if not self._subtrees and destination._subtrees:
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.data_size -= self.data_size
            self._parent_tree = destination
            destination._subtrees.append(self)
        
            
    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees:
            if factor > 0:
                to_add = math.ceil(self.data_size * factor)
                self.data_size += to_add
            else:
                to_add = math.floor(self.data_size * factor)
                if self.data_size == 0:
                    pass
                elif self.data_size + to_add >= 1:
                    self.data_size +=  to_add
                else:
                    self.data_size = 1

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        if self._parent_tree:
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.data_size -= self.data_size
            if not self._parent_tree._subtrees:
                self._parent_tree._expanded = False
            return True
        return False

    def expand(self) -> None:
        """
        self is the selected rectangle,if the tree is not already expanded,
        pressing e will expand the tree . If the tree does not have children,
        then the tree is left as it is.
        """
        if self._parent_tree is not None: 
            self._parent_tree.expand() 
        if self._subtrees != []:
            self._expanded = True
    
    def expand_all(self) -> None:
        """
        self is the selected rectangle,if the tree is not already expanded,
        pressing a will expand the tree and all of it's children. 
        If the tree does not have children,
        then the tree is left as it is.
        """
        if self._subtrees:
            self.expand()
            for subtree in self._subtrees:
                subtree.expand_all()

    def collapse(self) -> None:
        """
        self is the selected rectangle,if the tree is not already collapsed,
        pressing c will collapse the tree. 
        If the tree does not have children,
        then the tree is left as it is.
        """
        
        if self._parent_tree:
            self._parent_tree._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree._expanded = False
                for tree in subtree._subtrees:
                    tree.collapse()
        


    def collapse_all(self) -> None:
        """
        self is the selected rectangle,if the tree is not already expanded,
        pressing x will collapse the tree and all of it's acestors. 
        If the tree does not have parents,
        then the tree is left as it is.
        """
        self.collapse()
        if self._parent_tree:
            self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        return self._parent_tree.get_path_string() + \
            self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.
        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TODO: (Task 1) Implement the initializer DONE
        # setting variables to be used in init
        name = os.path.basename(path)
        file_size = os.path.getsize(path)
        if os.path.isdir(path):  # recursive case
            children = []
            for child in os.listdir(path):
                child_path = os.path.join(path, child)
                child_node = FileSystemTree(child_path)
                child_node._parent_tree = self
                children.append(child_node)
            TMTree.__init__(self, name, children, file_size)
        else:  # is not a directory, base case
            TMTree.__init__(self, name, [], file_size)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'

if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict', '_get_data'],
        'max-args': 8
    })

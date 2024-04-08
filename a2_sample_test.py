"""
Assignment 2 - Sample Tests

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains sample tests for Assignment 2, Tasks 1 and 2.
The tests use the provided example-directory, so make sure you have downloaded
and extracted it into the same place as this test file.
This test suite is very small. You should plan to add to it significantly to
thoroughly test your code.

IMPORTANT NOTES:
    - If using PyCharm, go into your Settings window, and go to
      Editor -> General.
      Make sure the "Ensure line feed at file end on Save" is NOT checked.
      Then, make sure none of the example files have a blank line at the end.
      (If they do, the data size will be off.)

    - os.listdir behaves differently on different
      operating systems.  These tests expect the outcomes that one gets
      when running on the *Teaching Lab machines*.
      Please run all of your tests there - otherwise,
      you might get inaccurate test failures!

    - Depending on your operating system or other system settings, you
      may end up with other files in your example-directory that will cause
      inaccurate test failures. That will not happen on the Teachin Lab
      machines.  This is a second reason why you should run this test module
      there.
"""
import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.
EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


def test_file_system_tree_from_directory() -> None:
    """Test creating a FileSystemTree from a directory with files and subdirectories."""
    # Initialize FileSystemTree from the example path
    tree = FileSystemTree(EXAMPLE_PATH)

    # Assert tree attributes
    assert tree._name == 'workshop'  # Updated assertion



def test_file_system_tree_from_file() -> None:
    """Test creating a FileSystemTree from a single file."""
    # Create a test file
    with open('test_file.txt', 'w') as f:
        f.write('Test file content')

    # Initialize FileSystemTree from the test file
    tree = FileSystemTree('test_file.txt')

    # Assert tree attributes
    assert tree._name == 'test_file.txt'
    assert tree.data_size == os.path.getsize('test_file.txt')

    # Remove the test file
    os.remove('test_file.txt')


def test_single_file() -> None:
    """Test a tree with a single file.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert tree._name == 'draft.pptx'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)

###### HERE IDK IF THIS IS BUGGED OR NOT CHECK #####

def test_example_data() -> None:
    """Test the root of the tree at the 'workshop' folder in the example data
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == 'workshop'
    assert tree._parent_tree is None
    assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        assert subtree._parent_tree is tree


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_single_file_rectangles(x, y, width, height) -> None:
    """Test that the correct rectangle is produced for a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    tree.update_rectangles((x, y, width, height))
    rects = tree.get_rectangles()

    # This should be just a single rectangle and colour returned.
    assert len(rects) == 1
    rect, colour = rects[0]
    assert rect == (x, y, width, height)
    assert is_valid_colour(colour)


# def test_example_data_rectangles() -> None:
#     """This test sorts the subtrees, because different operating systems have
#     different behaviours with os.listdir.
#
#     You should *NOT* do any sorting in your own code
#     """
#     tree = FileSystemTree(EXAMPLE_PATH)
#     _sort_subtrees(tree)
#
#     tree.update_rectangles((0, 0, 200, 100))
#     rects = tree.get_rectangles()
#
#     # IMPORTANT: This test should pass when you have completed Task 2, but
#     # will fail once you have completed Task 5.
#     # You should edit it as you make progress through the tasks,
#     # and add further tests for the later task functionality.
#     assert len(rects) == 6
#
#     # UPDATED:
#     # Here, we illustrate the correct order of the returned rectangles.
#     # Note that this corresponds to the folder contents always being
#     # sorted in alphabetical order. This is enforced in these sample tests
#     # only so that you can run them on your own computer, rather than on
#     # the Teaching Labs.
#     actual_rects = [r[0] for r in rects]
#     expected_rects = [(0, 0, 94, 2), (0, 2, 94, 28), (0, 30, 94, 70),
#                       (94, 0, 76, 100), (170, 0, 30, 72), (170, 72, 30, 28)]
#
#     assert len(actual_rects) == len(expected_rects)
#     for i in range(len(actual_rects)):
#         assert expected_rects[i] == actual_rects[i]


######################## TASK 2 TESTS ########################

def test_update_rectangles_single_subtree() -> None:
    """Test update_rectangles with a single subtree."""
    subtree1 = TMTree('B', [], data_size=30)
    tree = TMTree('A', [subtree1], data_size=30)
    tree.update_rectangles((0, 0, 100, 100))


def test_update_rectangles_multiple_subtrees() -> None:
    """Test update_rectangles with multiple subtrees."""
    subtree1 = TMTree('B', [], data_size=30)
    subtree2 = TMTree('C', [], data_size=70)
    tree = TMTree('A', [subtree1, subtree2], data_size=100)
    tree.update_rectangles((0, 0, 200, 100))
    assert tree.rect == (0, 0, 200, 100)
    assert subtree1.rect == (0, 0, 60, 100)
    assert subtree2.rect == (60, 0, 140, 100)


def test_empty_directory() -> None:
    """Test creating a FileSystemTree from an empty directory."""
    # Create an empty directory
    os.makedirs('empty_directory', exist_ok=True)

    # Initialize FileSystemTree with the empty directory
    empty_tree = FileSystemTree('empty_directory')

    # Assert tree attributes for an empty directory
    assert empty_tree._name == 'empty_directory', "Expected the tree name to match the empty directory's name"
    assert empty_tree.data_size == 0, "Expected data size to be 0 for an empty directory"
    assert len(empty_tree._subtrees) == 0, "Expected no subtrees for an empty directory"

    # Clean up: remove the empty directory
    os.rmdir('empty_directory')


def test_extreme_file_sizes() -> None:
    """Test FileSystemTree with very small (0 bytes) and very large file sizes."""
    # Create a very small file (0 bytes)
    with open('zero_byte_file.txt', 'w') as f:
        pass  # Do not write anything to the file

    # Create a very large file
    large_file_name = 'large_file.txt'
    with open(large_file_name, 'wb') as f:
        f.seek(10**9 - 1)  # Seek to 1GB minus 1 byte
        f.write(b'\0')  # Write a single zero byte at this position

    # Initialize FileSystemTrees for each file
    small_tree = FileSystemTree('zero_byte_file.txt')
    large_tree = FileSystemTree(large_file_name)

    # Assert that the data sizes are as expected
    assert small_tree.data_size == 0, "Expected 0 bytes for the very small file"
    assert large_tree.data_size == 10**9, "Expected 1GB for the very large file"

    # Clean up: remove the test files
    os.remove('zero_byte_file.txt')
    os.remove(large_file_name)


######################## TASK 4 TESTS ########################

def test_change_size_negative_factor() -> None:
    """Test change_size with a negative factor."""
    tree = TMTree('root', [], data_size=100)
    tree.change_size(-0.5)
    assert tree.data_size == 50


def test_change_size_zero_factor() -> None:
    """Test change_size with a factor of zero."""
    tree = TMTree('root', [], data_size=100)
    tree.change_size(0)
    assert tree.data_size == 100


def test_change_size_large_factor() -> None:
    """Test change_size with a large factor."""
    tree = TMTree('root', [], data_size=100)
    tree.change_size(10)
    assert tree.data_size == 1100


def test_change_size_fractional_factor() -> None:
    """Test change_size with a fractional factor."""
    tree = TMTree('root', [], data_size=100)
    tree.change_size(0.25)
    assert tree.data_size == 125


def test_change_size_zero_data_size() -> None:
    """Test change_size on a tree with a data size of zero."""
    tree = TMTree('root', [], data_size=0)
    tree.change_size(2)
    assert tree.data_size == 0  # Should remain unchanged


def test_update_data_sizes_single_node() -> None:
    """Test update_data_sizes on a tree with a single node."""
    tree = TMTree('A', [], data_size=100)
    assert tree.update_data_sizes() == 100


def test_update_data_sizes_multiple_nodes() -> None:
    """Test update_data_sizes on a tree with multiple nodes."""
    subtree1 = TMTree('B', [], data_size=30)
    subtree2 = TMTree('C', [], data_size=70)
    tree = TMTree('A', [subtree1, subtree2], data_size=100)
    assert tree.update_data_sizes() == 100


def test_update_data_sizes_uneven_data_sizes() -> None:
    """Test update_data_sizes on a tree with uneven data sizes."""
    subtree1 = TMTree('B', [], data_size=30)
    subtree2 = TMTree('C', [], data_size=70)
    tree = TMTree('A', [subtree1, subtree2], data_size=100)
    assert tree.update_data_sizes() == 100


def test_update_data_sizes_empty_tree() -> None:
    """Test update_data_sizes on an empty tree."""
    tree = TMTree('root', [])
    assert tree.update_data_sizes() == 0


def test_update_data_sizes_negative_data_size() -> None:
    """Test update_data_sizes on a tree with a negative data size."""
    tree = TMTree('root', [], data_size=-50)
    assert tree.update_data_sizes() == -50


# insert move test case here

def test_move_leaf_to_internal_node():
    # Create a tree structure
    root = TMTree('Root', [
        TMTree('Subtree1', [
            TMTree('Leaf1', []),
            TMTree('Leaf2', [])
        ]),
        TMTree('Subtree2', [
            TMTree('Subsubtree1', [])
        ])
    ])

    # Select a leaf node
    selected_leaf = root._subtrees[0]._subtrees[0]

    # Hover over an internal node
    hovered_internal = root._subtrees[1]

    # Move the selected leaf to be a subtree of the hovered internal node
    selected_leaf.move(hovered_internal)

    # Verify that the selected leaf is now a subtree of the hovered internal node
    assert selected_leaf._parent_tree is hovered_internal
    assert selected_leaf in hovered_internal._subtrees

    # Verify that the selected leaf is removed from its original parent's subtrees
    assert selected_leaf not in root._subtrees[0]._subtrees


# insert delete self test case here

def test_delete_self() -> None:
    """Test the delete_self method."""
    # Create a parent node
    parent = TMTree('Parent', [], data_size=100)

    # Create a child node
    child = TMTree('Child', [], data_size=50)

    # Add the child node to the parent
    parent._subtrees.append(child)
    child._parent_tree = parent

    # Call delete_self on the child node
    result = child.delete_self()

    # Assert that the child node is no longer present in the parent's subtree list
    assert child not in parent._subtrees

    # Assert that the method returns True, indicating successful deletion
    assert result is True


def test_delete_self_with_parent_tree() -> None:
    """Test delete_self when the node has a parent tree."""
    # Create a parent tree
    parent_tree = TMTree('Parent', [])

    # Create a node with the parent tree
    node = TMTree('Node', [])
    node._parent_tree = parent_tree

    # Add the node to the parent tree's list of subtrees
    parent_tree._subtrees.append(node)

    # Call delete_self and check if it returns True
    assert node.delete_self(), "Expected delete_self to return True"

    # Check if the node is removed from the parent tree's list of subtrees
    assert node not in parent_tree._subtrees, "Expected node to be removed from parent tree"


######################## TASK 5 TESTS ########################


def test_expand_leaf_node() -> None:
    """Test expanding a leaf node."""
    # Create a leaf node without subtrees
    leaf = TMTree('Leaf', [])
    # Ensure that the tree is not expanded initially
    assert not leaf._expanded
    # Call the expand method
    leaf.expand()
    # Ensure that the tree remains unexpanded after calling the method
    assert not leaf._expanded
    # Ensure that the expand_all method does not expand any subtrees
    leaf.expand_all()
    # Ensure that the tree remains unexpanded after calling the method
    assert not leaf._expanded


def test_collapse_all_single_node_tree():
    """Test edge case of collapsing all nodes in a single-node tree."""
    # Create a tree with a single node
    single_node_tree = TMTree('Root', [])

    # Attempt to collapse all nodes in the single-node tree
    single_node_tree.collapse_all()

    # Assert that the single-node tree remains unchanged
    assert not single_node_tree.is_empty()
    assert single_node_tree._expanded is False


def test_expand_all_leaf_node():
    """Test expanding all nodes starting from a leaf node."""
    # Create a leaf node with no children
    leaf = TMTree('Leaf', [])

    # Expand all nodes starting from the leaf node
    leaf.expand_all()

    # Assert that the leaf node is still not expanded
    assert not leaf._expanded


def test_collapse_single_node_tree():
    """Test edge case of collapsing a single-node tree."""
    # Create a tree with a single node
    single_node_tree = TMTree('Root', [])

    # Attempt to collapse the single-node tree
    single_node_tree.collapse()

    # Assert that the single-node tree remains unchanged
    assert not single_node_tree.is_empty()
    assert single_node_tree._expanded is False


def test_collapse_leaf_node():
    """Test collapsing a leaf node."""
    # Create a leaf node with no children
    leaf = TMTree('Leaf', [])

    # Collapse the leaf node
    leaf.collapse()

    # Assert that the leaf node is still not collapsed
    assert not leaf._expanded


def test_collapse_all_leaf_node():
    """Test collapsing all nodes starting from a leaf node."""
    # Create a leaf node with no children
    leaf = TMTree('Leaf', [])

    # Collapse all nodes starting from the leaf node
    leaf.collapse_all()

    # Assert that the leaf node is still not collapsed
    assert not leaf._expanded


######################## TASK 6 TESTS ########################


##############################################################################
# Helpers
##############################################################################


def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)


######################## RANDOMS #####################

def test_special_character_names() -> None:
    """Test FileSystemTree with file and directory names containing special characters and spaces."""
    special_dir = 'special_dir !@#$'
    special_file = 'special_file @$%.txt'
    os.makedirs(special_dir, exist_ok=True)
    with open(os.path.join(special_dir, special_file), 'w') as f:
        f.write('This is a test file with a special character in its name.')

    tree = FileSystemTree(special_dir)

    assert tree._name == special_dir, "Directory name with special characters should be handled correctly"
    assert tree._subtrees[0]._name == special_file, "File name with special characters should be handled correctly"
    
    # Clean up
    os.remove(os.path.join(special_dir, special_file))
    os.rmdir(special_dir)


def test_large_file_structure() -> None:
    """Test FileSystemTree with a large number of files and directories."""
    base_dir = 'large_structure_test'
    os.makedirs(base_dir, exist_ok=True)
    num_files = 1000  # Adjust based on system capabilities

    for i in range(num_files):
        with open(os.path.join(base_dir, f'file_{i}.txt'), 'w') as f:
            f.write(f'This is file number {i}')

    tree = FileSystemTree(base_dir)

    assert len(tree._subtrees) == num_files, f"Expected {num_files} files in the directory"
    
    # Clean up
    for i in range(num_files):
        os.remove(os.path.join(base_dir, f'file_{i}.txt'))
    os.rmdir(base_dir)


import stat

def test_file_permissions() -> None:
    """Test FileSystemTree with files that have restricted permissions."""
    restricted_file = 'restricted_file.txt'
    with open(restricted_file, 'w') as f:
        f.write('This file has restricted permissions.')
    os.chmod(restricted_file, stat.S_IREAD)  # Set file to read-only

    try:
        tree = FileSystemTree(restricted_file)
        assert tree.data_size > 0, "Expected to read file size even with restricted permissions"
    finally:
        os.chmod(restricted_file, stat.S_IWRITE)  # Restore write permission for cleanup
        os.remove(restricted_file)


def test_hidden_files() -> None:
    """Test FileSystemTree with hidden files and directories."""
    os.makedirs('.hidden_dir', exist_ok=True)
    with open('.hidden_dir/.hidden_file.txt', 'w') as f:
        f.write('This is a hidden file.')

    tree = FileSystemTree('.hidden_dir')

    assert tree._name.startswith('.'), "Expected a hidden directory"
    assert any(subtree._name.startswith('.') for subtree in tree._subtrees), "Expected a hidden file in the directory"
    
    # Clean up
    os.remove('.hidden_dir/.hidden_file.txt')
    os.rmdir('.hidden_dir')


def test_empty_file() -> None:
    """Test creating a FileSystemTree with an empty file."""
    file_name = 'empty_file.txt'
    with open(file_name, 'w') as f:
        pass  # Create an empty file

    tree = FileSystemTree(file_name)
    assert tree.data_size == 0, "Expected data size to be 0 for an empty file"
    assert tree._name == file_name, "Expected tree name to match the empty file's name"

    # Cleanup
    os.remove(file_name)


def test_directory_with_only_empty_files() -> None:
    """Test a directory containing only empty files."""
    os.makedirs('empty_files_dir', exist_ok=True)
    num_empty_files = 5
    for i in range(num_empty_files):
        open(f'empty_files_dir/empty_file_{i}.txt', 'w').close()

    tree = FileSystemTree('empty_files_dir')
    assert tree.data_size == 0, "Expected data size to be 0 for a directory with only empty files"
    assert len(tree._subtrees) == num_empty_files, f"Expected {num_empty_files} subtrees for the empty files"

    # Cleanup
    for i in range(num_empty_files):
        os.remove(f'empty_files_dir/empty_file_{i}.txt')
    os.rmdir('empty_files_dir')


def test_expand_single_subtree() -> None:
    """Test expanding a single subtree."""
    subtree = TMTree('Subtree', [], data_size=50)
    tree = TMTree('Root', [subtree], data_size=50)

    # Initially, the tree is not expanded
    assert not tree._expanded

    # Expand the tree
    tree.expand()

    # Check if the tree is now expanded
    assert tree._expanded, "Expected the tree to be expanded"


def test_collapse_tree_with_multiple_levels() -> None:
    """Test collapsing a tree that has multiple levels of subtrees."""
    leaf = TMTree('Leaf', [], data_size=10)
    subtree = TMTree('Subtree', [leaf], data_size=10)
    root = TMTree('Root', [subtree], data_size=10)

    # Manually expand all nodes
    root._expanded = True
    subtree._expanded = True
    leaf._expanded = True  # Leaf nodes should not be expandable, but added for test completeness

    # Collapse from the root
    root.collapse_all()

    # Verify that all nodes are collapsed
    assert not root._expanded
    assert not subtree._expanded
    assert not leaf._expanded, "Leaf nodes should remain unexpanded"


def test_change_size_of_leaf_and_update_ancestors() -> None:
    """Test changing the size of a leaf node and updating ancestor sizes accordingly."""
    # Creating a leaf node and its ancestors
    leaf = TMTree('Leaf', [], data_size=10)
    subtree = TMTree('Subtree', [leaf], data_size=10)  # Initially, the subtree's size matches the leaf
    root = TMTree('Root', [subtree], data_size=10)  # The root initially has the same size for simplicity

    # Increase the size of the leaf and propagate the change up
    leaf.change_size(0.5)  # Increase leaf size by 50%
    subtree.update_data_sizes()  # Assuming this updates the subtree's size based on its children
    root.update_data_sizes()  # Update the root size based on its subtrees

    # Verify the leaf's new size
    expected_leaf_size = 15  # Original size (10) increased by 50%
    assert leaf.data_size == expected_leaf_size, f"Expected the leaf's size to be updated to {expected_leaf_size}"

    # Verify the updated sizes of the ancestors
    expected_subtree_size = 15  # The subtree size should now match the new leaf size
    assert subtree.data_size == expected_subtree_size, f"Expected the subtree's size to be updated to {expected_subtree_size}"

    expected_root_size = 15  # The root size should also be updated to reflect the leaf's new size
    assert root.data_size == expected_root_size, f"Expected the root's size to be updated to {expected_root_size}"




if __name__ == '__main__':
    import pytest

    pytest.main(['a2_sample_test.py'])

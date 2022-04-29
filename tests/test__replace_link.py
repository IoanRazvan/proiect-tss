from copy import deepcopy
import unittest
from parameterized import parameterized

from avl.avl import AVLNode, AVLTree

# old_node None
# odl_node not None
# old_node without parent
# old_node left child of it's parent
# old_node right child of it's parent
# new_node None
# new_node not None
class TestReplaceLink(unittest.TestCase):
    @parameterized.expand([
        (None, None),
        (None, AVLNode(2))
    ])
    def test_replace_link_old_node_null(self, old_node, new_node):
        with self.assertRaises(AttributeError):
            AVLTree._replace_link(old_node, new_node)
    
    @parameterized.expand([
        (AVLNode(1, parent=None), None),
        (AVLNode(1, parent=None), AVLNode(2)),
    ])
    def test_replace_link_old_node_parent_null(self, old_node, new_node):
        try:
            AVLTree._replace_link(old_node, new_node)
        except Exception:
            self.fail("Should not raise any excpetions")
    
    @parameterized.expand([
        (None,),
        (AVLNode(2),)
    ])
    def test_replace_link_old_node_right_child_of_parent(self, new_node):
        old_node_parent = AVLNode(0)
        old_node_parent.right = AVLNode(1, parent=old_node_parent)
        AVLTree._replace_link(old_node_parent.right, new_node)
        self.assertEqual(old_node_parent.right, new_node, "Should change old_node_parent.right to equal new_node")
    
    @parameterized.expand([
        (None,),
        (AVLNode(-2),)
    ])
    def test_replace_link_old_node_left_child_of_parent(self, new_node):
        old_node_parent = AVLNode(0)
        old_node_parent.left = AVLNode(-1, parent=old_node_parent)
        AVLTree._replace_link(old_node_parent.left, new_node)
        self.assertEqual(old_node_parent.left, new_node, "Should change old_node_parent.left to equal new_node")
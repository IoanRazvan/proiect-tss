import unittest

from avl import AVLTree, AVLNode

# None
# Not None


class TestHeight(unittest.TestCase):
    def test_height_with_null_node(self):
        node = None
        self.assertEqual(AVLTree._height(node), 0, "Should equal 0")

    def test_height_with_non_null_node(self):
        node = AVLNode(1, 1)
        self.assertEqual(AVLTree._height(node), node.height,
                         "Should equal height of node")

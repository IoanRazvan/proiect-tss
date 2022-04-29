import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from avl import AVLTree, AVLNode
from tests.util import SHOULD_HAVE_HEIGHT

PARAMETERIZATION_1 = [
    (2, 1, 3, SHOULD_HAVE_HEIGHT.format(3)),
    (2, 2, 3, SHOULD_HAVE_HEIGHT.format(3)),
    (1, 2, 3, SHOULD_HAVE_HEIGHT.format(3)),
]

# None
# leaf
# one child
# right.height > left.height
# right.height == left.height
# right.height < left.height


class TestAdjustHeightFunctional(unittest.TestCase):
    def setUp(self) -> None:
        self.node = AVLNode(1)
        return super().setUp()

    def test_adjust_height_with_null_node(self):
        node = None
        AVLTree._adjust_height(node)
        self.assertIsNone(node, "Should leave node unchanged")

    def test_adjust_height_with_leaf_node(self):
        AVLTree._adjust_height(self.node)
        self.assertEqual(self.node.height, 1, SHOULD_HAVE_HEIGHT.format(1))

    def test_adjust_height_with_single_child_node(self):
        right_child = AVLNode(2)
        self.node.right = right_child
        AVLTree._adjust_height(self.node)
        self.assertEqual(self.node.height, 2, SHOULD_HAVE_HEIGHT.format(2))

    @parameterized.expand(PARAMETERIZATION_1)
    def test_adjust_height_with_two_children_node(self, right_height, left_height, expected, msg):
        self._test_adjust_height_with_two_children_node(
            right_height, left_height, expected, msg)

    def _test_adjust_height_with_two_children_node(self, right_height, left_height, expected, msg):
        right_child = AVLNode(2, height=right_height)
        left_child = AVLNode(0, height=left_height)
        self.node.right = right_child
        self.node.left = left_child
        AVLTree._adjust_height(self.node)
        self.assertEqual(self.node.height, expected, msg)

# call count of _height
# correctness of _adjust_height in isolation
#   by mocking _height and repeating functional tests


# subclassing TestAdjustHeightFunction to gain access to functional test cases
class TestAdjustHeightStructural(TestAdjustHeightFunctional):
    def setUp(self) -> None:
        self.original_height = AVLTree._height
        return super().setUp()

    def tearDown(self) -> None:
        AVLTree._height = self.original_height
        return super().tearDown()

    def test_adjust_height_height_call_count_with_null_node(self):
        AVLTree._height = MagicMock(return_value=0)
        AVLTree._adjust_height(None)
        AVLTree._height.assert_not_called()

    def test_adjust_height_height_call_count_with_non_null_node(self):
        AVLTree._height = MagicMock(return_value=0)
        AVLTree._adjust_height(self.node)
        self.assertEqual(AVLTree._height.call_count, 2,
                         "Should call _height two times")

    def test_adjust_height_with_leaf_node(self):
        AVLTree._height = MagicMock(return_value=0)
        super().test_adjust_height_with_leaf_node()

    def test_adjust_height_with_single_child_node(self):
        # simulate existance of right child with height 1
        AVLTree._height = MagicMock()
        AVLTree._height.side_effect = [0, 1]
        super().test_adjust_height_with_single_child_node()

    @parameterized.expand(PARAMETERIZATION_1)
    def test_adjust_height_with_two_children_node(self, left_height, right_height, expected, msg):
        AVLTree._height = MagicMock()
        # simulate existance of two children
        AVLTree._height.side_effect = [left_height, right_height]
        super()._test_adjust_height_with_two_children_node(
            left_height, right_height, expected, msg)

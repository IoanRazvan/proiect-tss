import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from avl import AVLTree, AVLNode
from tests.util import SHOULD_BE_FALSE, SHOULD_BE_TRUE

PARAMETERIZATION_1 = [
    (1, False, SHOULD_BE_FALSE),
    (2, True, SHOULD_BE_TRUE)
]

PARAMETERIZATION_2 = [
    (1, 1, False, SHOULD_BE_FALSE),
    (2, 1, False, SHOULD_BE_FALSE),
    (3, 1, True, SHOULD_BE_TRUE)
]

# None
# leaf
# left child of height 1
# left child of height 2
# left.height < right.height + 1
# left.height == right.height + 1
# left.height > right.height + 1


class TestIsUnbalancedLeftFunctional(unittest.TestCase):
    def setUp(self) -> None:
        self.node = AVLNode(1)
        return super().setUp()

    def test_is_unbalanced_left_with_null_node(self):
        with self.assertRaises(AttributeError):
            AVLTree._is_unbalanced_left(None)

    def test_is_unbalanced_left_with_leaf_node(self):
        self.assertFalse(AVLTree._is_unbalanced_left(
            self.node), SHOULD_BE_FALSE)

    @parameterized.expand(PARAMETERIZATION_1)
    def test_is_unbalanced_left_with_single_left_child(self, left_height, expected, msg):
        self._test_is_unbalanced_left_with_single_left_child(
            left_height, expected, msg)

    def _test_is_unbalanced_left_with_single_left_child(self, left_height, expected, msg):
        left_child = AVLNode(0, height=left_height)
        self.node.left = left_child
        self.assertEqual(AVLTree._is_unbalanced_left(self.node), expected, msg)

    @parameterized.expand(PARAMETERIZATION_2)
    def test_is_unbalanced_left_with_two_children(self, left_height, right_height, expected, msg):
        self._test_is_unbalanced_left_with_two_children(
            left_height, right_height, expected, msg)

    def _test_is_unbalanced_left_with_two_children(self, left_height, right_height, expected, msg):
        left_child = AVLNode(0, height=left_height)
        right_child = AVLNode(0, height=right_height)
        self.node.left = left_child
        self.node.right = right_child
        self.assertEqual(AVLTree._is_unbalanced_left(self.node), expected, msg)

# call count of _height
# correctness of _is_unblanaced_left_structural in isolation
#   by mocking _height and repeating functional tests


class TestIsUnbalancedLeftStructural(TestIsUnbalancedLeftFunctional):
    def setUp(self) -> None:
        self.original_height = AVLTree._height
        return super().setUp()

    def tearDown(self) -> None:
        AVLTree._height = self.original_height
        return super().tearDown()

    def test_is_unbalanced_left_height_call_count(self):
        AVLTree._height = MagicMock(return_value=0)
        AVLTree._is_unbalanced_left(self.node)
        self.assertEqual(AVLTree._height.call_count, 2,
                         "Should call _height two times")

    def test_is_unbalanced_left_with_leaf_node(self):
        AVLTree._height = MagicMock(return_value=0)
        super().test_is_unbalanced_left_with_leaf_node()

    @parameterized.expand(PARAMETERIZATION_1)
    def test_is_unbalanced_left_with_single_left_child(self, left_height, expected, msg):
        AVLTree._height = MagicMock()
        AVLTree._height.side_effect = [left_height, 0]
        super()._test_is_unbalanced_left_with_single_left_child(left_height, expected, msg)

    @parameterized.expand(PARAMETERIZATION_2)
    def test_is_unbalanced_left_with_two_children(self, left_height, right_height, expected, msg):
        AVLTree._height = MagicMock()
        AVLTree._height.side_effect = [left_height, right_height]
        self._test_is_unbalanced_left_with_two_children(
            left_height, right_height, expected, msg)

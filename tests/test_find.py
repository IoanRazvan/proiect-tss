from glob import glob
import unittest
from parameterized import parameterized
from avl.avl import AVLTree

from tests.util import SHOULD_BE_FALSE, SHOULD_BE_TRUE, Utils


# tree structure equivalence classes
#   empty tree
#   single node tree
#   one level tree
#   arbitrary number of levels tree
# search node equivalence classes
#   non existent
#   positioned at root
#   positioned at an arbitrary level

REF_1 = 'tests/references/find/empty.json' 
REF_2 = 'tests/references/find/one_node.json'
REF_3 = 'tests/references/find/one_level.json'
REF_4 = 'tests/references/find/more_levels.json'

PARAMETERIZATION_1 = [
    (REF_1, 1, False, SHOULD_BE_FALSE),
    (REF_2, 1, True, SHOULD_BE_TRUE),
    (REF_2, 2, False, SHOULD_BE_FALSE),
    (REF_3, 2, True, SHOULD_BE_TRUE),
    (REF_3, 1, True, SHOULD_BE_TRUE),
    (REF_3, 4, False, SHOULD_BE_FALSE),
    (REF_4, 4, True, SHOULD_BE_TRUE),
    (REF_4, 5, True, SHOULD_BE_TRUE),
    (REF_4, 8, False, SHOULD_BE_TRUE),   
]

class TestFind(unittest.TestCase):
    @parameterized.expand(PARAMETERIZATION_1)
    def test_find(self, file_to_load, node_to_search, expected, msg):
        comparator = lambda x, y: x - y
        tree = Utils.load_tree_from_json_file(comparator, file_to_load) # pragma: no cover
        is_present = tree.find(node_to_search) is not None
        self.assertEqual(is_present, expected, msg)

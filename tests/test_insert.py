import unittest
from parameterized import parameterized

from tests.util import SHOULD_HAVE_SAME_REPRESENTATION, Utils


FILE_1 = "tests/references/insert/rebalance_left_1_before.json"
REF_1 = "tests/references/insert/rebalance_left_1_after.json"
FILE_2 = "tests/references/insert/rebalance_left_2_before.json"
REF_2 = "tests/references/insert/rebalance_left_2_after.json"
FILE_3 = "tests/references/insert/rebalance_right_1_before.json"
REF_3 = "tests/references/insert/rebalance_right_1_after.json"
FILE_4 = "tests/references/insert/rebalance_right_2_before.json"
REF_4 = "tests/references/insert/rebalance_right_2_after.json"
FILE_5 = "tests/references/insert/no_rebalance_before.json"
REF_5 = "tests/references/insert/no_rebalance_after.json"

PARAMETERIZATION_1 = [
    (FILE_1, FILE_1, 1, SHOULD_HAVE_SAME_REPRESENTATION),
    (FILE_1, REF_1, 3, SHOULD_HAVE_SAME_REPRESENTATION),
    (FILE_2, REF_2, 5, SHOULD_HAVE_SAME_REPRESENTATION),
    (FILE_3, REF_3, 1, SHOULD_HAVE_SAME_REPRESENTATION),
    (FILE_4, REF_4, 0, SHOULD_HAVE_SAME_REPRESENTATION),
    (FILE_5, REF_5, 2, SHOULD_HAVE_SAME_REPRESENTATION),
]

# insert existent node
# cause rotate left without parent
# insert to cause rotate left with parent
# insert to cause rotate right without parent
# insert to cause rotate right with parent
# insert to cause rotate right left
# insert to cause rotate left right
# insert without causing rebalancing
class TestInsert(unittest.TestCase):
    @parameterized.expand(PARAMETERIZATION_1)
    def test_insert(self, file_to_load, reference_file, node_to_insert, msg):
        comparator = lambda x, y: x - y
        tree = Utils.load_tree_from_json_file(comparator, file_to_load)
        reference_tree = Utils.load_tree_from_json_file(comparator, reference_file)
        tree.insert(node_to_insert)
        self.assertEqual(Utils.get_tree_json_representation(tree), Utils.get_tree_json_representation(reference_tree), msg)
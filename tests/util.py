from copy import deepcopy
import json
from typing import Callable
from avl.avl import AVLNode, AVLTree


SHOULD_BE_FALSE = "Should be false"
SHOULD_BE_TRUE = "Should be true"
SHOULD_HAVE_HEIGHT = "Should have height {}"
SHOULD_HAVE_SAME_REPRESENTATION = "Should have same representation"


class Utils:
    @staticmethod
    def get_node_dict_representation(node : AVLNode):
        representation = deepcopy(node.__dict__)
        representation['parent'] = None if not node.parent else node.parent.info
        representation['right'] = None if not node.right else node.right.info
        representation['left'] = None if not node.left else node.left.info
        return representation

    @staticmethod
    def load_node_from_dict(dict):
        return AVLNode(dict["info"])
    
    @staticmethod
    def get_tree_json_representation(tree: AVLTree) -> str:
        nodes = []
        if tree.root:
            q = [tree.root]
            while q:
                current_node = q.pop(0)
                nodes.append(Utils.get_node_dict_representation(current_node))
                if current_node.left:
                    q.append(current_node.left)
                if current_node.right:
                    q.append(current_node.right)
        json_obj = json.dumps(nodes, indent=4)
        return json_obj

    @staticmethod
    def load_tree_from_json_file(comparator: Callable[[any, any], int], filename: str) -> AVLTree:
        json_obj = None
        with open(filename, "r") as f:
            json_obj = json.load(f)
        tree = AVLTree(comparator)
        if json_obj:
            tree.root = Utils.load_node_from_dict(json_obj[0])
            for node_dict in json_obj[1:]:
                node = Utils.load_node_from_dict(node_dict)
                parent = tree.find(node_dict["parent"])
                node.parent = parent
                if tree.comparator(node.info, parent.info) > 0:
                    parent.right = node
                else:
                    parent.left = node
                tree._rebalance(parent)
        return tree
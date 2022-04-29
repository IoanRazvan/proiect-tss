from copy import deepcopy
import json
import re
from typing import Union
from typing import Callable


class AVLNode:
    def __init__(self, info: any, height: int = 1, parent: 'AVLNode' = None, left: 'AVLNode' = None, right: 'AVLNode' = None):
        self.info = info
        self.height = height
        self.parent = parent
        self.right = right
        self.left = left

class AVLTree:
    def __init__(self, comparator: Callable[[any, any], int]):
        self.root = None
        self.comparator = comparator

    def insert(self, val: any) -> None:
        if not self.root:
            self.root = AVLNode(val)
            return
        new_node = self._insert(val)
        if not new_node:
            return
        self._rebalance(new_node)

    def _insert(self, val: any) -> Union[AVLNode, None]:
        p = self.root
        prev_p = None
        while p:
            prev_p = p
            if self.comparator(val, p.info) == 0:
                return None
            if self.comparator(val, p.info) > 0:
                p = p.right
            else:
                p = p.left
        new_node = AVLNode(val, parent=prev_p)
        if self.comparator(val, prev_p.info) > 0:
            prev_p.right = new_node
        else:
            prev_p.left = new_node
        return new_node

    def _rebalance(self, node: AVLNode) -> None:
        p = node.parent
        if AVLTree._is_unbalanced_left(node):
            self._rebalance_right(node)
        if AVLTree._is_unbalanced_right(node):
            self._rebalance_left(node)
        AVLTree._adjust_height(node)
        if p:
            self._rebalance(p)

    def _rebalance_right(self, node: AVLNode) -> None:
        m = node.left
        if AVLTree._height(m.right) > AVLTree._height(m.left):
            self._rotate_left(m)
        self._rotate_right(node)

    def _rebalance_left(self, node: AVLNode) -> None:
        m = node.right
        if AVLTree._height(m.left) > AVLTree._height(m.right):
            self._rotate_right(m)
        self._rotate_left(node)

    def _rotate_left(self, node: AVLNode) -> None:
        right = node.right
        node.right = right.left
        right.left = node
        right.parent = node.parent
        node.parent = right
        if node.right:
            node.right.parent = node
        if right.parent:
            if right.parent.right == node:
                right.parent.right = right
            else:
                right.parent.left = right
        else:
            self.root = right
        AVLTree._adjust_height(node)
        AVLTree._adjust_height(right)
        AVLTree._adjust_height(right.parent)

    def _rotate_right(self, node: AVLNode) -> None:
        left = node.left
        node.left = left.right
        left.right = node
        left.parent = node.parent
        node.parent = left
        if node.left:
            node.left.parent = node
        if left.parent:
            if left.parent.left == node:
                left.parent.left = left
            else:
                left.parent.right = left
        else:
            self.root = left
        AVLTree._adjust_height(node)
        AVLTree._adjust_height(left)
        AVLTree._adjust_height(left.parent)

    @staticmethod
    def _adjust_height(node: AVLNode) -> None:
        """
        if node is not None set the height to one plus the maximum of it's children height
        otherwise does nothing
        """
        if node:
            node.height = 1 + max(AVLTree._height(node.left),
                                  AVLTree._height(node.right))

    @staticmethod
    def _height(node: AVLNode) -> int:
        """
        if the node is None return one
        otherwise return the height of the node
        """
        return 0 if not node else node.height

    @staticmethod
    def _is_unbalanced_left(p: AVLNode) -> bool:
        """
        expects non null node
        if the height of left child is greater than the height of right child plus one return true
        otherwise return false
        """
        return AVLTree._height(p.left) > AVLTree._height(p.right) + 1

    @staticmethod
    def _is_unbalanced_right(p: AVLNode) -> bool:
        """
        expects non null node
        if the height of right child is greater than the height of left child plus one return true
        otherwise return false
        """
        return AVLTree._height(p.right) > AVLTree._height(p.left) + 1

    def find(self, val: any) -> Union[AVLNode, None]:
        p = self.root
        while p:
            if self.comparator(val, p.info) == 0:
                return p
            elif self.comparator(val, p.info) > 0:
                p = p.right
            else:
                p = p.left
        return None

    def delete(self, val: any) -> None:
        parent = self._delete(val)
        if parent:
            self._rebalance(parent)

    def _delete(self, val: any) -> Union[AVLNode, None]:
        p = self.find(val)
        if p:
            return self._delete_node(p)
        return None

    def _delete_node(self, node: AVLNode) -> Union[AVLNode, None]:
        if not node.left and not node.right:
            AVLTree._replace_link(node, None)
            if not node.parent:
                self.root = None
                return None
            return node.parent
        if node.left and not node.right:
            node.left.parent = node.parent
            AVLTree.replace_link(node, node.left)
            if not node.parent:
                self.root = node.left
                return None
            return node.parent
        else:
            p = node.right
            while p.left:
                p = p.left
            node.info = p.info
            if p.right:
                p.info = p.right.info
                p.height = 1
                p.right = None
            else:
                p.parent.left = None
            return p.parent

    @staticmethod
    def _replace_link(old_node: AVLNode, new_node: Union[AVLNode, None]):
        if old_node.parent:
            if old_node.parent.left == old_node:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        
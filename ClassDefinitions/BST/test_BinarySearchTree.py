import unittest
from ClassDefinitions.BST.BinarySearchTree import BinarySearchTree

class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        self.bst = BinarySearchTree()

    def test_insert(self):
        self.bst.insert(5)
        self.assertEqual(self.bst.root.value, 5)
        self.bst.insert(3)
        self.assertEqual(self.bst.root.left.value, 3)
        self.bst.insert(7)
        self.assertEqual(self.bst.root.right.value, 7)

    def test_search(self):
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)
        node = self.bst.search(5)
        self.assertEqual(node.value, 5)
        node = self.bst.search(3)
        self.assertEqual(node.value, 3)
        node = self.bst.search(7)
        self.assertEqual(node.value, 7)
        node = self.bst.search(10)
        self.assertIsNone(node)

    def test_balance(self):
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)
        self.bst.insert(2)
        self.bst.insert(4)
        self.bst.insert(6)
        self.bst.insert(8)
        self.bst.balance()
        self.assertEqual(self.bst.root.value, 5)
        self.assertEqual(self.bst.root.left.value, 3)
        self.assertEqual(self.bst.root.left.left.value, 2)
        self.assertEqual(self.bst.root.left.right.value, 4)
        self.assertEqual(self.bst.root.right.value, 7)
        self.assertEqual(self.bst.root.right.left.value, 6)
        self.assertEqual(self.bst.root.right.right.value, 8)
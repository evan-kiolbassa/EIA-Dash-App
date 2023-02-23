class TreeNode:
    """
    A node in a binary search tree.

    Attributes:
        value: The value stored in the node.
        left: The left child of the node.
        right: The right child of the node.
    """

    def __init__(self, value):
        """
        Constructs a new TreeNode instance.

        Args:
            value: The value to be stored in the node.
        """
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    A binary search tree.

    Attributes:
        root: The root node of the tree.
    """

    def __init__(self):
        """
        Constructs a new BinarySearchTree instance.
        """
        self.root = None

    def insert(self, value):
        """
        Inserts a new value into the binary search tree.

        Args:
            value: The value to be inserted.

        Time complexity: O(log n) in the average case and O(n) in the worst case,
        where n is the number of nodes in the tree.
        Space complexity: O(1) in the best case and O(n) in the worst case,
        where n is the number of nodes in the tree.
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        """
        Helper method to insert a new value into the binary search tree.

        Args:
            node: The current node being visited.
            value: The value to be inserted.

        Time complexity: O(log n) in the average case and O(n) in the worst case,
        where n is the number of nodes in the tree.
        Space complexity: O(1) in the best case and O(n) in the worst case,
        where n is the number of nodes in the tree.
        """
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def search(self, value):
        """
        Searches for a value in the binary search tree.

        Args:
            value: The value to search for.

        Returns:
            TreeNode: The node that contains the value, or None if the value is not found.
        """
        return self._search(self.root, value)

    def _search(self, node, value):
        """
        Helper method to search for a value in the binary search tree.

        Args:
            node: The current node being visited.
            value: The value to search for.

        Returns:
            TreeNode: The node that contains the value, or None if the value is not found.
        """
        if node is None or node.value == value:
            return node
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def balance(self):
        """
        Balances the binary search tree.


        Time complexity: O(n) in the worst case, where n is the number of nodes in the tree.
        Space complexity: O(n) in the worst case, where n is the number of nodes in the tree.
        """
        values = []
        self._inorder_traversal(self.root, values)
        self.root = self._create_balanced_tree(values, 0, len(values)-1)

    def _inorder_traversal(self, node, values):
        """
        Helper method to perform an inorder traversal of the binary search tree.

        Args:
            node: The current node being visited.
            values: The list to store the values of the nodes in the tree.
        """
        if node is not None:
            self._inorder_traversal(node.left, values)
            values.append(node.value)
            self._inorder_traversal(node.right, values)

    def _create_balanced_tree(self, values, start, end):
        """
        Helper method to create a balanced binary search tree from a sorted list of values.

        Args:
            values: The list of values.
            start: The starting index of the sublist.
            end: The ending index of the sublist.

        Returns:
            TreeNode: The root node of the balanced binary search tree.
        """
        if start > end:
            return None

        mid = (start + end) // 2
        node = TreeNode(values[mid])

        node.left = self._create_balanced_tree(values, start, mid-1)
        node.right = self._create_balanced_tree(values, mid+1, end)

        return node
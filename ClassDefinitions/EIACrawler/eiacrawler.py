import requests
from ClassDefinitions.BST.BinarySearchTree import TreeNode, BinarySearchTree

class EIACrawler:
    """
    A web crawler for the EIA API.
    """

    def __init__(self, api_key):
        """
        Constructs a new EIACrawler instance.

        Args:
            api_key: The API key to access the EIA API.
        """
        self.api_key = api_key
        self.tree = BinarySearchTree()

    def crawl(self):
        """
        Crawls the EIA API to obtain the category ids and category names,
        storing them in a Binary Search Tree.

        Returns:
            BinarySearchTree: The binary search tree containing the category ids and names.
        """
        url = f"https://api.eia.gov/category/?api_key={self.api_key}&all=true"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for category in data["category"]:
                self.tree.insert((category["category_id"], category["name"]))

            self.tree.balance()

        return self.tree

    def search(self, keyword):
        """
        Performs a depth-first search of the binary search tree to find the
        data series ids or data series ids associated with a matched category type.

        Args:
            keyword: The keyword to search for.

        Returns:
            List: A list of the data series ids or data series ids associated with a matched category type.
        """
        results = []
        self._dfs_search(self.tree.root, keyword, results)
        return results

    def _dfs_search(self, node, keyword, results):
        """
        Helper method to perform a depth-first search of the binary search tree to find the
        data series ids or data series ids associated with a matched category type.

        Args:
            node: The current node being visited.
            keyword: The keyword to search for.
            results: A list to store the data series ids or data series ids associated with a matched category type.
        """
        if node is not None:
            if keyword.lower() in node.value[1].lower():
                results.extend(self._get_series_ids(node))
            self._dfs_search(node.left, keyword, results)
            self._dfs_search(node.right, keyword, results)

    def _get_series_ids(self, node):
        """
        Helper method to get the data series ids or data series ids associated with a matched category type.

        Args:
            node: The current node being visited.

        Returns:
            List: A list of the data series ids or data series ids associated with a matched category type.
        """
        series_ids = []
        url = f"https://api.eia.gov/category/?api_key={self.api_key}&category_id={node.value[0]}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for child in data["category"]["childcategories"]:
                for series in child["childseries"]:
                    series_ids.append(series["series_id"])

        return series_ids
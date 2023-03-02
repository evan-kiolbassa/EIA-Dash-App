import scrapy
from scrapy.crawler import CrawlerProcess
from ClassDefinitions.BST.BinarySearchTree import TreeNode, BinarySearchTree

class EIACrawler((scrapy.Spider)):
    """
    A web crawler for the EIA API.
    """
    name = "eia"

    def __init__(self, api_key, *args, **kwargs):
        """
        Constructs a new EIACrawler instance.

        Args:
            api_key: The API key to access the EIA API.
        """
        self.api_key = api_key
        self.tree = BinarySearchTree()
        super(EIACrawler, self).__init__(*args, **kwargs)
        self.start_urls = [
        f"https://api.eia.gov/category/?api_key={self.api_key}&all=true"
    ]

    def parse(self, response):
        """
        Parses the response from the EIA API and inserts the category IDs and names into the binary search tree.

        Args:
            response: The response from the EIA API.
        """
        data = response.json()

        if "category" in data:
            for category in data["category"]:
                self.tree.insert((category["category_id"], category["name"]))

            self.tree.balance()
        else:
            raise ValueError("Failed to parse API response: 'category' not found")

    def crawl(self):
        """
        Crawls the EIA API to obtain the category IDs and category names,
        storing them in a Binary Search Tree.

        Returns:
            BinarySearchTree: The binary search tree containing the category IDs and names.
        """
        process = CrawlerProcess()
        process.crawl(EIACrawler, self.api_key)
        process.start()

        return self.tree

    def search(self, keyword, params=None):
        """
        Performs a depth-first search of the binary search tree to find the
        data series IDs or data series IDs associated with a matched category type.

        Args:
            keyword: The keyword to search for.

        Returns:
            List: A list of the data series IDs or data series IDs associated with a matched category type.
        """
        results = []
        self._dfs_search(self.tree.root, keyword, results, params)
        return results

    def _dfs_search(self, node, keyword, results, params=None):
        """
        Helper method to perform a depth-first search of the binary search tree to find the
        data series IDs or data series IDs associated with a matched category type.

        Args:
            node: The current node being visited.
            keyword: The keyword to search for.
            results: A list to store the data series IDs or data series IDs associated with a matched category type.
        """
        if node is not None:
            if keyword.lower() in node.value[1].lower():
                results.extend(self._get_series_ids(node, params))
            self._dfs_search(node.left, keyword, results, params)
            self._dfs_search(node.right, keyword, results, params)

    def _get_series_ids(self, node, params=None):
        """
        Helper method to get the data series IDs or data series IDs associated with a matched category type.

        Args:
            node: The current node being visited.
            params: A dictionary of parameters to include in the API request.

        Returns:
            List: A list of the data series IDs or data series IDs associated with a matched category type.
        """
        if params is None:
            params = {}

        series_ids = []
        url = f"https://api.eia.gov/category/?api_key={self.api_key}&category_id={node.value[0]}"
        response = scrapy.Request(url, callback=self.parse_series_ids, meta={"series_ids": series_ids}, params=params)

        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve series IDs: {response.status_code}")

        return response.meta["series_ids"]

    def parse_series_ids(self, response):
        """
        Parses the response from the EIA API and extracts the data series IDs.

        Args:
            response: The response from the EIA API.

        Returns:
            List: A list of the data series IDs.
        """
        data = response.json()

        if "category" in data and "childcategories" in data["category"]:
            for child in data["category"]["childcategories"]:
                for series in child["childseries"]:
                    self.meta["series_ids"].append(series["series_id"])
        else:
            raise ValueError("Failed to parse API response: 'category' or 'childcategories' not found")

        return self.meta["series_ids"]
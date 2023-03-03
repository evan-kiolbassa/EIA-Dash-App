import unittest
from scrapy.http import Response
from scrapy.spiders import Spider
from unittest.mock import patch
from ClassDefinitions.BST.BinarySearchTree import BinarySearchTree, TreeNode
from ClassDefinitions.EIACrawler.eiacrawler import EIACrawler

class TestEIACrawler(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.crawler = EIACrawler(self.api_key)

    @patch("scrapy.http.Response.json")
    def test_parse_with_category(self, mock_json):
        mock_json.return_value = {
            "category": [
                {
                    "category_id": "1",
                    "name": "Category 1"
                },
                {
                    "category_id": "2",
                    "name": "Category 2"
                }
            ]
        }
        self.crawler.parse(Response("https://api.eia.gov/category", body=b""))
        self.assertEqual(self.crawler.tree.root.value, ("1", "Category 1"))
        self.assertEqual(self.crawler.tree.root.right.value, ("2", "Category 2"))

    @patch("scrapy.http.Response.json")
    def test_parse_without_category(self, mock_json):
        mock_json.return_value = {}
        with self.assertRaises(ValueError):
            self.crawler.parse(Response("https://api.eia.gov/category", body=b""))

    def test_crawl(self):
        self.assertIsInstance(self.crawler.crawl(), BinarySearchTree)

    def test_search_with_keyword(self):
        self.crawler.tree.insert(("1", "Category 1"))
        self.crawler.tree.insert(("2", "Category 2"))
        self.assertEqual(self.crawler.search("category"), [("1", "Category 1"), ("2", "Category 2")])

    def test_search_without_keyword(self):
        self.crawler.tree.insert(("1", "Category 1"))
        self.crawler.tree.insert(("2", "Category 2"))
        self.assertEqual(self.crawler.search("subcategory"), [])

    def test_dfs_search(self):
        node1 = TreeNode(("1", "Category 1"))
        node2 = TreeNode(("2", "Category 2"))
        node3 = TreeNode(("3", "Subcategory 1"))
        node4 = TreeNode(("4", "Subcategory 2"))
        node1.right = node2
        node2.left = node3
        node2.right = node4
        results = []
        self.crawler._dfs_search(node1, "category", results)
        self.assertEqual(results, [("1", "Category 1"), ("2", "Category 2")])

    @patch("scrapy.http.Request")
    @patch("scrapy.http.Response.json")
    def test_get_series_ids(self, mock_json, mock_request):
        mock_json.return_value = {
            "category": {
                "childcategories": [
                    {
                        "category_id": "3",
                        "childseries": [
                            {
                                "series_id": "1"
                            },
                            {
                                "series_id": "2"
                            }
                        ]
                    }
                ]
            }
        }
        mock_request.return_value.status_code = 200
        mock_request.return_value.meta = {"series_ids": []}
        self.assertEqual(self.crawler._get_series_ids(TreeNode(("3", "Subcategory 1"))), ["1", "2"])

    @patch("scrapy.http.Response.json")
    def test_parse_series_ids_with_category(self, mock_json):
        mock_json.return_value = {
            "category": {
                "childcategories": [
                    {
                        "childseries": [
                            {
                                "series_id": "1"
                            }
                        ]
                    }
                ]
            }
        }
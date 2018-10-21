from unittest import TestCase

import requests


class TestFlaskApiUsingRequests(TestCase):
    def test_products(self):
        response = requests.get('http://192.168.99.100:8081/api/products')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        payload = {
            "product": {
                "image": "banana.png",
                "name": "Product 1",
                "price": 2,
                "slug": "product-1"
            }
        }
        response = requests.post('http://192.168.99.100:8081/api/product/create', payload)
        self.assertEqual(response.status_code, 200)

    def test_product(self):
        response = requests.get('http://192.168.99.100:8081/api/product/product-1')
        self.assertEqual(response.status_code, 200)
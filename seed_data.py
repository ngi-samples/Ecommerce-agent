# seed_data.py
import json
from db import products_collection

with open("data/amazon_mock_products.json", "r") as f:
    product_data = json.load(f)

unique_data = {f"{item['title']}|{item['description']}": item for item in product_data}
products_collection.delete_many({})  # Clear old data
products_collection.insert_many(unique_data.values())
print("Data seeded.")

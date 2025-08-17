from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Choose database and collection
db = client["shopping_assistant"]
products_collection = db["products"]
cart_collection = db["cart"]

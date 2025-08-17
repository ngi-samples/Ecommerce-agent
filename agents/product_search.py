# agents/product_search.py
from dspy import Module, InputField, OutputField, Signature, ChainOfThought
from dspy.teleprompt import BootstrapFewShot
from db import products_collection

# Fetch products
db_products = list(products_collection.find({}, {"_id": 0}))
print(f"✅ Loaded {len(db_products)} products.")

# === Signature ===
class ProductSearchSignature(Signature):
    query: str = InputField(desc="User's search query")
    products_list: str = InputField(desc="List of products with title, price, rating")
    response: str = OutputField(desc="Top 3 relevant products with reasons")

class ProductSearchModule(Module):
    def __init__(self, products):
        super().__init__()
        self.predictor = ChainOfThought(ProductSearchSignature)
        self.products = products

    def forward(self, query):
        product_text = "\n".join(
            f"{i+1}. {p['title']} - ₹{p['price']} - ⭐{p['rating']}"
            for i, p in enumerate(self.products[:20])
        )
        result = self.predictor(query=query, products_list=product_text)
        return result

# Training data
trainset = [
    # ... (your examples)
]

def evaluate_quality(gold, pred, trace=None):
    return "1." in pred.response and "2." in pred.response and "3." in pred.response

def compile_optimized_search(products):
    unoptimized = ProductSearchModule(products=products)
    optimizer = BootstrapFewShot(metric=evaluate_quality, max_labeled_demos=3)
    return optimizer.compile(unoptimized, trainset=trainset)

optimized_search = compile_optimized_search(db_products)
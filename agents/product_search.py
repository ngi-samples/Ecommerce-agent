# agents/product_search.py
from dspy import Module, InputField, OutputField, Signature, Example, ChainOfThought
from dspy.teleprompt import BootstrapFewShot
from db import products_collection

# ==========================
# Fetch products
# ==========================
db_products = list(products_collection.find({}, {"_id": 0}))
print(f"✅ Loaded {len(db_products)} products.")

# ==========================
# DSPy Signature
# ==========================
class ProductSearchSignature(Signature):
    query: str = InputField(desc="User's search query")
    response: str = OutputField(desc="Top 3 relevant products with reasons")

# ==========================
# DSPy Module
# ==========================
class ProductSearchModule(Module):
    def __init__(self, products):
        super().__init__()
        self.products = products
        self.predictor = ChainOfThought(ProductSearchSignature)

    # forward now only requires query
    def forward(self, query):
        # Format product list for context
        product_text = "\n".join(
            f"{i+1}. {p['title']} - ₹{p['price']} - ⭐{p['rating']}"
            for i, p in enumerate(self.products[:20])
        )

        # Run the predictor
        return self.predictor(query=query, products_list=product_text)

# ==========================
# Training Examples
# ==========================
trainset = [
    Example(
        query="budget smartphone under 30000",
        response="1. Redmi Note 13 – Affordable price and good specs\n2. iQOO Neo 7 – Great performance\n3. Realme 12 Pro – Balanced features"
    ).with_inputs("query"),

    Example(
        query="laptop for programming under 60000",
        response="1. HP Pavilion 15 – Good CPU and RAM\n2. Dell Inspiron 15 – Reliable build\n3. Lenovo Ideapad Gaming – Strong performance"
    ).with_inputs("query")
]

# ==========================
# Evaluator for optimizer
# ==========================
def evaluate_quality(gold, pred, trace=None):
    return "1." in pred.response and "2." in pred.response and "3." in pred.response

# ==========================
# Compile Optimized Search Module
# ==========================
def compile_optimized_search(products):
    unoptimized = ProductSearchModule(products=products)
    
    if not trainset:
        print("⚠️ No training data found. Using unoptimized search.")
        return unoptimized

    optimizer = BootstrapFewShot(metric=evaluate_quality, max_labeled_demos=3)
    return optimizer.compile(unoptimized, trainset=trainset)

# ==========================
# Final optimized search
# ==========================
optimized_search = compile_optimized_search(db_products)

# ==========================
# Public function for Streamlit
# ==========================
def run_search(query: str):
    return optimized_search(query=query)

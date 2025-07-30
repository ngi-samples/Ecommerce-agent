🛒 Ecommerce Agent (DSPy-based)

An intelligent Ecommerce Agent built using [DSPy](https://github.com/stanfordnlp/dspy) for seamless product search, comparison, and cart management — integrated with a lightweight frontend and backend.

---

## ✨ Features

- 🔍 Product Search: Intelligent querying using natural language.
- ⚖️ **Product Comparison**: Side-by-side comparison of features and prices.
- 🛒 **Cart Management**: Add/remove/view products from the cart.
- 📄 **Mock Data Integration**: Works with `amazon_mock_products.json`.
- 🧠 **Memory Support**: Retains user session state using custom memory logic.
- 🌐 **Frontend**: Simple HTML interface for interaction.
- 🚀 **API Server**: Flask backend (`server.py`) to serve frontend and DSPy agent logic.

---

## 🧱 Project Structure

  dspy-agent/
    ├── agents/
    │   ├── product_search.py
    │   ├── product_comparator.py
    │   └── cart_manager.py
    ├── config.py
    ├── core/
    │   └── memory.py
    ├── data/
    │   └── amazon_mock_products.json
    ├── frontend/
    │   └── index.html
    ├── main.py
    ├── server.py
    ├── test_cart.py
    ├── test_compare.py
    └── README.md



## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/ngi-samples/Ecommerce-agent.git
cd dspy-agent
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is not available, manually install:

bash
Copy
Edit
pip install dspy openai flask
3. Run the server
bash
Copy
Edit
python server.py
4. Access frontend
Open your browser and visit:

arduino
Copy
Edit
http://localhost:5000
🧪 Running Tests
bash
Copy
Edit
python test_cart.py
python test_compare.py
📁 Data Format
The mock product data is stored in data/amazon_mock_products.json. You can modify or extend it for different product categories.

📌 Dependencies
Python 3.8+

DSPy

Flask

OpenAI (for LLM if used)

🙌 Contribution
Feel free to submit pull requests or open issues for improvements or feature requests.

📝 License
This project is under the MIT License.

👨‍💻 Author
Built by Shaik Uzair Ahmed

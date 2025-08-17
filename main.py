# app.py
import streamlit as st

# 🔥 MUST BE FIRST: This configures DSPy safely
try:
    import dspy_setup  # This will configure DSPy only once
except Exception as e:
    st.error(f"❌ Failed to initialize DSPy: {str(e)}")
    st.stop()

# Now safe to import agents
from agents.cart_manager import CartManagerModule
from agents.product_search import optimized_search
from agents.product_comparator import ProductComparatorModule
from db import products_collection
import json

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []

@st.cache_resource
def get_cart_manager():
    return CartManagerModule()

@st.cache_resource
def get_comparator():
    return ProductComparatorModule()

cart_manager = get_cart_manager()
comparator = get_comparator()

# === UI ===
st.set_page_config(page_title="🛍️ AI Shopping Assistant", page_icon="🛍️", layout="wide")
st.title("🛍️ AI Shopping Assistant")
st.markdown("Let me help you **search**, **compare**, and **manage your cart** like a pro!")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["🔍 Search Product", "⚖️ Compare Products", "🛒 Cart Management"])

# === Search Page ===
if page == "🔍 Search Product":
    st.header("🔍 Search for Products")
    query = st.text_input("What are you looking for?", placeholder="e.g., smartphone under ₹30,000")

    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Finding best options..."):
                try:
                    result = optimized_search(query=query)
                    st.success("Here are the top recommendations:")
                    st.markdown(f"> {result.response.replace(chr(10), chr(10) + '> ')}")
                except Exception as e:
                    st.error(f"Search error: {str(e)}")

# === Compare Page ===
elif page == "⚖️ Compare Products":
    st.header("⚖️ Compare Two Products")
    all_titles = [p['title'] for p in products_collection.find({}, {"title": 1, "_id": 0})]

    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("First Product", all_titles, key="p1")
    with col2:
        p2 = st.selectbox("Second Product", all_titles, key="p2")

    if st.button("Compare"):
        if p1 == p2:
            st.warning("Pick two different products.")
        else:
            with st.spinner("Comparing..."):
                try:
                    result = comparator(p1, p2)
                    st.markdown("### 🤖 AI Comparison")
                    st.code(json.dumps(result, indent=2) if isinstance(result, dict) else str(result), language="json")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# === Cart Page ===
elif page == "🛒 Cart Management":
    st.header("🛒 Your Cart")
    
    if st.session_state.cart:
        for i, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1])
            c1.write(f"{i+1}. {item}")
            if c2.button("🗑️", key=f"rm_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    else:
        st.info("Cart is empty.")

    add_item = st.text_input("Add product", placeholder="e.g., iPhone 14")
    if st.button("Add to Cart"):
        if add_item.strip() and add_item in [p['title'] for p in products_collection.find({}, {"title":1})]:
            st.session_state.cart.append(add_item)
            st.success(f"✅ {add_item} added!")
            st.rerun()
        elif add_item.strip():
            st.warning("Product not found.")
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from recommender import get_recommendations
from ai_assistant import ask_gemini


st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #f8f9ff, #eef2ff);
}

h1 {
    color: #4f46e5;
    font-size: 42px !important;
    font-weight: 800;
}

h2, h3 {
    color: #312e81;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🛍️ AI Shopping Assistant")
st.subheader("Personalized Recommendations for You")

st.write(
    "Find the best products based on your budget, category and preferences."
)


# Connect to SQLite database
engine = create_engine("sqlite:///shopping.db")

# Read products from database
products = pd.read_sql(
    "SELECT * FROM products",
    engine
)


# Store recommendations
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


st.divider()

st.header("🔍 Tell us what you're looking for")


category = st.selectbox(
    "Select Product Category",
    products["category"].unique()
)


budget = st.number_input(
    "Enter your maximum budget (₹)",
    min_value=0,
    value=50000
)


preference = st.text_input(
    "What is your preference?",
    placeholder="Example: Good performance and battery life"
)


if st.button("✨ Get Personalized Recommendations"):

    st.session_state.recommendations = get_recommendations(
        products,
        category,
        budget,
        preference
    )


# Show recommendations
recommendations = st.session_state.recommendations


if recommendations is not None:

    st.subheader("✨ Your Personalized Recommendations")

    if recommendations.empty:

        st.warning("No products found for your requirements.")

    else:

        for _, product in recommendations.iterrows():

            st.markdown(
                f"""
                ### 🛍️ {product['name']}

                **Brand:** {product['brand']}  
                **Price:** ₹{product['price']:,.0f}  
                **Rating:** ⭐ {product['rating']}  
                **Match Score:** {product['match_score'] * 100:.0f}%

                {product['description']}
                """
            )

            st.divider()


        # AI Assistant
        st.subheader("🤖 Ask AI Shopping Assistant")


        question = st.text_input(
            "Ask something about these recommendations",
            placeholder="Example: Which one is best for performance?"
        )


        if st.button("💬 Ask AI") and question:

            product_info = recommendations[
                ["name", "brand", "price", "rating", "description"]
            ].to_string(index=False)


            prompt = f"""
You are an AI Shopping Assistant.

Category: {category}
Maximum budget: ₹{budget}
Preference: {preference}

Recommended products:

{product_info}

User question:
{question}

Answer clearly and briefly.
Recommend only from the products provided above.
"""


            with st.spinner("🤖 AI is thinking..."):
                answer = ask_gemini(prompt)


            st.markdown("### 🤖 AI Recommendation")
            st.write(answer)
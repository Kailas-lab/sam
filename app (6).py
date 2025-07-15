import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.llm import LLMChain
import os

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAOBV-XP98L4tQCXd_sfmbrp2VuLA9o3TA"

# Streamlit page setup
st.set_page_config(page_title="Chef AI - Recipe Generator", layout="centered")
st.title("👨‍🍳 AI Chef - Main Course Recipe Generator")
st.markdown("Enter ingredients (comma-separated). The AI chef will create a main course using only those ingredients!")

# LangChain prompt template
prompt = PromptTemplate(
    input_variables=["ingredients"],
    template="""
You are a professional chef AI that also knows about nutrition.

Create a complete main course recipe using only the ingredients: {ingredients}.

Important Rules:
- DO NOT add any extra ingredients.
- Use only what is listed. Assume basic pantry items (salt, water, oil) only if required for cooking.
- Make it a main course dish – not a side or snack.
- Be creative and ensure the dish feels satisfying and complete.

Explicitly include the following estimated nutritional information **per serving** for the recipe:
1. Calories (kcal)
2. Carbohydrates (g)
3. Protein (g)
4. Fat (g)
5. Fiber (g)
6. Sodium (mg)

Output Format:
1. Recipe Title
2. Ingredients List (only from the input)
3. Preparation Steps
4. Estimated Cook Time
5. Nutrient Chart per Serving (Estimated):
    | Nutrient      | Amount   |
    |---------------|----------|
    | Calories      | ___ kcal |
    | Carbohydrates | ___ g    |
    | Protein       | ___ g    |
    | Fat           | ___ g    |
    | Fiber         | ___ g    |
    | Sodium        | ___ mg   |
"""
)

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# User input
user_input = st.text_input("📝 Ingredients", placeholder="e.g. chicken, spinach, garlic")

if st.button("🍽️ Generate Recipe"):
    if not user_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        with st.spinner("Cooking up something delicious..."):
            recipe = chain.run(user_input)
        st.markdown("### 🍛 Generated Recipe")
        st.code(recipe, language="markdown")

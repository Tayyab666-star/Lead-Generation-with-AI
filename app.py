import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_leads(query: str):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    system_prompt = """You are a lead generation assistant. For each query:
    1. Provide numbered leads (1., 2., etc.)
    2. Include detailed information for each lead:
       - Full name and position
       - Company name and location
       - Contact information (email, LinkedIn)
       - Brief description of relevance
    3. Add source information when available (LinkedIn, company website, etc.)
    4. For LinkedIn profiles:
       - Only provide profiles that are currently active and accessible
       - Include the complete LinkedIn URL (e.g., https://www.linkedin.com/in/username)
       - Verify the profile matches the person's current role and company
    Format the response in a clean, readable way.
    
    IMPORTANT: Double-check all LinkedIn URLs to ensure they are valid and accessible before including them."""
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get("choices", [])[0].get("message", {})
            return [{"result": result.get("content", "No leads found.")}]
        else:
            return [{"error": f"Groq API error: {response.status_code}"}]
    except Exception as e:
        return [{"error": str(e)}]

def call_groq_chat_completion(user_message: str):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    system_message = """You are a specialized lead generation and business development assistant. Focus only on:
    1. Lead generation strategies and insights
    2. Marketing email templates and campaigns
    3. Business development tactics
    4. Sales outreach methods
    5. Lead qualification and scoring
    6. Market research and competitor analysis
    7. Analyzing and explaining previously generated leads
    
    If the query is outside these topics, politely explain that you can only assist with lead generation and business development related questions.
    Always provide practical, actionable advice with examples when possible."""
    
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("choices", [])[0].get("message", {})
        else:
            return {"error": f"Groq API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Set page config
st.set_page_config(page_title="Lead Generation AI", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp {
    max-width: 1200px;
    margin: 0 auto;
}
.lead-container {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
}
.source-info {
    color: #666;
    font-size: 0.9em;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎯 Lead Generation AI with Groq")
st.markdown("""Generate detailed, relevant leads with AI-powered search and verification.  
*Powered by Groq's advanced language models*""")

# Main lead generation section
st.header("🔍 Find Potential Leads")
query = st.text_input("What kind of leads are you looking for?", placeholder="e.g., 'Find tech startup founders in London with successful exits'")

col1, col2 = st.columns([2,1])
with col1:
    if st.button("🚀 Generate Leads", type="primary") and query:
        with st.spinner("🔄 Searching for leads..."):
            leads = get_leads(query)
        
        if "error" in leads[0]:
            st.error(leads[0]["error"])
        else:
            st.markdown("### 📋 Generated Leads")
            st.markdown(leads[0]["result"])

with col2:
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be specific about industry and location
    - Mention company size or stage
    - Include specific roles or titles
    - Add any special criteria
    """)

# Separator
st.markdown("---")

# Chat section
st.header("💬 Lead Generation Assistant")
st.markdown("Get expert advice on lead generation, marketing strategies, and business development. Ask about specific leads, outreach tactics, or market insights.")

user_message = st.text_area(
    "Your question:", 
    placeholder="e.g., 'How can I effectively reach out to the tech founders we found?' or 'Create an email template for the financial leads'"
)

col3, col4 = st.columns([2,1])
with col3:
    if st.button("💭 Get Expert Advice", type="secondary") and user_message:
        with st.spinner("🤔 Analyzing your question..."):
            chat_response = call_groq_chat_completion(user_message)
        
        if "error" in chat_response:
            st.error(chat_response["error"])
        else:
            st.markdown("### 🎯 Expert Guidance")
            st.markdown(chat_response.get("content", "No response generated."))

with col4:
    st.markdown("### 💡 Suggested Topics")
    st.markdown("""
    - Lead qualification strategies
    - Email templates & outreach
    - Market research insights
    - Sales conversion tactics
    - Follow-up strategies
    """)

import streamlit as st
import os
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
from groq import Groq

# Set page configuration
st.set_page_config(page_title="Lead Generation AI", page_icon="💼", layout="wide")

# Initialize session state
if 'GROQ_API_KEY' not in st.session_state:
    st.session_state.GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if 'leads' not in st.session_state:
    st.session_state.leads = []

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Reusable Groq client setup
@st.cache_resource
def get_groq_client(api_key: str):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        return None

# Groq API call
def get_groq_response(client, messages: List[Dict[str, str]]) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error fetching Groq response: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later."

# Extract and save lead data

def extract_lead_data(response: str) -> Dict[str, Any]:
    try:
        json_start = response.find("```json")
        json_end = response.find("```", json_start + 6)
        if json_start != -1 and json_end != -1:
            json_str = response[json_start + 7:json_end].strip()
            return json.loads(json_str)
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
    return {}

def update_lead_info(lead_data: Dict[str, Any]):
    if not lead_data:
        return
    lead_data['timestamp'] = datetime.now().isoformat()
    if lead_data.get('email'):
        for i, lead in enumerate(st.session_state.leads):
            if lead.get('email') == lead_data.get('email'):
                st.session_state.leads[i].update(lead_data)
                return
    st.session_state.leads.append(lead_data)

def save_leads_to_csv():
    if st.session_state.leads:
        df = pd.DataFrame(st.session_state.leads)
        df.to_csv('leads.csv', index=False)
        return True
    return False

# UI
st.title("Lead Generation AI Assistant 💼")

with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("
", st.session_state.GROQ_API_KEY, type="password")
    if st.button("Save API Key"):
        st.session_state.GROQ_API_KEY = api_key_input
        st.success("API Key saved!")
    st.markdown("---")
    st.header("Lead Analytics")
    hot_leads = sum(1 for lead in st.session_state.leads if lead.get('lead_quality') == 'hot')
    warm_leads = sum(1 for lead in st.session_state.leads if lead.get('lead_quality') == 'warm')
    cold_leads = sum(1 for lead in st.session_state.leads if lead.get('lead_quality') == 'cold')
    col1, col2, col3 = st.columns(3)
    col1.metric("Hot Leads", hot_leads)
    col2.metric("Warm Leads", warm_leads)
    col3.metric("Cold Leads", cold_leads)
    if st.button("Export Leads"):
        if save_leads_to_csv():
            st.success("Leads exported to leads.csv")
            st.download_button(
                label="Download CSV",
                data=pd.DataFrame(st.session_state.leads).to_csv(index=False),
                file_name="leads.csv",
                mime="text/csv"
            )
        else:
            st.warning("No leads to export")

# Persona intro message
persona_prefix = {
    "role": "system",
    "content": (
        "You are a professional marketing assistant specialized in lead generation. "
        "Provide actionable, structured lead data, contact strategies, and outreach plans. "
        "All responses must be related to lead generation, target audience analysis, or marketing."
    )
}

# Chat start
if not st.session_state.messages:
    st.session_state.messages.append(persona_prefix)
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm your Marketing Lead Assistant. How can I help today?"})

# Display past messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        content = message["content"]
        if message["role"] == "assistant":
            json_start = content.find("```json")
            if json_start != -1:
                content = content[:json_start]
        st.markdown(content)

# Prompt input
if prompt := st.chat_input("Ask for leads, outreach strategy, etc..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    client = get_groq_client(st.session_state.GROQ_API_KEY.strip())
    if client:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_groq_response(client, st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response})
                lead_data = extract_lead_data(response)
                update_lead_info(lead_data)
                display_response = response.split("```json")[0]
                st.markdown(display_response)
    else:
        st.error("Please enter a valid Groq API key in the sidebar.")
